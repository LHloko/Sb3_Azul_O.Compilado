from eviroment.Env_solo1 import S_game_V3
from eviroment.Env_solo1 import Azul_solo1_env as azul
import numpy as np
import gymnasium as gym

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks

def mask_fn(env: gym.Env):
    return env.action_masks_fn()


env = azul.AzulEnv()

env = ActionMasker(env, mask_fn)

model = MaskablePPO.load('teste_01')
for i in range(5):
    obs, _ = env.reset()
    done = False
    rw = 0

    while done != True:
        action_masks = get_action_masks(env)
        #print('action_masks ',action_masks)
        action, _states = model.predict(obs, action_masks=action_masks)
        #print('action ' , action)
        obs, reward, terminated, truncated, info = env.step(action)
        #print('obs',obs)
        #print('info',info)
        #print('reward',reward)
        #print('terminated',terminated)
        #print('truncated',truncated)
        rw = reward
        done = terminated or truncated
        #input()

    print('======================')
    env.render()

'''
for _ in range(5):
    act = int(input('play ai fellas '))
    env.play_human_first(env, act)

'''

