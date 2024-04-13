from stable_baselines3 import PPO, A2C, DQN
import os
from monopoly.envs.monopoly_env2 import MonopolyEnv2
import time

models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = MonopolyEnv2(5, 6, 2, 1000)
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
iters = 0
while True:
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS * iters}")

###### RUN THE BELOW CODE IN CMD FOR PROGRESS GRAPHS #######
# tensorboard --logdir=logs
