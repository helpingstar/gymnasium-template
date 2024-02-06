from gymnasium.envs.registration import register

register(
    id="MyCustomEnv-v0",
    entry_point="gym_customenv.envs:MyCustomEnv",
)
