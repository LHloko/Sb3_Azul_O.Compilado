from typing import List, Optional
import numpy as np
from gymnasium import spaces
from stable_baselines3.common.envs import IdentityEnv
from sb3_contrib.common.wrappers import ActionMasker

from sb3_contrib import MaskablePPO
from sb3_contrib.common.envs import InvalidActionEnvMultiDiscrete
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from sb3_contrib.common.maskable.utils import get_action_masks

from eviroment.Env_solo import S_game_V3
from eviroment.Env_solo import Azul_solo_env as azul

class InvalidActionEnvMultiDiscrete(IdentityEnv[np.ndarray]):
    """
    Identity env with a multidiscrete action space. Supports action masking.
    """

    action_space: spaces.MultiDiscrete

    def __init__(
        self,
        dims: Optional[List[int]] = None,
        ep_length: int = 100,
        n_invalid_actions: int = 0,
    ):
        if dims is None:
            dims = [6,5,6]

        if n_invalid_actions > sum(dims) - len(dims):
            raise ValueError(f"Cannot find a valid action for each dim. Set n_invalid_actions <= {sum(dims) - len(dims)}")

        space = spaces.MultiDiscrete(dims)
        self.n_invalid_actions = n_invalid_actions
        self.possible_actions = np.arange(sum(dims))
        self.invalid_actions: List[int] = []
        super().__init__(space=space, ep_length=ep_length)

    def _choose_next_state(self) -> None:
        self.state = self.action_space.sample()

        converted_state: List[int] = []
        running_total = 0
        for i in range(len(self.action_space.nvec)):
            converted_state.append(running_total + self.state[i])
            running_total += self.action_space.nvec[i]

        # Randomly choose invalid actions that are not the current state
        potential_invalid_actions = [i for i in self.possible_actions if i not in converted_state]
        self.invalid_actions = np.random.choice(potential_invalid_actions, self.n_invalid_actions, replace=False).tolist()

    def action_masks(self) -> List[bool]:
        return [action not in self.invalid_actions for action in self.possible_actions]
