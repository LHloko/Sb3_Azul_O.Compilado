from Ambiente.M_game_v3 import Board_v3
from Ambiente.M_game_v3 import Factory_V3
from Ambiente.M_game_v3 import Player_V3
from Ambiente.M_game_v3 import State_V3

import numpy as np

'''

    O que fara minha funcao de observacao ? 
        Ela retornar o estado atual do jogo independe do momento deste 
    
    O que eu preciso para montar ela ?
        preciso das fabricas 
        preciso do chao de fabricas 
        preciso de todos os jogadores
            pego o tabuleiro de cada um 
                recortar a parede
                recortar as linhas adjacente
                recortar a linha de baixo do tabuleiro 
        
    Como eu vou organizar isso tudo ? 
        sera uma linha so que descrevera o estado atual de jogo, juntando tudo
    
'''

def tabuleiro_de_jogador(jogadores):
    # Pegar os tabuleiros de cada jogador 
    tabuleiros = []    
    
    for i in jogadores:
        tabuleiros.append(i.get_tabuleiro())
    
    # Separar do tabuleiro a parede e as linhas adjacente 
    obs_tabu = []

    for i in tabuleiros:
        wall = i.get_wall()
        wall = [
            [cor if estado else -1 for cor, estado in line] 
            for line in wall
            ]
        wall = np.array(wall).flatten()
    
        pattern = i.get_pattern()
        pattern = [
            [cor if estado else -1 for cor, estado in line] 
            for line in pattern
            ]

        pattern = np.concatenate(pattern)
        
        obs_tabu = np.concatenate((obs_tabu,pattern, wall))
        
    # Junto ambas em um list unidimensional e retorno
    return obs_tabu


def fabricas_de_jogo(tabuleiro):
    tabu = tabuleiro.get_factory_board()
    
    # Criando uma list numpy de 20 elementos -1
    fabricas = np.full(20, -1)

    # Passa as fabricas para a list
    i = 0
    for line in tabu:
        if not line:
            line = [-1,-1,-1,-1]
        for col in line:
            fabricas[i] = col
            i += 1
    
    return fabricas


def chao_de_fabrica_de_jogo(tabuleiro):
    # Chao de fabrica
    flr = tabuleiro.get_factory_floor()

    # Criando uma matriz 5x4
    chao = np.full(15, -1)

    if not flr:
        return chao

    for i, cel in zip(range(15), flr):
        chao[i] = cel

    return chao


'''
Entrada: game_infos sao os dados de jogo, e nele devem ter os jogadores e as
         fabricas
Saida: um recorte do estado do jogo atual em  um vetor unidimensional 
'''
def observacao(game_infos):
    tab_jogador = tabuleiro_de_jogador(game_infos[2])
    fabs = fabricas_de_jogo(game_infos[0])
    chao = chao_de_fabrica_de_jogo(game_infos[0])
    
    observe = np.concatenate((tab_jogador,fabs, chao))
    
    return observe
    