from stable_baselines3 import PPO, A2C, DQN
import os
from monopoly.envs.monopoly_env2 import MonopolyEnv2
import time

models_dir = f"models/{int(time.time())}/"
logdir = f"logs_mihir/{int(time.time())}/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = MonopolyEnv2(12, 6, 2, 200, './city.csv')
env.reset()

model = PPO('MlpPolicy', env, verbose=0, tensorboard_log=logdir)

TIMESTEPS = 1000
iters = 0
episodes_we_want = 10

# We can control the number of episodes we want to run
# while iters < 2:
position_list = [0,0]
file_path = "ownership_data.txt"
with open(file_path, 'w') as file:
    file.write("")
while True:
    iters += 1
    # We can either put env.reset here not; produced same results. But on safer side, we should put
    env.reset()
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS * iters}")
    print

    # This is for debug, as I turned the verbose=0 because it was too verbose. This is better.
    # Potential can do TQDM
    print(f"env.episode_length {env.episode_length}")
    if env.episode_length < 50:
        print(f"Episode")
        print(f"Current_player: {env.current_player.num}")
        print(f"Position before roll: {env.current_player.pos}")
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
        print("OWNER:",owner)
        print(worths)
        owner_tuple = [(location, value) for location, value in owner]
        position_list[env.current_player.num-1] = env.current_pos
        with open(file_path, 'a') as file:
            file.write(str(owner_tuple)+"\n")
            file.write(str(env.current_player.num)+"\n")
            file.write(str(env.roll_val)+"\n")
            file.write(str(env.actions[random_action])+"\n")
            file.write(str(position_list)+"\n")
        break

###### RUN THE BELOW CODE IN CMD FOR PROGRESS GRAPHS #######
# tensorboard --logdir=logs
