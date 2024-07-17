import random
from enum import Enum

#Start class ------------------------------------------------------------------
class Color(Enum):
    #cores
    BLUE = 0
    WHITE = 1
    BLACK = 2
    RED = 3
    YELL = 4
#End class --------------------------------------------------------------------


#Start class ------------------------------------------------------------------
class Bag():

    def __init__(self):
        self.pkt = []            #Defino o Saco (rsrsrs) de ceramicas
        self.adj_pkt = []        #Defina o Saco (rsrsrs) auxiliar vazio

        #Cria o *saco* com 100 ceramicas, 20 de cada cor
        for i in range(5):
            for j in range(20):
                self.pkt.append(i)

        #Embaralha o saco (rsrsrs)
        random.shuffle(self.pkt)

    """
    #  GETTERS - SETTERS - __STR__  #
    """

    def get_pocket_pkt(self):
        return self.pkt

    def get_pocket_adj_pkt(self):
        return self.adj_pkt

    def set_pocket_pkt(self, pkt):
        self.pkt = pkt

    def set_pocket_adj_pkt(self, adj_pkt):
        self.adj_pkt = adj_pkt

    def __str__(self):
        return f"SACO =  {self.pkt} \nSACO AUXILIAR = {self.adj_pkt}"


    """
    #  Funçoes de Classe  ================================================== #
    """

    """
    Entrada: Vazia 
    Saida: Vazia
    Embaralha as peças existentes no saco 
    """
    def shuffle(self):
        random.shuflle(self.pkt)

    """
    Entrada: Vazia 
    Saida: Verdadeiro para caso esteja vazio e falso senao 
    """
    def is_empty(self):
        if not self.pkt:
            return True

        return False

    """
    Entrada: Vazia 
    Saida: Vazio
    Coloca no saco as ceramicas presentes no saco auxiliar
    """
    def bag(self):
        tam = len(self.adj_pkt)
        for _ in range(tam):
            self.pkt.append(self.adj_pkt.pop(0))

#End class --------------------------------------------------------------------
