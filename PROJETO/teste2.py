# Criando a minha mascara de açoes

import copy
import gymnasium as gym
from gymnasium import spaces
import numpy as np

# Minhas Classes
from eviroment.Env_solo.S_game_V3 import Factory_V3
from eviroment.Env_solo.S_game_V3 import State_V3
from eviroment.Env_solo.S_game_V3 import Player_V3

# Sb3 Contrib
from sb3_contrib.ppo_mask import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks
from typing import List, Optional
from stable_baselines3.common.envs import IdentityEnv

class AzulEnv(gym.Env):
    metadate = {"render_modes":['rgb_array','human']}

    def __init__(self, render_mode = None):
        super(AzulEnv, self).__init__()

        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fábrica
        self.players = [Player_V3.Jogador("AGNT")]  # Instanciar o jogador
        self.dados = [self.fab, self.fab.pocket, self.players]
        self.estado = State_V3.Estados(self.dados)

        # Gym enviroment
        self.action_space = spaces.MultiDiscrete([6,4,6])
        self.observation_space = spaces.Box(low=-1, high=4, shape=(75,), dtype=int) # -1 (sem ceramica), 0:4 (ceramicas postas)
        self.render_mode = render_mode

        # Sb3
        #self.legal_moves = self.get_mask_action()

        # Inicializar o estado do ambiente
        self.reset()

    '''
    Entrada: Vazia
    Saida: A observaçao do estado inicial do jogo 
    Inicia um jogo do zero, com a instanciaçao de cada classe e dos jogadores 
    '''
    def reset(self, seed=None, options=None):
        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fábrica
        self.players = [Player_V3.Jogador("AGNT")]  # Instanciar os jogadores =+= , Jogador.Jogador("VK")
        self.truncated = False
        self.terminated = False

        # Dados iniciais do ambiente
        self.dados = [self.fab, self.fab.pocket, self.players]

        # Estado inicial do jogo
        self.estado = State_V3.Estados(self.dados)

        # Retornar a observação inicial do ambiente
        return self.observe(), self._get_info()

    '''
    Entrada: action como uma tupla com 3 valores 
    Saida: List com 'observation, reward, terminated, truncated, info'
    Implementar lógica para executar uma ação no ambiente
    '''
    def step(self, action):
        reward = 0
        jogada = list(action)

        # Executar a ação no ambiente
        self.players[0].playar(self.fab ,jogada)
        self.render() if self.render_mode=='human' else None

        # Verificar se o turno acabou
        if self.estado.fim_de_turno():
            reward += self.players[0].pontuar() # Obter a recompensa do fim do turno
            # Verificar se o jogo acabou
            if self.estado.is_game_over():
                self.terminated = True
                reward += self.estado.fim_de_jogo()  # Obter a recompensa do fim do jogo
            # senao, reinicia o ambiente
            else:
                self.estado.iniciar_turno()

        # Recompensa imediata
        # ???
        if action[2] < 5:
            reward += 1
        else:
            reward -= 1

        # Atualizar o estado do jogo e retornar a observação, recompensa e sinalizadores de término
        observation = self.observe()
        info = self._get_info()

        return observation, reward, self.terminated, self.truncated, info

    '''
    Entrada: agent
    Saida: A observaçao do ambiente (fabricas-chao_de_fabrica-tabuleiros) como 
    uma matriz.
    '''
    def observe(self):
        # Obter o estado atual do jogo
        state = self.estado.get_states()

        factories       = state['fac']
        factory_floor   = state['fac-flr']
        ply_bord_01     = state['ply_01']

        # Processar o estado para criar as observações
        table = np.concatenate((factories, factory_floor, ply_bord_01))

        observations = np.array(table)

        return observations


    '''
    Entrada: Vazia
    Saida: informaçao como um dict de quem e o primeiro jogador e se eh o ultimo round
    '''
    def _get_info(self):
        is_last_round = False

        if self.estado.is_last_round_to_end():
            is_last_round = True

        info = {
            "is_last_round": is_last_round
        }
    
        return info

    '''
    Entrada: Vazia 
    Saida: O jogo rederizado 
    '''
    def render(self):
        if self.render_mode == "human":
            self.estado.game_player_status()
        pass

    # ???
    def get_mask_action(self):
        pass

