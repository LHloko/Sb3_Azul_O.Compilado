# Criando a minha mascara de aÃ§oes
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import List, Optional

# Minhas Classes
from eviroment.Env_solo1.S_game_V3 import Factory_V3
from eviroment.Env_solo1.S_game_V3 import State_V3
from eviroment.Env_solo1.S_game_V3 import Player_V3

class AzulEnv(gym.Env):
    metadate = {"render_modes":['rgb_array','human']}

    def __init__(self, render_mode = None):
        super(AzulEnv, self).__init__()

        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fÃ¡brica
        self.players = [Player_V3.Jogador("AGNT")]  # Instanciar o jogador
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
    Saida: A observaÃ§ao do estado inicial do jogo 
    Inicia um jogo do zero, com a instanciaÃ§ao de cada classe e dos jogadores 
    '''
    def reset(self, seed=None, options=None):
        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fÃ¡brica
        self.players = [Player_V3.Jogador("AGNT")]  # Instanciar os jogadores =+= , Jogador.Jogador("VK")
        self.truncated = False
        self.terminated = False

        # Dados iniciais do ambiente
        self.dados = [self.fab, self.fab.pocket, self.players]

        # Estado inicial do jogo
        self.estado = State_V3.Estados(self.dados)

        # Retornar a observaÃ§Ã£o inicial do ambiente
        return self.observe(), self._get_info()

    '''
    Entrada: action como uma tupla com 3 valores 
    Saida: List com 'observation, reward, terminated, truncated, info'
    Implementar lÃ³gica para executar uma aÃ§Ã£o no ambiente
    '''
    def step(self, action):
        reward = 0
        jogada = self._possible_actions()[action]
        valids =self.valid_actions()

        if jogada not in valids:
                jogada = valids[0]

        # Executar a acoes no ambiente
        self.players[0].playar(self.fab ,jogada)
        self.render() if self.render_mode=='human' else None


        if self.estado.fim_de_turno(): # Verificar se o turno acabou
            reward += self.players[0].pontuar()
            if self.estado.is_game_over(): # Verificar se o jogo acabou
                self.terminated = True
                self.estado.fim_de_jogo()
            else: # senao, reinicia o ambiente
                self.estado.iniciar_turno()

        # Atualizar o estado do jogo e retornar a observaÃ§Ã£o, recompensa e sinalizadores de tÃ©rmino
        observation = self.observe()
        info = self._get_info()

        return observation, reward, self.terminated, self.truncated, info


    '''
    Entrada: agent
    Saida: A observaÃ§ao do ambiente (fabricas-chao_de_fabrica-tabuleiros) como 
    uma matriz.
    '''
    def observe(self):
        # Obter o estado atual do jogo
        state = self.estado.get_states()

        factories       = state['fac']
        factory_floor   = state['fac-flr']
        ply_bord_01     = state['ply_01']

        # Processar o estado para criar as observaÃ§Ãµes
        table = np.concatenate((factories, factory_floor, ply_bord_01))

        observations = np.array(table)

        return observations


    '''
    Entrada: Vazia
    Saida: informaÃ§ao como um dict de quem e o primeiro jogador e se eh o ultimo round
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
        print(self.fab)
        self.estado.game_player_status()


    # ???
    def valid_actions(self):
        return sorted(self._valid_lines())

