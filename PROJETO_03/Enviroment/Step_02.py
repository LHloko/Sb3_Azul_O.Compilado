from Ambiente.M_game_v3 import State_V3 as estado
from Enviroment import Observation as obs


def valid_actions(dados, idx_jogador):
        return sorted(valid_lines_01(dados, idx_jogador))


def pre_process_line_board(dados, idx_jogador):
    """
    Entrada: Conjunto de dados do jogo e o indice do jogador 
    Saida: List com as linhas adjacentes do tabuleiro do jogador passado
    """    
    
    lines  = estado.Estados(dados).get_states()[idx_jogador]

    lns =[]

    lns.append([lines[25]])
    lns.append([lines[26],lines[27]])
    lns.append([lines[28],lines[29],lines[30]])
    lns.append([lines[31],lines[32],lines[33],lines[34]])
    lns.append([lines[35],lines[36],lines[37],lines[38],lines[39]])

    return lns

def pre_process_wall_board(dados, idx_jogador):
    """
    Entrada: Conjunto de dados do jogo e o indice do jogador 
    Saida: Lista contendo a parede do jogador passado 
    """   
    
    wall = estado.Estados(dados).get_states()[idx_jogador]

    lns=[]
    idx = 0
    for i in range(5):
        l =[]
        for j in range(5):
            l.append(wall[idx])
            idx += 1
        lns.append(l)

    return lns

def pre_process_fabs(dados):
    """
    Entrada: Conjunto de dados do jogo 
    Saida: Lista contendo as fabricas
    """   
    
    state = estado.Estados(dados).get_states()
    
    factories = state['fac']

    facs = []

    for i in range(5):
        f = []
        for j in range(4):
            f.append(factories[i*4 + j])
        facs.append(f)

    floor = state['fac-flr']

    fl = []
    for i in floor:
        if i != -1:
            fl.append(i)
    facs.append(fl)

    return facs

def pre_process_fabs_floor(dados):
    """
    Entrada: Os dados do jogo para pegar o chao de fabrica
    Saida: Uma list contendo 5-cor disponivel pra uso
    """

    #Pega as jogadas ja processadas 
    j_fab = []
    
    #Pegar o chao de fabrica e avaliar as peças que tem dentro
    fabs = dados[0]
    fabs = fabs.get_factory_floor()
    
    if fabs:
        for cor in fabs:
            if cor != -1:
                color = [5]
                color.append(cor)
                if not color in j_fab: # Adiciona se nao houver o conjunto
                    j_fab.append(color)
    
    jogadas = []
    
    # Crio as jogadas possiveis
    for j in j_fab:

        for k in range(6):
            jg = j[:]
            jg.append(k)
            jogadas.append(jg)
    
    
    return jogadas

def valid_fabricas(dados):
    """
    Entrada: Conjunto de dados do jogo
    Saida: 
    """   
    
    state = estado.Estados(dados).get_states()
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

    if floor[0] == -1 :
        if floor[1] != -1:
            facs.append(5)
        else:
            facs.append(-1)
    else:
        facs.append(5)
            
    return facs

def valid_cores(dados):
    """
    Entrada: Conjunto de dados do jogo e o indice do jogador 
    Saida: Uma list contendo as combinacoes fab-cor 
    """   
    
    state = valid_fabricas(dados)
    state = [valid for valid in state if valid != -1] # comprime para so validos

    fabs = pre_process_fabs(dados)

    facAndColor = []

    for i in state:
        for j in fabs[i]:
            facAndColor.append([i,j])

    return facAndColor



def valid_lines_01(dados, idx_jogador):
    
    # Obtém combinações válidas de fábrica e cor
    states = valid_cores(dados)
    
    # Prepara o tabuleiro do jogador
    lines = pre_process_line_board(dados, idx_jogador)
    wall = pre_process_wall_board(dados, idx_jogador)
    
    valid_play = []

    # Adiciona o piso como opcao 
    for f_c in states:
        stp = f_c.copy()
        stp.append(5)  # Piso
        valid_play.append(stp)

    # Identifica linhas vazias e adiciona jogadas validas
    empty = [i for i, sublista in enumerate(lines) if all(x == -1 for x in sublista)]
    for i in states:
        for j in empty:
            stp = i.copy()
            stp.append(j)
            valid_play.append(stp)

    # Identifica linhas parcialmente preenchidas e verifica compatibilidade de cor
    parcel_empty = [i for i, sublista in enumerate(lines) if any(x == -1 for x in sublista) and not all(x == -1 for x in sublista)]
    for f_c in states:
        cor = f_c[1]
        for parcel in parcel_empty:
            color_line = lines[parcel][0]
            if color_line == cor:
                stp = f_c.copy()
                stp.append(parcel)
                valid_play.append(stp)

    # Remove jogadas para linhas completamente preenchidas
    full_line = [i for i, sublista in enumerate(lines) if all(x != -1 for x in sublista)]
    valid_play = [v for v in valid_play if v[2] not in full_line]

    # Remove duplicatas
    valid_play = remove_duplicates(valid_play)
    valid_play = sorted(valid_play)

    # Validação final contra a parede
    filtered_play = []
    
    for v in valid_play:
        linha_destino = v[2]
        cor = v[1]

        # Para o piso, a jogada é sempre válida
        if linha_destino == 5:
            filtered_play.append(v)
        else:
            # Verifica se a linha está cheia na parede
            if cor in wall[linha_destino] and all(x != -1 for x in lines[linha_destino]):
                print(f"Jogada inválida: {v}, motivo: cor já está na parede ou linha cheia.")
            else:
                filtered_play.append(v)

    # Caso nenhuma jogada seja válida, retorna apenas a opção de enviar para o piso
    if not filtered_play:
        for f_c in states:
            stp = f_c.copy()
            stp.append(5)
            filtered_play.append(stp)

    return filtered_play

