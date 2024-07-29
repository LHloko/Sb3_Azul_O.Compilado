from eviroment.Env_solo import S_game_V3
from eviroment.Env_solo import Azul_solo_env as azul
import numpy as np
import gymnasium as gym

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.maskable.utils import get_action_masks
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

def mask_fn(env: gym.Env):
    return env.action_masks_fn()


env = azul.AzulEnv('human')

env = ActionMasker(env, mask_fn)

model = MaskablePPO(
    policy = MaskableActorCriticPolicy,
    env = env,
    learning_rate=0.0003,
    gamma=0.99,
    ent_coef=0.005,
    vf_coef=0.5,
    max_grad_norm=0.5,
    rollout_buffer_class=None,
    rollout_buffer_kwargs=None,
    target_kl=None,
    stats_window_size=100,
    tensorboard_log="---",
    verbose=1,
    )

model.learn(total_timesteps=10,
            progress_bar=False,
            tb_log_name="---",
            reset_num_timesteps=False)

model.save("---")

print("Model has been saved.")

