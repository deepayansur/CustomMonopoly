import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from monopoly.envs.monopoly_env2 import MonopolyEnv2

env = MonopolyEnv2(12, 6, 2, 200)

######################### RUN THIS TO CHECK ENV #######################

# from stable_baselines3.common.env_checker import check_env
#
# check_env(env, warn=True)
#
# # if check_env(agent, warn=True):
# print("Hell yeah!")

#########################################################################

######################### RUN FOR DRY RUN ###############################


episodes = 1

for episode in range(episodes):
    done = False
    obs = env.reset()
    position_list = [0,0]
    file_path = "ownership_data.txt"
    with open(file_path, 'w') as file:
        file.write("")
    while not done:  # not done:
        print(f"Current_player: {env.current_player.num}")
        print(f"Position before roll: {env.current_player.pos}")
        random_action = env.action_space.sample()
        print("action", random_action)

        obs, reward, done, trunc, info = env.step(random_action)
        print(f"Roll: {env.roll_val}")
        print(f"Position after roll: {env.current_pos}")
        # if reward != 0.:
        print('state', [format(num, '.2f') for num in obs])
        print('reward', reward)
        print(info)
        owner = []
        worths = []
        for city in env.board:
            owner.append([city.name, city.owner])
        for player in env.players:
            worths.append([player.num, player.money])
        print("OWNER:",owner)
        print(worths)
        print()
        
        owner_tuple = [(location, value) for location, value in owner]
        position_list[env.current_player.num-1] = env.current_pos
        with open(file_path, 'a') as file:
            file.write(str(owner_tuple)+"\n")
            file.write(str(env.current_player.num)+"\n")
            file.write(str(env.roll_val)+"\n")
            file.write(str(env.actions[random_action])+"\n")
            file.write(str(position_list)+"\n")
        if trunc:
            done = True


########################################################################

# from stable_baselines3 import PPO, A2C, DQN
# from stable_baselines3.common.env_util import make_vec_env
#
# # Instantiate the env
# vec_env = make_vec_env(MonopolyEnv, n_envs=1, env_kwargs=dict(num_states=2,num_agents=2,max_turns=200))
# # Train the agent
# model = PPO("MlpPolicy", agent, verbose=1).learn(5000)
# # Test the trained agent
# # using the vecenv
# obs = vec_env.reset()
# n_steps = 200
# for step in range(n_steps):
#     action, _ = model.predict(obs, deterministic=True)
#     print(f"Step {step + 1}")
#     print("Action: ", action)
#     obs, reward, done, info = vec_env.step(action)
#     print("obs=", obs, "reward=", reward, "done=", done)
#     vec_env.render()
#     if done:
#         # Note that the VecEnv resets automatically
#         # when a done signal is encountered
#         print("Goal reached!", "reward=", reward)
#         break
#
#
#
#
# print("done")
# # else:
#     print("oh Shit! here we go again!")
