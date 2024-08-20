from eviroment.Env_solo1 import S_game_V3
from eviroment.Env_solo1 import Azul_solo1_env as azul
import numpy as np
import gymnasium as gym

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.maskable.utils import get_action_masks
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

def mask_fn(env: gym.Env):
    return env.action_masks_fn()


env = azul.AzulEnv()

env = ActionMasker(env, mask_fn)

model = MaskablePPO(
    policy = MaskableActorCriticPolicy,
    env = env,
    learning_rate=0.00008,
    n_epochs=3,
    gamma=0.97,
    ent_coef=0.003,
    vf_coef=0.5,
    max_grad_norm=0.5,
    rollout_buffer_class=None,
    rollout_buffer_kwargs=None,
    target_kl=None,
    stats_window_size=100,
    tensorboard_log="Azul_Solo_01",
    verbose=0,
    )

model.learn(total_timesteps=50000000,
            progress_bar=True,
            tb_log_name="ec-0_003|lr-0_00008|g-0_97|ne-3",
            reset_num_timesteps=True)

model.save("teste_001")

print("Model has been saved.")