def remove_duplicates(lst):
    """
    Entrada: Lista com varias listas
    Saida: A mesma lista passada retirando as redundancias 
    """   
    
    seen = set()
    result = []
    for sublist in lst:
        sublist_tuple = tuple(sublist)  # Converte a sublista para tupla para que possa ser adicionada ao set
        if sublist_tuple not in seen:
            seen.add(sublist_tuple)
            result.append(sublist)
    return result

def invalid_actions(dados, idx_jogador):
    """
    Entrada: Conjunto de dados do jogo e o indice do jogador 
    Saida: List contendo todas as jogadas invalidas 
    """   
    
    valid_act = valid_actions(dados, idx_jogador)

    resultados = []
    for primeiro in range(6):
        for meio in range(5):
            for ultimo in range(6):
                lista = [primeiro, meio, ultimo]
                resultados.append(lista)

    def converter_para_tuplas(lista):
        return tuple(tuple(sub_lista) for sub_lista in lista)
    
    # Define as listas válidas e possíveis
    validas = valid_act
    possiveis = resultados

    # Converte as listas em tuplas para operações de conjuntos
    validas_tuplas = set(converter_para_tuplas(validas))
    possiveis_tuplas = set(converter_para_tuplas(possiveis))
    
    # Calcula as listas inválidas (listas possíveis que não são válidas)
    invalidas_tuplas = possiveis_tuplas - validas_tuplas
    
    # Converte as tuplas de volta para listas
    invalidas = [list(sub_lista) for sub_lista in invalidas_tuplas]

    return invalidas

def possible_actions():
    """
    Entrada: Vazio
    Saida: Todas as jogadas possiveis 
    """   
    
    resultados = []
    for primeiro in range(6):
        for meio in range(5):
            for ultimo in range(6):
                lista = [primeiro, meio, ultimo]
                resultados.append(lista)
                
    return resultados

def jogar_discretamente(action):
    jogada = possible_actions()
    jogada = jogada[int(action)]
    
    return jogada

def step(action, dados, estado):
    """
    Entrada: Uma acao que consiste em um discreto de 0 - 179
    Saida: A recompensa e observacao 
    """
    
    reward = 0 
    rw_01 = 0
    rw_02 = 0
    
    jogada = 0
    players = dados[2]
    fab = dados[0]
    
    terminated = False
    truncated = False 
        
    ###
    #   Se a jogada eh valida eu jogo 
    #   Jogo, recebo a recompensa, verifico se o turno terminou 
    #   Se terminou vejo se o jogo terminou
    #   Se o jogo nao terminou
    ###

    for plyr in players:
        idx_player = players.index(plyr)
        validas = valid_actions(dados, idx_player)
        
        if plyr.get_name() == 'AGENTE':
            # jogada = jogar_discretamente(action) 
            try:
                jogada = valid_actions(dados, idx_player)[0]
            except:
                #print(valid_lines_01(dados, idx_player))
                pass
        else:
            try:
                jogada = valid_actions(dados, idx_player)[0] # Pega a primeira jogada valida
            except:
                #print(valid_lines_01(dados, idx_player))
                pass
    

        # Verifico se a jogada eh valida
        if not jogada in validas:           
            reward += -10
            truncated = True 
            print('zuou aq', jogada )
        
        else:
            # Executo a jogada 
            plyr.playar(fab, jogada)
        
        # Fim de turno 
        if estado.fim_de_turno(): 
            rw_01 += players[0].pontuar()
            rw_02 += players[1].pontuar()
            
            reward = rw_01 - rw_02
    
            # Fim de jogo 
            if estado.is_game_over():
                terminated = True
                estado.fim_de_jogo()
            else:
                estado.first_player()
                estado.iniciar_turno()
                
                
        observation = obs.observacao(dados)
        info = {} 
                
    return observation, reward, terminated, truncated, info



