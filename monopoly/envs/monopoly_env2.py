import gymnasium as gym
from gymnasium import spaces
# from gymnasium.spaces import Box
import numpy as np
import pandas as pd
# import csv


# import pandas as pd
# import matplotlib.pyplot as plt
class Player:
    def __init__(self, num, tag="player1", static=False):
        self.tag = tag
        self.pos = 0
        self.num = num
        self.ally_num = None
        self.prev_pos = []
        self.possession_indices = []
        self.isStatic = static
        self.money = 1500

    def change_pos(self, roll_dice, num_states):
        cur_pos = self.pos + roll_dice
        self.pos = (cur_pos) % num_states
        if (cur_pos >= num_states):
            self.money += 100

    def buy(self, board):
        city = board[self.pos]
        if city.owner is not None:
            print(f"City is already owned by {city.owner.num}")
            return board

        if city.price > self.money:
            print(f"Insufficient money")
            return board

        self.possession_indices.append(self.pos)
        board[self.pos].owner = self
        self.money -= city.price

        return board

    def give(self, board):

        if self.pos not in self.possession_indices:
            print(f"City not owned by current player")
            return board

        self.possession_indices.remove(self.pos)
        # board[self.pos].owner = self.ally_num
        board[self.pos].owner = self.ally
        return board

    def mortgage(self, board, cities):
        if self.pos not in self.possession_indices:
            return board

        city = cities[self.pos]
        if city.num_houses == 0:
            city.is_mortgaged = True
        else:
            print(f"Handle the condition where mortgage was selected, but city has houses")

        return board

    def pay_rent(self, board):
        city = board[self.pos]
        if city.owner is None:
            return

        rent = city.rents_array[city.num_houses]
        self.money -= rent
        city.owner.money += rent

    def assign_ally(self, ally):
        self.ally = ally


class City:
    price_per_house = 5  # common for all houses
    def __init__(self, name, color, price, price_per_house, rent, rent_1_house, rent_2_house,
                 rent_3_house, rent_4_house, rent_hotel, mortgage, owner=None, num_houses=0, is_mortgaged=False):
        self.name = name
        self.color = color
        self.owner = owner
        self.num_houses = num_houses
        self.is_mortgaged = is_mortgaged
        self.price = price
        self.price_per_house = price_per_house
        self.rent = rent
        self.rent_1_house = rent_1_house
        self.rent_2_house = rent_2_house
        self.rent_3_house = rent_3_house
        self.rent_4_house = rent_4_house
        self.rent_hotel = rent_hotel
        self.mortgage = mortgage

        self.rents_array = [self.rent, self.rent_1_house, self.rent_2_house,
                            self.rent_3_house, self.rent_4_house, self.rent_hotel]


