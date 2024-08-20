"""

UGA BUGA TESTANTO O APRENDIZADO COM O NIVEL MAIS BAIXO DE ABSTRAÇAO KEKEKEK 

"""
# Criando a minha mascara de acoes
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List, Optional

# Minhas Classes
from eviroment.Env_mul.M_game_v3 import Factory_V3
from eviroment.Env_mul.M_game_v3 import State_V3
from eviroment.Env_mul.M_game_v3 import Player_V3

class AzulEnv(gym.Env):
    metadate = {"render_modes":['rgb_array','human']}

    def __init__(self, render_mode = None):
        super(AzulEnv, self).__init__()

        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fÃ¡brica
        self.players = [Player_V3.Jogador("AGNT_02"), Player_V3.Jogador("AGNT_01")]  # Instanciar o jogador
        self.dados = [self.fab, self.fab.pocket, self.players]
        self.estado = State_V3.Estados(self.dados)

        # Gym enviroment
        self.action_space = spaces.Discrete(180)
        self.observation_space = spaces.Box(low=-1, high=4, shape=(75,), dtype=int) # -1 (sem ceramica), 0:4 (ceramicas postas)
        self.render_mode = render_mode

        # Inicializar o estado do ambiente
        self.reset()

    '''
    Entrada: Vazia
    Saida: A observaçao do estado inicial do jogo 
    Inicia um jogo do zero, com a instanciaçao de cada classe e dos jogadores 
    '''
    def reset(self, seed=None, options=None):
        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fÃ¡brica
        self.players = [Player_V3.Jogador("AGNT_02"), Player_V3.Jogador("AGNT_01")]  # Instanciar o jogador
        self.truncated = False
        self.terminated = False

        # Dados iniciais do ambiente
        self.dados = [self.fab, self.fab.pocket, self.players]

        # Estado inicial do jogo
        self.estado = State_V3.Estados(self.dados)

        # Retornar a observaÃ§Ã£o inicial do ambiente
        return self.observe(), self._get_info()

    '''
    Entrada: agent
    Saida: A observaçao do ambiente (fabricas-chao_de_fabrica-tabuleiros) como 
    uma matriz.
    '''
    def observe(self, agent):
        # Obter o estado atual do jogo
        state = self.estado.get_states()

        factories       = state['fac']
        factory_floor   = state['fac-flr']
        ply_bord_01     = state['ply_01']
        ply_bord_02     = state['ply_02']

        # Processar o estado para criar as observações
        table = np.concatenate((factories, factory_floor), axis=1)

        observations = np.concatenate((table,ply_bord_01,ply_bord_02), axis = 0)

        print('observations', observations)
        return observations


    '''
    Entrada: action como uma tupla com 3 valores 
    Saida: List com 'observation, reward, terminated, truncated, info'
    Implementar lógica para executar uma ação no ambiente
    '''
    def step(self, action):
        terminated = False
        truncated = False
        reward = 0

        # Executar a ação no ambiente
        valid_move = self.players.playar(action)

        # Excede
        if  not valid_move:
            truncated = True
            reward -= 10 # Movimento invalido

        # Verificar se o turno acabou
        if self.estado.fim_de_turno():
            reward += self.players.pontuar() # Obter a recompensa do fim do turno
            # Verificar se o jogo acabou
            if self.estado.is_game_over():
                terminated = True
                reward += self.pontuar_ultimate_final()  # Obter a recompensa do fim do jogo

        # Atualizar o estado do jogo e retornar a observação, recompensa e sinalizadores de término
        observation = self.observe()
        info = self.get_info()

        return observation, reward, terminated, truncated, info


    '''
    Entrada: Vazia
    Saida: informaçao como um dict de quem e o primeiro jogador e se eh o ultimo round
    '''
    def get_info(self):
        first_player = None
        is_last_round = False

        if self.estado.fim_de_turno:
            for player in self.players:
                if player.me_have_minus_one_gd:
                    first_player = player.get_name()
                    break
    
        if self.estado.is_last_round_to_end():
            is_last_round = True

        info = {
            "first_player": first_player,
            "is_last_round": is_last_round
        }
    
        return info



#_----------------------------------------------------------------------------_

env = AzulEnv()
env.reset()
