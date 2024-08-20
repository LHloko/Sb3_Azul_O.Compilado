from eviroment.Env_solo1.S_game_V3 import Board_v3

#Start class ------------------------------------------------------------------
class Jogador():

    def __init__(self, name):
        self.board = Board_v3.Board(name)
        self.score_jogo = 0
        self.score_agente = 0
        self.name = name

    def get_name(self):
        return self.name

    def get_tabuleiro(self):
        return self.board

    def get_score(self):
        return self.score_jogo

    def __str__(self):
        return f'''
PLAYER [[[ {self.name} ]]]
SCORE Jogo = {self.score_jogo}
Score Agente = {self.score_agente}
{self.board}
    '''

    '''
    Entrada: Vazio 
    Saida: Verdadeiro caso o jogador contenha 0 -1 e falso senao 
    '''
    def me_first(self):
        lixo = self.board
        lixo = lixo.get_trash()
        for i, um in enumerate(lixo):
            if um == -1:
                lixo.pop(i)
                return True

        return False

    '''
    Entrada: Vazio 
    Saida: Verdadeiro caso o jogador contenha 0 -1 e falso senao 
    '''
    def me_have_minus_one_gd(self):
        lixo = self.board
        lixo = lixo.get_trash()
        for i, um in enumerate(lixo):
            if um == -1:
                return True

        return False


    '''
    Entrada: fabrica do jogo, e uma list jogada: 
     - onde pegar ceramica - qual ceramica pegar - onde por a ceramica pega -
    Saida: Verdadeiro para caso seja uma açao valida, falso senao
    '''
    def playar(self, fab, jogada):
        locus, pars, linea = jogada
        
        # Pegando as ceramicas
        tiles = self.pegar_ceramica(fab, locus, pars)
        assert tiles , "acao de pegar - invalida"

        # Colocando as ceramicas no tabuleiro
        assert self.colocar_no_tabuleiro(tiles, linea), "acao de meter - invalida"

        return True


    '''
    Entrada: fb - fabrica do jogo, lc - local onde se pegar ceramicas
    Saida: Lista com as ceramicas pegas ou falso senao for possivel 
    '''
    def pegar_ceramica(self, fabrica, lugar, ceramica):

        #Escolheu -> Fabrica
        if lugar >= 0 and lugar <=4:
            tiles = fabrica.pick_ceramic_board(lugar, ceramica)

        #Escolheu -> Chao de Fabrica
        elif lugar == 5:
            tiles = fabrica.pick_ceramic_floor(ceramica)

        else:
            tiles = False

        return tiles

    '''
    Entrada: ceramicas pegas 
    Saida: Verdadeiro em sucesso ou False senao 
    Insere, se possivel, as ceramicas na linha passada 
    '''
    def colocar_no_tabuleiro(self, ceramicas, linha):
        if not self.board.cement_line(ceramicas, linha):
            return False

        return True


###############################################################################

    '''
    Entrada: Vazia
    Saida: Verdadeiro caso uma linha sera completada, falso senao 
    '''
    def ended_game(self):
        if self.board.is_last_round():
            return True

        return False

    '''
    Entrada: Vazia 
    Saida: Vazia 
    Soma os pontos da tabela e a reseta ao fim de uma rodada de jogo  
    '''
    def pontuar(self):
        score_jogo = 0
        score_recompensa = 0
        score_sub = self.board.des_somar_ceramicas()

        recompensa = self.board.emparedar()

        # Salva a pontuaçao do jogador
        score_jogo += recompensa[0]
        score_jogo -= score_sub

        # Salva a pontuaçao do agente
        score_recompensa += recompensa[1]
        score_recompensa -= score_sub

        self.score_jogo += score_jogo
        #
        self.score_agente += score_recompensa

        return score_recompensa

    '''
    Entrada: Vazia 
    Saida: Vazia 
    Soma os pontos da tabela e a reseta ao fim de um jogo  
    '''
    def pontuar_ultimate_final(self):
        score_final = 0
        score_final += self.board.last_pontuar()

        self.score_jogo += score_final

        return score_final

    '''
    Entrada: Vazio
    Saida: Retorna verdadeiro caso haja uma linha do tabuleiro desse jogador que
    esteja completa, indicando o fim do jogo 
    '''
    def board_full(self):
        if self.board.is_line_wall_full():
            return True

        return False

#End class --------------------------------------------------------------------

