import gymnasium as gym
from gymnasium import spaces
import numpy as np


# Normalize the observation.
class CustomObsWrapper(gym.ObservationWrapper):
    def __init__(self, env):

        super().__init__(env)

        # observation이 바뀌면 space도 바꿔줘야 한다.
        self.observation_space = spaces.Box(
            shape=self.observation_space.shape, low=0, high=1, dtype=np.float32
        )

    def observation(self, obs):
        return obs / 10.0