# =========================================================================== #
    def _pre_process_board(self):
        lines  = self.estado.get_states()['ply_01']

        lns = []
        idx = 0
        for i in range(5):
            l = []
            for j in range(i+1):
                l.append(lines[idx])
                idx+=1
            lns.append(l)

        return lns

    def _pre_process_fabs(self):
        state = self.estado.get_states()
        factories = state['fac']
        #print('fabricas: ', factories)
        facs = []

        for i in range(5):
            f = []
            for j in range(4):
                f.append(factories[i*4 + j])
            facs.append(f)

        floor = state['fac-flr']
        #print('piso: ', floor)

        fl = []
        for i in floor:
            if i != -1:
                fl.append(i)
        facs.append(fl)

        return facs

    def _valid_fabricas(self):
        state = self.estado.get_states()
        factories   = state['fac']
        floor       = state['fac-flr']

        facs = []
        idx = 0
        for i in range(0, 20, 4):
            if factories[i] != -1:
                facs.append(idx)
            else:
                facs.append(-1)
            idx += 1

        facs.append(-1) if floor[0] == -1 else facs.append(5)

        return facs

    def _valid_cores(self):
        state = self._valid_fabricas()
        state = [valid for valid in state if valid != -1] # comprime para so validos

        fabs = self._pre_process_fabs()

        facAndColor = []

        for i in state:
            for j in fabs[i]:
                facAndColor.append([i,j])

        return facAndColor

    def _valid_linha(self):
        states = self._valid_cores()
        #meter sempre o piso do tab com opcao + SEMPRE + 'SONS DE TROVAO'
        lines  = self._pre_process_board()

        # maracutaia
        lines[0] = [2]
        lines[1] = [1,-1]
        lines[2] = [2,2,-1]
        lines[3] = [-1,-1,-1,-1]
        lines[4] = [4,4,4,-1,-1]



        valid_play = []

        # Adicionando o piso como uma opcao
        for f_c in states:
            stp = f_c.copy()
            stp.append(5)
            if stp not in valid_play:
                valid_play.append(stp)


        # Pega o indice das linhas vazias
        empty = [i for i, sublista in enumerate(lines) if all(x == -1 for x in sublista)]

        # Cria açoes possiveis com as linhas vazias
        for i in states:
            for j in empty:
                stp = i.copy()
                stp.append(j)
                if stp not in valid_play:
                    valid_play.append(stp)

        # Pega o indice das linhas parcialmente cheias
        parcel_empty = [i for i, sublista in enumerate(lines) if any(x == -1 for x in sublista) and not all(x == -1 for x in sublista)]

        # Cria açoes possiveis com as linhas vazias parcialmente cheias
        for f_c in states:
            cor = f_c[1]
            for parcel in parcel_empty:
                color_line = lines[parcel][0]
                if color_line == cor:
                    stp = f_c.copy()
                    stp.append(parcel)
                    valid_play.append(stp)

        return valid_play

#==============================================================================

# Exemplo de uso:
env = AzulEnv()
fabs = env._valid_fabricas()
pre_fabs = env._pre_process_fabs()
pre_bd = env._pre_process_board()
f_c = env._valid_cores()
f_c_l = env._valid_linha()
print(f_c_l)













































'''
# Crie uma instância do ambiente personalizado
env = AzulEnv('human')

# Reinicie o ambiente
observation, info = env.reset()

print(observation)
print(info)


# Execute uma ação aleatória no ambiente

#action = env.action_space.sample()
#observation, reward, terminated, truncated, info = env.step(action)

terminated = False
while terminated != True:
    a = int(input())
    b = int(input())
    c = int(input())

    if a == 10:
        break

    action = [a,b,c]
    print(action)
    
    observation, reward, terminated, truncated, info = env.step(action)
    env._get_fabs_pre_process()


# Imprima informações sobre o passo atual
print("Observation:\n", observation)
print("Reward:", reward)
print("truncated:", truncated)
print("terminated:", terminated)
print("Info:", info)
   #

for step in range(max_steps):
# Execute uma ação aleatória no ambiente
action = env.action_space.sample()
print(action)
observation, reward, terminated, truncated, info = env.step(action)

# Imprima informações sobre o passo atual
print("Observation:\n", observation)
print("Reward:", reward)
print("truncated:", truncated)
print("terminated:", terminated)
print("Info:", info)

# Verifique se o episódio terminou
if truncated or terminated:
    print("Episode finished after {} steps".format(step+1))
    env.reset()

'''


