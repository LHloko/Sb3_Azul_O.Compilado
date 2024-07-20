from typing import List, Optional
import numpy as np
from gymnasium import spaces
from stable_baselines3.common.envs import IdentityEnv
from sb3_contrib.common.wrappers import ActionMasker

from sb3_contrib import MaskablePPO
from sb3_contrib.common.envs import InvalidActionEnvMultiDiscrete
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from sb3_contrib.common.maskable.utils import get_action_masks

class CustomInvalidActionEnvMultiDiscrete(IdentityEnv[np.ndarray]):
    """
    Custom env with a multidiscrete action space that supports action masking
    based on the state of the environment.
    """
    action_space: spaces.MultiDiscrete

    def __init__(
        self,
        dims: Optional[List[int]] = None,
        ep_length: int = 100,
    ):
        if dims is None:
            dims = [6, 5, 6]

        self.dims = dims
        print('dims = ', dims)

        self.state = self._initialize_state(dims)
        print('self.state = ', self.state)

        space = spaces.MultiDiscrete(dims)

        self.possible_actions = np.arange(np.prod(dims))
        print('self.possible_actions = ', self.possible_actions)

        super().__init__(space=space, ep_length=ep_length)

    def _initialize_state(self, dims: List[int]) -> np.ndarray:
        # Inicialize o estado que representa a disponibilidade de peças
        # Para simplificar, vamos supor que cada lugar tenha inicialmente todas as cores
        return np.ones(dims, dtype=int)

    def _choose_next_state(self) -> None:
        # Atualize o estado aleatoriamente como exemplo
        # Para um ambiente real, atualize com base na lógica do seu ambiente
        self.state = self._initialize_state(self.dims)

        # Crie máscaras de ação com base no estado atual
        self.invalid_actions = self._determine_invalid_actions()

    def _determine_invalid_actions(self) -> List[int]:
        invalid_actions = []
        
        # Verifique locais de seleção inválidos
        for i in range(self.state.shape[0]):
            if not np.any(self.state[i, :, :]):
                invalid_actions.append(i)
        
        # Verifique cores inválidas em cada local de seleção
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if not np.any(self.state[i, j, :]):
                    invalid_actions.append(self.state.shape[0] + j)
        
        # Verifique locais inválidos
        for i in range(self.state.shape[2]):
            if not self._can_place(i):
                invalid_actions.append(self.state.shape[0] + self.state.shape[1] + i)
    
        return invalid_actions

    def _can_place(self, location_index: int) -> bool:
        # Exemplo de lógica para determinar se uma peça pode ser colocada em um local
        # Modifique de acordo com as regras do seu ambiente
        return True  # Substitua pela lógica real

    def action_masks(self) -> List[bool]:
        return [action not in self.invalid_actions for action in self.possible_actions]

    def step(self, action):
        # Atualize o estado com base na ação realizada
        place_idx, color_idx, pick_idx = action
        self.state[place_idx, color_idx] -= 1
        self.state[pick_idx, color_idx] += 1

        # Calcule recompensa, conclusão, informações (de acordo com a lógica do seu ambiente)
        reward = 0  # Example reward
        done = False  # Example termination condition
        info = {}

        self._choose_next_state()

        return self.state, reward, done, info

env = CustomInvalidActionEnvMultiDiscrete([6, 5, 6], 100)
print(get_action_masks(env))

