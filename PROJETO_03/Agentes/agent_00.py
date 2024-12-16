from Ambiente import M_game_v3
from Enviroment import Env as azul
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
    policy=MaskableActorCriticPolicy,
    env=env,
    learning_rate=0.0003,          # Taxa de aprendizado ajustada (mais alta para início rápido)
    n_epochs=10,                   # Mais épocas para aproveitar melhor cada batch
    gamma=0.99,                    # Maior retenção de longo prazo (melhor para jogos estratégicos)
    ent_coef=0.01,                 # Penalidade de entropia para melhor exploração inicial
    vf_coef=0.4,                   # Ajuste menor na perda da função de valor
    max_grad_norm=0.9,             # Gradiente maior para lidar com updates maiores
    gae_lambda=0.95,               # Reduz viés no GAE (Generalized Advantage Estimation)
    clip_range=0.2,                # Região de clipping da PPO para estabilidade
    batch_size=256,                # Aumentado para processar mais amostras por vez
    n_steps=2048,                  # Maior número de passos por atualização
    target_kl=0.03,                # Parar aprendizado se a divergência for alta
    stats_window_size=200,         # Janela maior para análise de estatísticas
    tensorboard_log="Azul_Duo_v3", # Nome do log para melhor monitoramento
    verbose=0,                     # Mantém saída detalhada
)

model.learn(total_timesteps=5000,
            progress_bar=True,
            tb_log_name="testando",
            reset_num_timesteps=True)

model.save("Azul_Mult_PPO_00")

print("Model has been saved.")