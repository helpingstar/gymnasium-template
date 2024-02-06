import gymnasium as gym
from typing import TYPE_CHECKING, Any, Generic, SupportsFloat, TypeVar, Optional
import pygame

import numpy as np

ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")
RenderFrame = TypeVar("RenderFrame")


class MyCustomEnv(gym.Env):
    metadata = {
        # ansi : 터미널을 이용한 렌더링, 문자 프린팅
        # rgb_array : 화면 녹화시 사용
        # human : 실시간 모니터링을 위해 사용 : 느림
        "render_modes": ["ansi", "rgb_array", "human"],
        "render_fps": 10,
    }

    def __init__(self, render_mode=None):
        """
        환경이 다시 만들어져도 절대 바뀌지 않는 정보를 초기화 합니다.
        """

        # 인수들이 제대로 주어졌는지 확인합니다.
        err_msg = f"{render_mode} is not in {self.metadata['render_modes']}"
        assert (
            render_mode is None or render_mode in self.metadata["render_modes"]
        ), err_msg
        # assert 다른 인수 검사

        self.render_mode = render_mode

        # Space 초기화
        self.observation_space: gym.spaces
        self.action_space: gym.spaces

        # 게임 상태에 관계없이 유지되는 정보 초기화
        # ex) 바둑판의 격자 개수

        # 렌더링을 위한 요소들 초기화
        self.window = None
        self.clock = None

    def reset(self, *, seed=None, options=None):
        """
        게임이 새로 시작될 때 바뀌는 요소들을 초기화합니다.
        """
        super().reset(seed=seed)

        # 게임이 초기화될 때마다 바뀌는 요소
        # ex) 바둑에서 바둑판을 깨끗하게 한다, 체스에서 말들을 원위치 한다.
        #     점수를 0으로 만든다 등

        # reset과 step에서는 self.render()이 마지막에 와야 한다.
        # 안그러면 내부 알고리즘의 처리되기 전의 그림이 렌더링된다.
        if self.render_mode == "human":
            self.render()

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

        # return self._get_obs(), self._get_info()

    def _get_info(self):
        """
        게임의 추가 정보를 제공한다, obs에 넣을 수는 없지만 디버깅에 좋은 요소를 주로 넣는다.
        ex) 뱀의 길이, 목표까지의 거리, 현재까지의 누적점수
        """
        info: Any
        return info

    def _get_obs(self):
        """
        게임의 각 요소를 concatenate 혹은 stack 등으로 가공해서 리턴한다.
        """
        obs: Any
        return obs

    def step(self, action):
        """
        사실상 게임의 엔진이라고 생각하면 됩니다. 인자로 들어온 action을 기반으로 다음 상태를 계산하고 리턴합니다.
        """
        # 보통 턴제 기반의 게임의 경우 illgeal action의 경우 assert로 환경을 종료합니다.
        assert self.action_space.contains(action)

        """
        게임의 엔진
        
        해당 행동이 취해지면 게임이 끝나는가?
        게임이 끝나지 않는다면 다음 상태는?
        """

        # reset과 step에서는 self.render()이 마지막에 와야 한다.
        # 안그러면 내부 알고리즘의 처리되기 전의 그림이 렌더링된다.
        if self.render_mode == "human":
            self.render()

        return

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        if self.render_mode == "ansi":
            self._render_text()
        else:  # self.render_mode in {"human", "rgb_array"}:
            return self._render_gui(self.render_mode)

    def _render_text(self):
        """
        observation이 terminal에 바로 출력되도록 한다.
        카드 게임류를 제외하고는 거의 쓰지 않는다.
        """

        # observation을 출력한다. StringIO를 주로 쓴다.

        return None

    def _render_gui(self, mode: str):
        pygame.font.init()
        # gui 렌더링 시 처음 초기화되고 그 뒤로는 None이 아니기 때문에 접근하지 않는다.
        if self.window is None:
            pygame.init()
            # render_mode 가 gui일 경우 렌더링 측면에서 초기화 해야 할 요소들을 초기화한다.
            # ex) 격자의 한칸의 크기, 화면의 크기 등

            if mode == "human":
                pygame.display.init()
                self.window = pygame.display.set_mode(
                    (self.window_size, self.window_size)
                )
            elif mode == "rgb_array":
                self.window = pygame.Surface((self.window_size, self.window_size))

        if self.clock is None:
            self.clock = pygame.time.Clock()

        ##### Surface에 draw, blit을 통해 렌더링 작업을 진행한다.#####
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((0, 0, 0))

        #########################################################

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
