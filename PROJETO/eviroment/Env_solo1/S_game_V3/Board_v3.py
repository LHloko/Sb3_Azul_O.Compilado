#Start class ------------------------------------------------------------------
class Board():

    def __init__(self, name):
        self.floor = []     #Piso do tabuleiro
        self.wall = []      #Parede de ceramica
        self.pattern = []   #Parede adjacente
        self.trash = []     #Lixo do tabuleiro
        self.name_player = name

        #Construindo a parede
        for i in range(5):
            line = []
            for j in range(5):
                cor = (i-j)%5
                line.append([cor, False])
            self.wall.append(line)

        #Construindo a parede adjacente
        for i in range(5):
            line = []
            for j in range(i+1):
                line.append(['',False])
            self.pattern.append(line)

        #Construindo o piso
        self.floor = [-1,False],[-1,False],[-2,False],[-2,False],[-2,False],[-3,False],[-3,False]

    """
    #  GETTERS - SETTERS - __STR__  #
    """
    def get_wall(self):
        return self.wall

    def get_floor(self):
        return self.floor

    def get_trash(self):
        return self.trash

    def get_pattern(self, line=None):
        if line is None:
            return self.pattern
        else:
            return self.pattern[line]

    def set_wall(self, wll):
        self.wall = wll

    def set_floor(self, flr):
        self.floor = flr

    def set_pattern(self, ptr):
        self.pattern = ptr

    def __str__(self):
        return f"""
TABULEIRO do {self.name_player}: 
-----------------------------------------------------------------------------------------------------------------------------------*
{self.wall[0]}  <  {self.pattern[0]}
{self.wall[1]}  <  {self.pattern[1]}
{self.wall[2]}  <  {self.pattern[2]}
{self.wall[3]}  <  {self.pattern[3]}
{self.wall[4]}  <  {self.pattern[4]}
-----------------------------------------------------------------------------------------------------------------------------------*                  
{self.floor}

Lixo do tabuleiro:
{self.trash}
"""

    """
    #  Funçoes de Classe  ================================================== #
    """

    '''
    Entrada: list de ceramicas tiles
    Saida: Vazio 
    Pega a list tiles e coloca no piso, caso exceda envia para o lixo
    '''
    def cement_floor(self, tiles):
        flr = self.floor

        #Pega o indice que tem posiçao livre
        idx = 0
        while flr[idx][1] == True:
            idx += 1
            if idx > 6:
                break

        #Colocar as ceramicas
        for i in range(idx,len(tiles)+idx):
            if i<7: #Nao extrapolou o piso
                flr[i][0] = tiles.pop(0)
                flr[i][1] = True
            else: #Piso estourado
                self.trash.append(tiles.pop())


    '''
    Entrada: list de ceramicas tiles, e linha adjancente line
    Saida: Verdadeiro caso inserido, falso senao
    Pega a list tiles e coloca no piso, caso exceda envia para o lixo
    '''
    def cement_line(self, tiles, line):
        # Se passar um valor invalido
        if line< 0 or line >5:
            return False

        #se tiver o -1
        self.is_tile_um(tiles)

        #se escolhido o piso
        if line == 5:
            self.cement_floor(tiles)
            return True

        #se escolhido uma linha adjacente
        ln_adj = self.pattern[line]
        cor = tiles[0]
        cpv = self.how_is_full_line(line)
        rest = []

        #verifica se ja tem ceramica na parede
        if self.wall_grouted(cor, line):
            print("ceramica ja esta na parede! ")
            return False

        #verificar se a linha esta cheia
        if cpv == -2:
            print("linha cheia [!]")
            return False

        #colocar os tijolos em uma linha parcialmente cheia de mesma cor 
        if cpv == -1:
            #pega o indice que tem posiçao livre
            idx = 0
            while ln_adj[idx][1] == True:
                idx += 1

            #meter os tijolos na linha
            for i in range(idx, len(tiles)):
                if i < len(ln_adj):
                    ln_adj[i][0] = tiles.pop()
                    ln_adj[i][1] = True

                else: #linha estourada
                    rest.append(tiles.pop())

            self.cement_floor(rest)

            return True

        if cpv == cor:
            idx = 0
            while ln_adj[idx][1] == True:
                idx += 1

            #meter os tijolos na linha
            for i in range(idx, idx+len(tiles)):
                if i < len(ln_adj):
                    ln_adj[i][0] = tiles.pop()
                    ln_adj[i][1] = True

                else: #linha estourada
                    rest.append(tiles.pop())

            self.cement_floor(rest)

            return True

        #verificar se a linha esta com outra cor
        if cpv != cor:
            print("linha ja contem ceramicas de outra cor [!]")
            return False

    '''
    Entrada: Vazia  
    Saida: Verdadeiro caso todas estejam as linhas estejam cheias e falso senao 
    '''
    def all_lines_full(self):
        for i in range(5):
            if self.how_is_full_line(i) != -2:
                return False

        return True


    '''
    Entrada: List tiles com as ceramicas pegas
    Saida: Retorna Verdadeiro se tiles conter o -1 e falso senao 
    Verifica se a tiles contem o -1 se tiver o coloca no piso 
    caso o piso esteja cheio, envia a peça do inicio para o lixo do tabuleiro
    senao estiver cheio coloca a peça no fim do piso e -1 no começo
    '''
    def is_tile_um(self, tiles):
        flr = self.floor

        #Verifica se o -1 exite na primeira posiçao do tiles
        if tiles[0] == -1:

            #Verifica se o piso ja esta cheio
            if flr[6][1] == True:
                self.trash.append(flr[0][0])

            else:
                idx = 0
                while flr[idx][1] == True:
                    idx += 1

                flr[idx][0] = flr[0][0]
                flr[idx][1] = True

            #Coloca o -1 na posiçao inicial
            flr[0][0] = tiles.pop(0)
            flr[0][1] = True

            return True

        else:
            return False


    '''
    Entrada: A linha escolhida 'line' a se por ceramicas
    Saida: -1 para linha vazia, -2 linha completamente cheia e o valor da cor 
            se preenchida parcialmente
    '''
    def how_is_full_line(self, line):
        flr = self.pattern[line]

        #Verifica se esta vazia
        if flr[0][1] == False:
            return -1

        #Verifica se esta completamente cheia
        if flr[line][1] == True:
            return -2

        #Retorna o valor da cor ja presente
        return flr[0][0]

