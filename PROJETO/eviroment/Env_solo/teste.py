import gymnasium as gym
from gymnasium import spaces
import numpy as np

# Minhas Classes
from S_game_V3 import Factory_V3
from S_game_V3 import State_V3
from S_game_V3 import Player_V3

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

    '''
    Entrada: Vazia 
    Saida: O jogo rederizado 
    '''
    def render(self):
        if self.render_mode == "human":
            self.estado.game_player_status()
        pass

    def get_mask_action(self):
        pass

# =========================================================================== #
    '''
    Para construir uma mascara de açao que impeça jogadas invalidas eu preciso 
    me atentar para os seguintes casos: 
        1- nao posso pegar de fabricas vazias, isto eh, no primeiro elemento da
           tupla preciso que sejam retiradas as fabricas vazias 

        2- nao posso selecionar uma cor que nao exista na fabrica escolhida 

        3- nao posso colocar ceramicas em linhas que elas ja existam 

    Talvez eu deva fazer uma funçao que gere todas as possibilidades de jogada 
    por exemplo se tenho 2 fabricas e o chao de fabrica 

    1 - [0,0,2,2] 
    3 - [0,1,0,4] 

    5 - [0,0,1,2,3,4]

    entao eu gero os primeiro possiveis valores [1,3,5]

    Com base nisso eu tenho agora os conjuntos de pseudo açoes possiveis 
    [1,0,0]
    [1,0,1]
    [1,0,2]
    [1,0,3]
    [1,0,4]
    [1,0,5]

    [1,2,0]
    [1,2,1]
    [1,2,2]
    [1,2,3]
    [1,2,4]
    [1,2,5]
    
    ... 

    Depois eu preciso retirar desse conjunto aqueles onde o tabuleiro ja esta 
    preenchido ou tem outras ceramicas na linhas 

    '''

    #
    def _get_fabs_pre_process(self):
        state = self.estado.get_states()
        factories   = state['fac']
        facs = []
        for i, j in enumerate(range(0, 20, 4)):
            f = []
            for _ in range(4):
                f.append(factories[j])
            facs.append(f)

        return facs


    # Recorta as fabricas e o chao de fabrica possivel
    def _get_mask_fab(self):
        state = self.estado.get_states()
        factories   = state['fac']
        floor       = state['fac-flr']

        print('fabricvas ' ,factories)
        print('piso ' ,floor)

        fabs = []
        for i, j in enumerate(range(0,20, 4)):
            if factories[j] != -1:
                fabs.append(i)

        if floor[0] != -1:
            fabs.append(5)

        print(fabs)

        return fabs

    # Pega os possiveis locais de pegagem de ceramica e gera listas com eles
    def _get_mask_catch(self, idk):
        floor = self.estado.get_states()['fac-flr']
        factories   = self._get_fabs_pre_process()
        picks_possibles = None

        if idk != 5:
            picks_possibles = factories[idk]
        else:
            picks_possibles = floor


        return picks_possibles




   # def get_mask_action(self):
        state = self.estado.get_states()

        factories       = state['fac']
        factory_floor   = state['fac-flr']
        ply_bord_01     = state['ply_01']


        # Retorna os locais possiveis para se pegar ceramica
        pick = []







        # Retorna as cores possiveis para se pegar
        color = []

        # Retorna os locais possiveis para se colocar ceramica
        put = []



        mask = [pick,color,put]

        return mask




#==============================================================================

# Exemplo de uso:
env = None
print("Estado:", env.state)
print("Ações inválidas:", env.invalid_actions)
print("Máscara de ações:", env.action_masks())












































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

