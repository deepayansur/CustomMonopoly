from gym.envs.registration import register

register(
    id="monopoly",
    entry_point="gym_example.envs:MonopolyEnv",
)