###############################################################################

    '''
    Entrada: Vazia 
    Saida: 
    '''
    def emparedar(self):
        '''
        # Verificas linha por linha, qual esta completa
        # Preencher na parede a linha completa 
        # Somar os pontos gerados nessa alocaçao 
        # Jogar no lixo as ceramicas sobressalentes 
        '''
        pontos = 0
        pontos_agnt = 0

        for l in range(5):
            if self.line_adj_is_full(l):
                pontos += 1
                pontos_agnt += 1

                #cor da ceramica a ser colocada na parede
                cor = self.pattern[l][0][0]

                #encontrar a linha e a coluna na parede que tem a cor e meter
                w = self.wall[l]
                column = 0
                for clm in w:
                    if clm[0] == cor:
                        column = w.index(clm)
                        clm[1] = True
                        break

                #Somar os pontos
                pontos += self.somar_ceramicas(l, column)
                pontos_agnt += self.pontuar_recompensa(l, column)

                #Resetar as posiçoes e manda pro lixo
                pattern = self.get_pattern(l)

                for cell in pattern:
                    cell[0] = ''
                    cell[1] = False

                for _ in range(len(pattern) - 1):
                    self.trash.append(cor)

        return [pontos, pontos_agnt]


    '''
    Entrada: Linha adjacente
    Saida: Verdadeiro se a linha adjacente estiver cheia, falso senao
    '''
    def line_adj_is_full(self, line):
        line_adj = self.pattern[line]
        last_pos = len(line_adj)-1

        if line_adj[last_pos][1] == True:
            return True
        else:
            return False


    '''
    Entrada: linha e coluna da parede onde foi posto uma ceramica 
    Saida: Quantidade de ceramicas adjacentes a esta, na horizontal e vertical
    '''
    def somar_ceramicas(self, line, column):
        wall = self.wall
        pontos = 0

        l = line
        c = column

        #andar para cima
        while l > 0:
            cel_cima = wall[l-1][c]

            if cel_cima[1] == True:
                pontos += 1
                l = l-1
            else:
                break

        l = line
        #andar para baixo
        while l < 4:
            cel_baixo = wall[l+1][c]

            if cel_baixo[1] == True:
                pontos += 1
                l = l+1
            else:
                break

        l = line
        c = column
        #andar para tras
        while c > 0:
            cel_tras = wall[l][c-1]

            if cel_tras[1] == True:
                pontos += 1
                c = c-1
            else:
                break

        c = column
        #andar para frente
        while c < 4:
            cel_frente = wall[l][c+1]

            if cel_frente[1] == True:
                pontos += 1
                c = c+1
            else:
                break

        #retornar os pontos
        return pontos


    '''
    Entrada: Vazia 
    Saida: Quantidade de pontos negativos oriundos do piso 
    '''
    def des_somar_ceramicas(self):
        floor = self.floor
        count = 0
        pontos = 0

        #calcula os pontos a serem decrescentados e reseta o piso
        for f in floor:
            if f[1]:
                self.trash.append(f[0])
                f[1] = False

                if count < 2:
                    f[0] = -1
                    pontos += 1

                elif count < 4:
                    f[0] = -2
                    pontos += 2

                elif count < 7:
                    f[0] = -3
                    pontos += 3

                count +=1
            else:
                return pontos

        return pontos

    '''
    Entrada: Cor da ceramica e linha adjacente 
    Saida: Verdadeiro caso a ceramica da cor passada ja esteja na parede e 
    falso senao
    '''
    def wall_grouted(self, color, line):
        wall = self.wall[line]

        for w in wall:
            if w[0] == color:
                if w[1] == True:
                    return True

        return False


    '''
    Entrada: Vazio 
    Saida: Verdadeiro para caso a linha venha a ser completada e falso senao
    '''
    def is_last_round(self):

        full_lines = []
        for l in range(5):
            if self.line_adj_is_full(l):
                full_lines.append(l)

        for fl in full_lines:
            if self.how_many_tiles(fl) == 1:
                return True

        return False


    '''
    Entrada: linha da matriz de ceramicas
    Saida: quantidade de ceramicas que faltam para que a linha fique cheia
    '''
    def how_many_tiles(self, line):
        wall = self.wall[line]
        lack = 0

        for w in wall:
            if w[1] == False:
                lack += 1
        return lack



    '''
    Entrada: Vazia
    Saida: Verdadeiro caso alguma linha da parede esteja cheia 
    '''
    def is_line_wall_full(self):
        wall = self.wall

        for line_wall in wall:
            count = 0
            for cell in line_wall:
                if cell[1] == False:
                    count += 1

            if count == 0:
                return True

        return False


    '''
    Entrada: Vazia 
    Saida: Vazia 
    Calcula a pontuaçao no final do jogo 
    '''
    def last_pontuar(self):
        pontos = 0
        wall = self.wall

        #somar na horizontal
        for line_wall in wall:
            count = 0
            for cell in line_wall:
                if cell[1] == False:
                    count += 1

            if count == 0:
                pontos += 2


        #somar na vertical
        for c in range(5):
            count = 0
            for line_wall in wall:
                if line_wall[0][1] == False:
                    count += 1
            if count == 0:
                pontos += 7

        #somar diagonal

            #amarelo 01
        if wall[4][0][1] == True:
            pontos += 10

            #vermelho 01
        red_01 = [wall[3][0][1], wall[4][1][1]]
        if all(red_01):
            pontos += 10

            #preto 01
        blck_01 = [wall[2][0][1], wall[3][1][1], wall[4][2][1]]
        if all(blck_01):
            pontos += 10

            #branco 01
        brc_01 = [wall[4][3][1], wall[3][2][1], wall[2][1][1], wall[1][0][1]]
        if all(brc_01):
            pontos += 10

            #azul mid
        perfect_blue = [wall[0][0][1], wall[1][1][1], wall[2][2][1], wall[3][3][1], wall[4][4][1]]
        if all(perfect_blue):
            print("perfect blue ")
            pontos += 10

            #amarelo 02
        yel_01 = [wall[3][4][1], wall[2][3][1], wall[1][2][1], wall[0][1][1]]
        if all(yel_01):
            pontos += 10

            #vermelho 02
        red_02 = [wall[2][4][1], wall[1][3][1], wall[0][2][1]]
        if all(red_02):
            pontos += 10

            #preto 02
        blck_02 = [wall[1][4][1], wall[0][3][1]]
        if all(blck_02):
            pontos += 10

            #branco 02
        if wall[0][4][1] == True:
            pontos += 10

        return pontos

    '''
    Entrada: Vazia 
    Saida: Vazia 
    Calcula a pontuaçao no final do jogo para a recompensa do agente
    '''
    def pontuar_recompensa(self, line, column):
        wall = self.wall
        pontos = 0

       # Função auxiliar para somar pontos em uma direção específica
        def contar_ceramicas(l, c, delta_l, delta_c):
            pontos_direcao = 0
            while 0 <= l < 5 and 0 <= c < 5:
                if wall[l][c][1] == True:
                    pontos_direcao += 1
                else:
                    break
                l += delta_l
                c += delta_c
            return pontos_direcao
    
        # Somar pontos nas quatro direções a partir da célula (line, column)
        pontos += contar_ceramicas(line - 1, column, -1, 0)  # Para cima
        pontos += contar_ceramicas(line + 1, column, 1, 0)   # Para baixo
        pontos += contar_ceramicas(line, column - 1, 0, -1)  # Para esquerda
        pontos += contar_ceramicas(line, column + 1, 0, 1)   # Para direita


        # Verificar linha horizontal completa
        if all(cell[1] == True for cell in wall[line]):
            pontos += 2
    
        # Verificar coluna vertical completa
        if all(wall[i][column][1] == True for i in range(5)):
            pontos += 7
    
        # Verificar padrões diagonais relacionados à jogada
        # Checar qual diagonal a jogada pode ter completado
    
        # Diagonal principal (canto superior esquerdo ao inferior direito)
        if line == column:
            if all(wall[i][i][1] == True for i in range(5)):
                pontos += 10
    
        # Diagonal secundária (canto superior direito ao inferior esquerdo)
        if line + column == 4:
            if all(wall[i][4-i][1] == True for i in range(5)):
                pontos += 10


        #retornar os pontos
        return pontos

#End class --------------------------------------------------------------------