# =========================================================================== #
    def _pre_process_line_board(self):
        lines  = self.estado.get_states()['ply_01']

        lns =[]

        lns.append([lines[25]])
        lns.append([lines[26],lines[27]])
        lns.append([lines[28],lines[29],lines[30]])
        lns.append([lines[31],lines[32],lines[33],lines[34]])
        lns.append([lines[35],lines[36],lines[37],lines[38],lines[39]])

        return lns

    def _pre_process_wall_board(self):
        wall = self.estado.get_states()['ply_01']

        lns=[]
        idx = 0
        for i in range(5):
            l =[]
            for j in range(5):
                l.append(wall[idx])
                idx += 1
            lns.append(l)

        #print('wall', lns)
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

    def _valid_lines(self):
        states = self._valid_cores()
        #meter sempre o piso do tab com opcao + SEMPRE + 'SONS DE TROVAO'
        lines  = self._pre_process_line_board()

        valid_play = []

        # Adicionando o piso como uma opcao
        for f_c in states:
            stp = f_c.copy()
            stp.append(5)
            if stp not in valid_play:
                valid_play.append(stp)

        # Pega o indice das linhas vazias
        empty = [i for i, sublista in enumerate(lines) if all(x == -1 for x in sublista)]

        # Cria acoes possiveis com as linhas vazias
        for i in states:
            for j in empty:
                stp = i.copy()
                stp.append(j)
                if stp not in valid_play:
                    valid_play.append(stp)

        # Pega o indice das linhas parcialmente cheias
        parcel_empty = [i for i, sublista in enumerate(lines) if any(x == -1 for x in sublista) and not all(x == -1 for x in sublista)]

        # Cria acoes possiveis com as linhas parcialmente cheias
        for f_c in states:
            cor = f_c[1]
            for parcel in parcel_empty:
                color_line = lines[parcel][0]
                if color_line == cor:
                    stp = f_c.copy()
                    stp.append(parcel)
                    valid_play.append(stp)

        # Filtra as linhas cheias
        full_line = [i for i, sublista in enumerate(lines) if all(x != -1 for x in sublista)]

        for v in valid_play:
            if v[2] in full_line:
                valid_play.remove(v)

        # Filtra jogadas repetidas
        valid_play = self._remove_duplicates(valid_play)
        valid_play = sorted(valid_play)

        # Filtra a parede
        wall = self._pre_process_wall_board()

        other_test =[]

        for v in valid_play:
            if v[2] != 5:
                if v[1] in wall[v[2]]:
                    pass
                else:
                    other_test.append(v)
            else:
                other_test.append(v)

        valid_play = other_test

        return valid_play

    def _remove_duplicates(self, lst):
        seen = set()
        result = []
        for sublist in lst:
            sublist_tuple = tuple(sublist)  # Converte a sublista para tupla para que possa ser adicionada ao set
            if sublist_tuple not in seen:
                seen.add(sublist_tuple)
                result.append(sublist)
        return result

    def _invalid_actions(self):
        valid_actions = self._valid_actions()

        resultados = []
        for primeiro in range(6):
            for meio in range(5):
                for ultimo in range(6):
                    lista = [primeiro, meio, ultimo]
                    resultados.append(lista)

        def converter_para_tuplas(lista):
            return tuple(tuple(sub_lista) for sub_lista in lista)
        
        # Define as listas válidas e possíveis
        validas = valid_actions
        possiveis = resultados

        # Converte as listas em tuplas para operações de conjuntos
        validas_tuplas = set(converter_para_tuplas(validas))
        possiveis_tuplas = set(converter_para_tuplas(possiveis))
        
        # Calcula as listas inválidas (listas possíveis que não são válidas)
        invalidas_tuplas = possiveis_tuplas - validas_tuplas
        
        # Converte as tuplas de volta para listas
        invalidas = [list(sub_lista) for sub_lista in invalidas_tuplas]

        return invalidas

    def _possible_actions(self):
        resultados = []
        for primeiro in range(6):
            for meio in range(5):
                for ultimo in range(6):
                    lista = [primeiro, meio, ultimo]
                    resultados.append(lista)
        return resultados

#==============================================================================
    def action_masks_fn(self):
        actions = np.zeros(180)
        pos_act = self._possible_actions()
        val_act = sorted(self.valid_actions())
        #print(val_act)

        idx = 0
        for i, p in enumerate(pos_act):
            if len(val_act) == idx:
                break

            if val_act[idx] == p:
                actions[i] = 1
                idx+=1

        return actions

#==============================================================================
# Exemplo de uso:
'''
env = AzulEnv('human')
env.reset()
env.render()
env._pre_process_wall_board()

trun = False


for i in range(100):
    input()
    if(trun):
        break
    observation, reward, term, trun, info= env.step(0)
    print('RECOMPENSA => ', reward)
'''