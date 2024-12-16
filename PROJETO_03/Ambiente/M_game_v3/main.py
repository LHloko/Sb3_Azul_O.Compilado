import Factory_V3 as Factories
import Player_V3 as Player
import State_V3 as States

from Enviroment import Step_02 as stp
from Enviroment import Env as en
from Enviroment import Observation as obs

#Start class ------------------------------------------------------------------
def main():

    # Instancio uma fabrica
    fab = Factories.Fabrica()

    # Instancio os jogadores
    players = [Player.Jogador('Agente'), Player.Jogador('DL')]

    # Crio uma tupla com os dados do jogo
    dados = [fab, fab.pocket, players]

    # Instancio o Estado de jogo
    estado = States.Estados(dados)
    
    env = en.AzulEnv()  

    for i in range(5):
        env.render()
        
        #print(env.action_masks_fn())
        
        #atc = input()
        
        print(env.step(1))
        env.render()
        print(i)
    return 
    
    fab.roubar()
    players[0].board.roubar()
    print(fab)
    
    players[0].board.roubar()
    print(players[0])
    
    print(stp.valid_lines_01(dados,1))
    return 0
    
    
    while not estado.is_game_over():
        #start do game
        while not estado.fim_de_turno():
            for p in players:
                                
                for i in range(5):
                    print(fab)
                    stp.step(0, dados, estado)
                    print(players[0])
                    print(players[1])
                
                pass
                #print(fab)
                #print(obs.action_masks_fn(dados))
                return 0

                if fab.is_board_empty() and fab.is_floor_empty():#caso o jogo termine no meio de um dos jogadores
                    break
                print("------------------------------------------------------------------------------------------------*")

                print(fab)
                print(p)

                jogada = []
                jogada.append(int(input('Escolha onde pegar ceramicas\n-> [0 - 4] Fabricas\n-> [5] Chao de fabrica\n')))
                jogada.append(int(input('Escolha a ceramica\n')))
                jogada.append(int(input('Escolha onde por as ceramicas\n-> [0 - 4] Linhas adjacentes\n-> [5] Piso do tabuleiro\n')))

                p.playar(fab, jogada)
                print(p)

                print("-----------------------------------------------------------------------------------------------------------------------------------*")
                if estado.is_last_round_to_end():
                    print("-----------------------------------------------------------------------------------------------------------------------------------*")
                    print(" *** ULTIMA RODADA ANTES DO FIM DO JOGO *** ")
                    print('                 :D ')
                    print("-----------------------------------------------------------------------------------------------------------------------------------*")

        #Colocar o player com o -1 no inicio da lista de jogadores
        estado.first_player()

        #final do turno
        print("-----------------------------------------------------------------------------------------------------------------------------------*")
        print("       Fim Da Rodada")
        print("-----------------------------------------------------------------------------------------------------------------------------------*")
        estado.game_player_status()
        estado.get_states()

        print("-----------------------------------------------------------------------------------------------------------------------------------*")
        print("       NOVA Rodada")
        print("-----------------------------------------------------------------------------------------------------------------------------------*")
        estado.iniciar_turno()

    #Concluindo o JOGO
    estado.fim_de_jogo()

#End class --------------------------------------------------------------------


if __name__ == "__main__":
    main()
