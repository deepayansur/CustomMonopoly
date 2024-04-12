import gymnasium as gym
from gymnasium import spaces
# from gymnasium.spaces import Box
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
class Player:
    def __init__(self, num, ally_num, tag="player1", static=False):
        self.tag = tag
        self.pos = 0
        self.num = num
        self.ally_num = ally_num
        self.prev_pos = []
        self.possession_indices = []
        self.isStatic = static

    def change_pos(self, roll_dice, num_states):
        self.pos = (self.pos + roll_dice) % num_states

    def buy(self, board):
        self.possession_indices.append(self.pos)
        board[self.pos] = self.num
        return board

    def sell(self, board, p2_num):
        if self.pos in self.possession_indices:
            self.possession_indices.remove(self.pos)
            board[self.pos] = p2_num
        else:
            pass
        return board



class MonopolyEnv2(gym.Env):
    def __init__(self, num_states,dice_size, num_agents=2, max_turns=100):
        self.static_agents = None
        self.actions = ["skip", "buy", "give"]
        self.action = None
        self.reward = 0
        self.action_space = spaces.Discrete(3)
        self.done = False
        self.truncated = False
        self.dice_size = dice_size
        self.episode_length = 0
        # self.no_operation = False
        self.players = [Player(1, 2, "player1", False), Player(2, 1, "player2")]
        self.roll_val = 0
        self.current_player_index = 1
        self.current_pos = 0
        self.current_pos_owner = 0
        self.current_player = self.players[self.current_player_index]
        self.num_states = num_states
        self.num_agents = num_agents
        self.board = np.zeros(self.num_states)
        # self.state_observation = [0, self.board]
        self.max_turns = max_turns
        dim = 3 + self.num_agents  #3 = agent_nos,cur_pos,cur_pos_owner
        self.observation_space = spaces.Box(low=0, high=max(num_states, num_agents, dice_size),
                                            shape=(dim,), dtype=np.float64)
        self.roll()

    def reset(self, seed=None, options=None):
        self.done = False
        self.truncated = False
        self.episode_length = 0
        # self.x = 0
        self.board = np.zeros(self.num_states)

        self.players = [Player(1, 2, "player1"), Player(2, 1, "player2")]
        # for i in range(num_agents):
        #     players.append(Player(i+1, f"player{i+1}"))
        # players[0] = Player(1, 2, "player1")
        # players[1] = Player(2, 1, "player2")

        self.roll_val = 0
        self.current_player_index = 1
        self.current_pos_owner = 0
        self.current_pos = 0
        self.current_player = self.players[self.current_player_index]

        # self.learnable_agents = self.players[1:]
        self.static_agents = self.players[1:]

        # self.state_observation = [self.x, self.board]
        # self.state_observation = [self.current_player.pos, self.board]
        # observation = np.array([self.current_pos, self.current_pos_owner]# ,self.roll_val]
        #                       , dtype=np.float64)

        observation = self.getObservaton()

        # print(observation.dtype)
        self.roll()
        self.current_pos = (self.current_pos + self.roll_val) % self.num_states
        self.current_player.pos = self.current_pos
        self.current_pos_owner = self.board[self.current_pos]
        return observation,{}

    def action_space(self):
        return self.action_space

    def getObservaton(self):
        """

        :return:
        """
        ownership = np.zeros(self.num_agents,dtype=np.float64)
        # We know the ownership of "agent 0"
        for x in range(self.num_agents):
            ownership[x] = list(self.board).count(x+1)

        print("ownership:" , ownership)

        observation = np.array([self.current_player.num, self.current_pos, self.current_pos_owner]# ,self.roll_val]
                              , dtype=np.float64)

        # print("observation:", observation)
        observation = np.append(observation, ownership)

        # print("observation total:", observation)
        return observation

    def roll(self):
        self.roll_val = np.random.randint(low=1, high=self.dice_size)

    def update_position_roll(self):
        self.current_player.change_pos(self.roll_val, self.num_states)
        # self.x = (self.x + roll) % self.num_states
        # return [self.x, self.board]
        # return [self.current_player.pos, self.board]

    def step(self, action):
        # observation = np.array([self.current_pos, self.current_pos_owner])#, self.roll_val])
        observation = self.getObservaton()
        self.current_player.pos = self.current_pos
        # self.current_player_index = 0
        # self.current_pos_owner = 0
        if self.episode_length > self.max_turns:
            self.done = False
            self.truncated = True
            # self.no_operation = True
            return observation, self.reward, self.done, self.truncated , {"episode_length": self.episode_length}

        if np.all(self.board == 2):
            self.done = True
            # self.no_operation = True
            return observation, self.reward, self.done,self.truncated , {"episode_length": self.episode_length}

        self.action = self.actions[action]
        # self.action = self.actions[action]
        self.reward = self.get_reward()
        self.take_action()
        self.episode_length += 1
        # self.no_operation = False

        if self.episode_length >= self.max_turns:
            self.done = True

        # for static_agent in self.static_agents:
        #     self.move_static_agent(static_agent)

        self.current_player_index = (self.current_player_index+1) % self.num_agents
        self.current_player = self.players[self.current_player_index]

        self.roll()
        # self.current_pos = (self.current_pos + self.roll_val) % self.num_states
        self.update_position_roll()
        self.current_pos = self.current_player.pos
        self.current_pos_owner = self.board[self.current_pos]


        # print("episode_length:" + str(self.episode_length))
        # self.current_player_index = (self.current_player_index + 1)%self.num_states
        return observation, self.reward, self.done,self.truncated , {"episode_length": self.episode_length}

    def get_reward(self):
        '''
        Return value : rewards
        Input argument.
        '''
        self.reward = 0
        if self.board[self.current_player.pos] == 0:
            if self.action == "buy":
                self.reward += 1
            elif self.action == "give":
                # Invalid action
                self.reward += -10
            else:
                # Skipping even when it can buy
                self.reward += -2

        elif self.board[self.current_player.pos] == 1:
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

        if np.all(self.board == 2):
            self.reward += 5
        else:
            self.reward += -1

        return self.reward

    def take_action(self):
        if self.action == "buy":
            if int(self.board[self.current_player.pos]) == 0:
                self.board[self.current_player.pos] = self.current_player.num
            # else:
            #     print(str(self.board[self.current_player.pos]) + " already owned by different player, cant BUY")

        elif self.action == "give":
            if int(self.board[self.current_player.pos]) == self.current_player.num:
                self.board[self.current_player.pos] = self.current_player.ally_num
            # else:
            #     print(str(self.board[self.current_player.pos]) + " is not owned by current player, cant GIVE")

        # return [self.current_player.pos, self.board]

    def move_static_agent(self, static_agent):
        # roll = np.random.randint(low=1, high=3)
        self.roll()
        static_agent.change_pos(self.roll_val, self.num_states)
        action_in = np.random.choice([0, 1])
        action = self.actions[action_in]

        if action == "buy":
            if int(self.board[static_agent.pos]) == 0:
                self.board[static_agent.pos] = static_agent.num