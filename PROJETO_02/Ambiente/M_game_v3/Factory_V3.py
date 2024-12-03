import Bag_v3 as Saco

#Start class ------------------------------------------------------------------
class Fabrica():

    def __init__(self):
        #Variaveis de uma Mesa
        self.num_factorys = 5       #Define o numero padrao de fabricas para 2 players
        self.factory_board = []     #Cria a o circulo de fabricas como uma list
        self.factory_floor = []     #Cria o chao de fabrica como uma list
        self.pocket = Saco.Bag()    #Instancia de um saco (rsrs) de ceramicas

        self.manufacture_board()    #Inicia a mesa de fabricas


    """
    #  GETTERS - SETTERS - __STR__  #
    """
    def get_num_factorys(self):
        return self.num_factorys

    def get_factory_board(self):
        return self.factory_board

    def get_factory(self, index):
        fac = self.factory_board[index]
        return fac

    def get_factory_floor(self):
        return self.factory_floor

    def get_pocket(self):
        return self.pocket

    def set_num_factorys(self, num):
        self.num_factorys = num

    def set_factory_board(self, board):
        self.factory_board = board

    def set_factory(self, index, fac):
        self.factory_board[index] = fac

    def set_factory_floor(self, floor):
        self.factory_floor = floor

    def set_pocket(self, pkt):
        self.pocket = pkt
        
    def __str__(self):
        # Dicionário de símbolos para as cores
        color_symbols = {0: "🟦", 1: "⬜", 2: "⬛", 3: "🟥", 4: "🟨", -1: "O"}
        color_names = {0: "Azul", 1: "Preto", 2: "Branco", 3: "Vermelho", 4: "Amarelo", -1: "Peça inicial"}
    
        # Garantir que cada fábrica tenha 4 elementos (preenchendo com -1 caso necessário)
        formatted_factories = []
        for factory in self.factory_board:
            factory += [-1] * (4 - len(factory))  # Completa a fábrica com -1 caso tenha menos de 4 itens
            formatted_factories.append(factory)
    
        # Criar uma linha única com todas as fábricas
        factory_line = ""
        for i, factory in enumerate(formatted_factories):
            factory_line += f" * {i} * "  # Número da fábrica
            for color in factory:
                if color != -1:
                    factory_line += f"{color_symbols.get(color, ' ')} "
                else:
                    factory_line += "   "  # Espaço vazio se o valor for -1
            factory_line += "   "  # Espaço entre as fábricas

    
        # Exibir as fábricas e a legenda
        return f"""FABRICAS:
{factory_line.strip()}

CHAO DE FABRICA: 
         {' '.join(color_symbols.get(color, ' ') for color in self.factory_floor)}
"""



    """
    #  Funçoes de Classe  ================================================== #
    """

    '''
    Entrada: Vazia 
    Saida: Retorna uma list com quatro ceramicas escolhidas aleatoriamente
    Cria uma list contendo 4 cores selecionadas usando a biblioteca random
    '''
    def manufacture(self):
        ceramicas_set = []
        for _ in range(4):
            ceramicas_set.append(self.pocket.pkt.pop(0))

        return ceramicas_set

    '''
    Entrada: Vazio
    Saida: Preenche a matriz factory_board com peças aleatorias e descontadas 
    do saco, e reinicia o chao de fabrica com -1
    
    '''
    def manufacture_board(self):
        for i in range(self.num_factorys):
            facture = self.manufacture() #Isso eh uma Fabrica recebendo 4 ceramicas
            self.factory_board.append(facture)

        self.factory_floor.append(-1)

    def re_manufacture_board(self):
        #Variaveis de uma Mesa
        self.factory_board = []     #Cria a o circulo de fabricas como uma list
        self.factory_floor = []   #Cria o chao de fabrica como uma list

        self.manufacture_board()    #Inicia a mesa de fabricas

    '''
    Entrada: A fabrica escolhida, factury e a ceramica escolhida, tile
    Saida: Uma lista contendo todas as peças semelhantes da escolhida ou falso 
    senao existir essa ceramica 
    '''
    def pick_ceramic_board(self, factury, tile):
        piece = tile
        fac = self.factory_board[factury] #List: fabrica escolhida
        pushcart = [] #List com todos as ceramicas escolhidas

        #Verifica se tem esse tipo de ceramica na fabrica
        if not self.not_ceramic(fac, piece):
            return False

        for i in range(4): #Separa as peças iguais e as que vao pro chao de f.
            lady = fac.pop(0)
            if piece == lady:
                pushcart.append(lady)
            else:
                self.factory_floor.append(lady)

        #organiza o chao de fabrica
        self.factory_floor.sort()

        return pushcart

    '''
    Entrada: A ceramica escolhida: piece
    Saida: Uma lista contendo todas as peças semelhantes da escolhida ou falso 
    senao existir a ceramica 
    Retorna uma lista com todas as peças semelhantes a escolhida, se o [-1] 
    estiver ele eh adicionado a list retornada
    '''
    def pick_ceramic_floor(self, piece):
        pushcart = [] #List com todos as ceramicas escolhidas
        floor = self.factory_floor

        #Verifica se tem esse tipo de ceramica no chao
        if not self.not_ceramic(floor, piece):
            return False

        if len(self.factory_floor) != 0:
            if self.factory_floor[0] == -1:
                um = self.factory_floor.pop(0)
                pushcart.append(um)

        while piece in floor:
            floor.remove(piece)
            pushcart.append(piece)

        #organiza o chao de fabrica
        self.factory_floor.sort()

        return pushcart

    '''
    Entrada: Vazio  
    Saida: Verdadeiro se o chao de fabrica esta limpo, i.e so tem o [-1], Falso
    senao
    '''
    def clear_floor(self):
        #Verificar se ha ceramicas no chao de fabrica
        if len(self.factory_floor) == 1 and self.factory_floor[0] == -1:
            return True

        return False

    '''
    Entrada: Index da fabrica 
    Saida: Verdadeiro caso a fabrica passada no index esteja vazia, e falso se
    nao
    '''
    def is_manufacture_empty(self, index):
        if len(self.factory_board[index]) == 0:
            return True

        return False

    '''
    Entrada: Vazio
    Saida: Verdadeiro caso o chao de fabrica esteja vazio, e falso senao
    '''
    def is_floor_empty(self):
        if not self.factory_floor:
            return True

        return False

    '''
    Entrada: Vazio
    Saida: Verdadeiro caso todas as fabricas estejam vazias, e falso senao
    '''
    def is_board_empty(self):

        if all(fab == [-1, -1, -1, -1]for fab in self.factory_board):
            return True
        else:
            return False


    '''
    Entrada: Ceramica selecionada piece e list avaliada
    Saida: Verdadeiro caso tenha a ceramica, e falso senao
    '''
    def not_ceramic(self, lista, piece):
        if piece in lista:
            return True

        return False

#End class --------------------------------------------------------------------

    """
    Entrada: Vazia 
    Saida: Vazia 
    Serve so pra testar algumas coisas em um tabuleiro parcialmente cheio ou 
    construido 
    """
    def roubar(self):
        self.factory_floor.append(2)
        self.factory_floor.append(2)
        self.factory_floor.append(3)
        self.factory_floor.append(1)
    
        pass