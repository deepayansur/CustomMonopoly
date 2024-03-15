import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from monopoly.envs.monopoly_env import MonopolyEnv

agent = MonopolyEnv(2, 2, 200)
from stable_baselines3.common.env_checker import check_env
check_env(agent, warn=True)