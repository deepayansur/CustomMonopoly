from stable_baselines3 import PPO
import os
from monopoly.envs.monopoly_env2 import MonopolyEnv2
import time

models_dir = "models/"  # Update this path to the directory where your models are saved

env = MonopolyEnv2(12, 6, 2, 1000, './city.csv')
env.reset()

# Load the saved model
model_name = "470000.zip"
model = PPO.load(os.path.join(models_dir, model_name), env)

# Run inference
for _ in range(1):  # Adjust the number of episodes you want to run inference on
    obs, _ = env.reset()
    done = False
    trunc = False
    # while not done:
    #     action, _ = model.predict(obs, deterministic=True)
    #     obs, reward, done, _, _ = env.step(action)
    position_list = [0,0]
    file_path = "ownership_data.txt"
    with open(file_path, 'w') as file:
        file.write("")
    while not done: # not done:
        if trunc == True:
            print(f"Episode failed")
            break
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
            if city.owner != None:
                owner_num = city.owner.num
            else:
                owner_num = 0
            owner.append([city.name, owner_num])
        for player in env.players:
            worths.append([player.num, player.money])
        print(owner)
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
    print(f"Episode reward: {env.reward}, Episode length: {env.episode_length}")
