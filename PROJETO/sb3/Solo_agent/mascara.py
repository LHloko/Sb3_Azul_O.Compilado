from typing import List, Optional

import numpy as np
from gymnasium import spaces
from stable_baselines3.common.envs import IdentityEnv


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
            dims = [1, 1]

        if n_invalid_actions > sum(dims) - len(dims):
            raise ValueError(f"Cannot find a valid action for each dim. Set n_invalid_actions <= {sum(dims) - len(dims)}")

        space = spaces.MultiDiscrete(dims)
        print(space)
        self.n_invalid_actions = n_invalid_actions
        print(self.n_invalid_actions)
        self.possible_actions = np.arange(sum(dims))
        print(self.possible_actions)
        self.invalid_actions: List[int] = []
        print(self.invalid_actions)

        super().__init__(space=space, ep_length=ep_length)

    def _choose_next_state(self) -> None:
        self.state = self.action_space.sample()
        print(self.state)

        converted_state: List[int] = []
        running_total = 0
        for i in range(len(self.action_space.nvec)):
            converted_state.append(running_total + self.state[i])
            running_total += self.action_space.nvec[i]

        print(converted_state)

        # Randomly choose invalid actions that are not the current state
        potential_invalid_actions = [i for i in self.possible_actions if i not in converted_state]
        print(potential_invalid_actions)

        self.invalid_actions = np.random.choice(potential_invalid_actions, self.n_invalid_actions, replace=False).tolist()
        print(self.invalid_actions)

    def action_masks(self) -> List[bool]:
        return [action not in self.invalid_actions for action in self.possible_actions]

env = InvalidActionEnvMultiDiscrete([6,5,6])
env._choose_next_state()
print(env.action_masks())