class MonopolyEnv2(gym.Env):
    def __init__(self, num_states, dice_size, num_agents=2, max_turns=100, file='city.csv'):
        self.static_agents = None
        self.actions = ["skip", "buy", "give"]
        self.action = None
        self.reward = 0
        self.action_space = spaces.Discrete(3)
        self.done = False
        self.truncated = False
        self.dice_size = dice_size
        self.file = file
        self.episode_length = 0
        # self.no_operation = False
        self.roll_val = 0
        self.current_pos = 0
        self.current_pos_owner = 0

        self.players = [Player(1, "player1", False), Player(2, "player2")]
        self.current_player_index = 1
        self.current_player = self.players[self.current_player_index]

        # TODO: Better way of doing this
        self.players[0].assign_ally(self.players[1])
        self.players[1].assign_ally(self.players[0])

        self.player_init_money = 1500
        self.num_states = num_states
        self.num_agents = num_agents
        self.board = np.array(self.create_board(),dtype=City)
        # self.state_observation = [0, self.board]
        self.max_turns = max_turns
        # dim = 4 + self.num_agents  # 4 = agent_nos,cur_pos,cur_pos_owner,money
        # self.observation_space = spaces.Box(low=0, high=max(num_states, num_agents, dice_size, self.player_init_money),
        #                                     shape=(dim,), dtype=np.float64)
        dim = 3 + self.num_agents
        self.observation_space = spaces.Box(low=0, high=max(num_states, num_agents, dice_size),
                                            shape=(dim,), dtype=np.float64)
        self.roll()

    def create_board(self):
        board = np.empty(self.num_states, dtype=City)
        df = pd.read_csv(self.file)
        for index, row in df.iterrows():
            if index < self.num_states:
                board[index] = City(row['name'], row['color'],row['price'], row['price_per_house'], row['rent'],
                                    row['rent_1_house'],row['rent_2_house'], row['rent_3_house'], row['rent_4_house'],
                                    row['rent_hotel'], row['mortgage'])
            else:
                break
        return board

    def reset(self, seed=None, options=None):
        self.done = False
        self.truncated = False
        self.episode_length = 0
        # self.x = 0
        self.board = np.array(self.create_board(), dtype=City)

        self.players = [Player(1, "player1", False), Player(2, "player2")]

        self.players[0].assign_ally(self.players[1])
        self.players[1].assign_ally(self.players[0])
        # for i in range(num_agents):
        #     players.append(Player(i+1, f"player{i+1}"))
        # players[0] = Player(1, 2, "player1")
        # players[1] = Player(2, 1, "player2")

        self.roll_val = 0

        self.current_player_index = 1
        self.current_player = self.players[self.current_player_index]

        self.current_pos = 0
        self.current_pos_owner = self.get_owner()

        # self.learnable_agents = self.players[1:]
        # self.static_agents = self.players[1:]

        observation = self.getObservation()

        # self.roll()
        # self.current_pos = (self.current_pos + self.roll_val) % self.num_states
        # self.current_player.pos = self.current_pos

        return observation, {}

    def get_owner(self):
        city = self.board[self.current_pos]
        if city.owner != None:
            return city.owner
        return None

    def action_space(self):
        return self.action_space

    def getObservation(self):
        """

        :return:
        """
        ownership = np.zeros(self.num_agents, dtype=np.float64)
        # We know the ownership of "agent 0"=Total_states - addition of all agents possessions
        # city = self.board[self.current_pos]
        for city in self.board:
            if city.owner != None:
                ownership[city.owner.num-1] += 1

        # print("ownership:" , ownership)

        # observation = np.array([self.current_player.num, self.current_pos, self.current_pos_owner,
        #                         self.current_player.money], dtype=np.float64)
        # Potential solution Normalize all observations to 0 and 1 for NN
        # Should we send city property? - Experiment and try. If the model doesn't converge,
        # then include all the possible info necessary for decision making
        # Maptlotlib visualization/rendering for monopoly.
        if self.current_pos_owner is not None:
            owner = self.current_pos_owner.num
        else:
            owner = 0
        observation = np.array([self.current_player.num, self.current_pos, owner],
                               dtype=np.float64)

        # print("observation:", observation)
        observation = np.append(observation, ownership)

        # print("observation total:", observation)
        return observation

    def roll(self):
        self.roll_val = np.random.randint(low=1, high=self.dice_size)

    def update_position_roll(self):
        self.current_player.change_pos(self.roll_val, self.num_states)

    def pay_rent(self):
        rent = self.board[self.current_pos].price
        self.current_player.money -= rent
        self.players[self.current_pos_owner-1].money += rent

    def step(self, action):

        self.roll()
        self.update_position_roll()
        self.current_pos = self.current_player.pos
        self.current_pos_owner = self.get_owner()

        observation = self.getObservation()

        self.action = self.actions[action]
        self.reward = self.get_reward()
        self.take_action()
        self.episode_length += 1

        if self.episode_length >= self.max_turns:
            self.done = False
            self.truncated = True
            return observation, self.reward, self.done, self.truncated, {"episode_length": self.episode_length}

        if self.check_monopoly(2):
            self.done = True
            return observation, self.reward, self.done, self.truncated, {"episode_length": self.episode_length}

        self.change_turn()

        return observation, self.reward, self.done, self.truncated, {"episode_length": self.episode_length}

    def change_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_agents
        self.current_player = self.players[self.current_player_index]

    def get_reward(self):
        '''
        Return value : rewards
        Input argument.
        '''
        self.reward = 0
        if self.board[self.current_player.pos].owner is None:
            if self.action == "buy":
                self.reward += 1
            elif self.action == "give":
                # Invalid action
                self.reward += -10
            else:
                # Skipping even when it can buy
                self.reward += -2

        elif self.board[self.current_player.pos].owner.num == 1:
            if self.action == "buy":
                # Trying to buy already bought land
                self.reward += -1
            elif self.action == "give":
                # Good action
                # self.reward += 0
                if self.current_player.num == 1:
                    self.reward += 3
                else:
                    self.reward -= 3
            else:
                # Skipping even when it can sell
                self.reward += -2

        else:
            if self.action == "buy":
                # Trying to buy already bought land
                self.reward += -1
            elif self.action == "give":
                # Invalid action
                self.reward += -1
            else:
                # Skipping correct action
                self.reward += 0

        if self.check_monopoly(2):
            self.reward += 5
        else:
            self.reward += -1

        return self.reward

    def check_monopoly(self, player_num):
        count = 0
        for city in self.board:
            if city.owner is not None:
                if city.owner.num == player_num:
                    count += 1
                else:
                    return False
            else:
                return False
        return True

    def take_action(self):
        if self.action == "buy":
            self.board = self.current_player.buy(self.board)

        elif self.action == "give":
            self.board = self.current_player.give(self.board)

        self.current_player.pay_rent(self.board)

    def move_static_agent(self, static_agent):
        # roll = np.random.randint(low=1, high=3)
        self.roll()
        static_agent.change_pos(self.roll_val, self.num_states)
        action_in = np.random.choice([0, 1])
        action = self.actions[action_in]

        if action == "buy":
            if int(self.board[static_agent.pos]) == 0:
                self.board[static_agent.pos] = static_agent.num
