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

env = MonopolyEnv2(4, 2, 2, 200, './city1.csv')
env.reset()

model = PPO('MlpPolicy', env, verbose=0, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0

# We can control the number of episodes we want to run
# while iters < 2:
while True:
    iters += 1
    # We can either put env.reset here not; produced same results. But on safer side, we should put
    env.reset()
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS * iters}")

    # This is for debug, as I turned the verbose=0 because it was too verbose. This is better.
    # Potential can do TQDM
    print(f"env.episode_length {env.episode_length}")

###### RUN THE BELOW CODE IN CMD FOR PROGRESS GRAPHS #######
# tensorboard --logdir=logs
