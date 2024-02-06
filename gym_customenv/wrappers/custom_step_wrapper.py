import gymnasium as gym


class CustomStepWrapper(gym.Wrapper):
    def __init__(self, env, log=True, goal_bonus=0):
        super().__init__(env)
        # 초기화

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        # 내 나름대로 엔진 수정

        return obs, reward, terminated, truncated, info
