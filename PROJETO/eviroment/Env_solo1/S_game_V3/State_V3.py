"""
Created on Fri May 10 17:30:58 2024

@author: lbalieiro@lince.lab
"""

import numpy as np
from eviroment.Env_solo1.S_game_V3 import Factory_V3
from eviroment.Env_solo1.S_game_V3 import Player_V3

#Start class ------------------------------------------------------------------
class Estados():

    '''
    Entrada: Uma tupla: [ fabrica, saco, [jogadores]] chamada dados
    '''
    def __init__(self, dados):
        self.fab = dados[0]
        self.pocket = dados[1]
        self.players = dados[2]

        self.static_players = dados[2]

    '''
    Entrada: vazia 
    Saida: Verdadeiro caso seja o fim do jogo e Falso senao 
    Verifica se algun dos jogadores tem uma linha completa no seu tabuleiro 
    '''
    def is_game_over(self):
        for ply in self.players:
            if ply.board_full():
                return True

        return False

    '''
    Entrada: vazia 
    Saida: Anuncia o ganhador e seu score, em caso de empate so o score
    '''
    def fim_de_jogo(self):
        pontos = 0
        #Ultima contagem de pontos
        for ply in self.players:
            pontos = ply.pontuar_ultimate_final()

        #Anuncia o Ganhador
        win = self.is_winner()
        if isinstance(win, int):
            print(f"======== O JOGO EMPATOU com SOCORE: {win} ========")

            pass
        
        return pontos

    '''
    Entrada: Vazia
    Saida: Verdadeiro para fim de do turno e falso senao
    Condiçao de fim de jogo: Todas as fabricas estao vazias e o chao tambem esta
    '''
    def fim_de_turno(self):
        # Verifico se as fabricas e o chao estao vazios
        if self.fab.is_board_empty() and self.fab.is_floor_empty():
            return True

        return False


    '''
    Entrada: Vazia 
    Saida: Vazia 
    Reinicia um turno de jogo, reiniciando a mesa de jogo 
    '''
    def iniciar_turno(self):
        #verifico a quantidade de peças do saco
        calc = self.fab.num_factorys * 4
        if len(self.pocket.pkt) < calc:
            #reembaralhar o saco
            self.pocket.set_pocket_adj_pkt(self.chao_limpo_board())
            self.pocket.bag()

        #Reiniciar a mesa de jogo
        self.fab.re_manufacture_board()


    '''
    Entrada: Vazia
    Saida: Vazia
    Verifica qual jogador tem o -1 e o coloca no inicio da list de jogadores
    '''
    def first_player(self):
        players = self.players
        for i, p in enumerate(players):
            if p.me_first():
                players.pop(i)
                players.insert(0, p)
                break

        return True


    '''
    Entrada: Vazia
    Saida: O player que tem o maior numero de pontos ou falso em caso de empate
    '''
    def is_winner(self):
        player = []
        player.append(self.players[0])
        scr = player[0].get_score()

        #pega a maior pontuaçao
        for p in self.players:
            if p.score_jogo > scr:
                scr = p.score
                player = p

        player = []

        #Verifica se tem mais de um com a mesma pontuaçao
        for p in self.players:
            if p.score_jogo == scr:
                player.append(p)

        if len(player) == 1:
            return player[0]
        else:
            return player[0].score_jogo


    '''
    Entrada: Vazia 
    Saida: Uma list contendo todas as peças dos lixos de cada tabuleiro 
    '''
    def chao_limpo_board(self):
        sacoadj = []

        for p in self.players:
            trash = p.board.get_trash()
            for _ in range(len(trash)):
                sacoadj.append(trash.pop())

        return sacoadj

    '''
    Entrada: vazia
    Saida: Imprime o tabuleiro de cada jogador 
    '''
    def game_player_status(self):
        for p in self.players:
            print(p)
            print()

    '''
    Entrada: Vazia 
    Saida: Verdadeiro caso seja a ultima rodada antes do fim do jogo 
    '''
    def is_last_round_to_end(self):
        for p in self.players:
            if p.ended_game():
                return True

        return False

###############################################################################
    '''
    Entrada: Vazia 
    Saida: Um dicionario com o estado atual do jogo  
    '''
    def get_states(self):
        factories     = self.format_factories()
        factory_floor = self._format_fac_floor()
        ply_bord_01   = self._format_player_board(self.static_players[0])

        state = {'fac'      : factories,
                 'fac-flr'  : factory_floor,
                 'ply_01'   : ply_bord_01,
       }

        return state

    '''
    Entrada: Vazio
    Saida: Uma matriz numpy 5x4 contendo o estado das fabricas -2 se estiver 
    vazia senao a ceramica presente
    '''
    def format_factories(self):
        # Fabricas
        fac = self.fab.get_factory_board()

        # Criando uma list numpy de 20 elementos -1
        mtx = np.full(20, -1)

        # Passa as fabricas para a list
        i = 0
        for line in fac:
            if not line:
                line = [-1,-1,-1,-1]
            for col in line:
                mtx[i] = col
                i += 1

        return mtx

    '''
    Entrada: Vazio
    Saida: Uma matriz numpy 5x4 que representa o chao de fabrica com -2 senao 
    preenchida com as ceramicas
    '''
    def _format_fac_floor(self):
        # Chao de fabrica
        flr = self.fab.get_factory_floor()

        # Criando uma matriz 5x4
        mtx = np.full(15, -1)

        if not flr:
            return mtx

        for i, cel in zip(range(15), flr):
            mtx[i] = cel


        return mtx


    '''
    Entrada: Player passado como parametro 
    Saida: Uma matriz numpy 5x10 contendo a parede e as linhas adjacentes
    '''
    def _format_player_board(self, player):
        '''
        pego a wall -> converto em um 5x5 onde -1 eh vazio senao eh preenchido
        pego as linhas adjacentes -> converto em um 5x5 onde -2 eh vazio, -3 eh
        posiçao inexistente senao eh preenchido
        concateno um em cima do outro
        '''
        # Recebe a parede e as linhas adjacentes do jogador
        board    = player.get_tabuleiro()
        adj_line = board.get_pattern()
        wall     = board.get_wall()

        #Criando duas matrizes 5x5
        mtx_01 = np.full(15,-1) # Adj_lines
        mtx_02 = np.full((5,5),-1) # Wall

        #Convertendo adj_line -> mtx_01
        i = 0
        for line in adj_line:
            for col in line:
                if col[1] == True:
                    mtx_01[i] = col[0]
                i+=1

        #Convertendo wall -> mtx_02
        for l, line in enumerate(wall):
            for c, col in enumerate(line):
                if col[1] == True:
                    mtx_02[l][c] = col[0]

        mtx_02 = np.ravel(mtx_02)

        #Concatenando as matrizes auxiliares
        mtx_000 = np.concatenate((mtx_02, mtx_01))

        return mtx_000

    def burlar(self):
        pass

#End class --------------------------------------------------------------------
