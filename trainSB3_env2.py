from stable_baselines3 import PPO, A2C, DQN
import os
from monopoly.envs.monopoly_env2 import MonopolyEnv2
import time

num_states = 4
max_turns = 200

models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/{num_states}_{max_turns}/"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = MonopolyEnv2(num_states, 6, 2, max_turns)
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir, device="cuda")

TIMESTEPS = 10000
iters = 0
while True:
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS * iters}")

###### RUN THE BELOW CODE IN CMD FOR PROGRESS GRAPHS #######
# tensorboard --logdir=logs
