# Criando a minha mascara de acoes
import gymnasium as gym
from gymnasium import spaces

# Minhas Classes
from Ambiente.M_game_v3 import Factory_V3
from Ambiente.M_game_v3 import State_V3
from Ambiente.M_game_v3 import Player_V3
class AzulEnv(gym.Env):
    
    metadate = {"render_modes":['rgb_array','human']}

    def __init__(self, render_mode = None):
        super(AzulEnv, self).__init__()

        # Inicializar o ambiente
        self.fab = Factory_V3.Fabrica()  # Instanciar a fabrica
        self.players = [Player_V3.Jogador("AGNT"), Player_V3.Jogador("JG_00")]  # Instanciar o jogador
        self.dados = [self.fab, self.fab.pocket, self.players]
        self.estado = State_V3.Estados(self.dados)

        # Gym enviroment
        self.action_space = spaces.Discrete(180)
        self.observation_space = spaces.Box(low=-1, high=4, shape=(150,), dtype=int) # -1 (sem ceramica), 0:4 (ceramicas postas)
        self.render_mode = render_mode

        # Inicializar o estado do ambiente
        self.reset()

    '''
    Entrada: Vazia
    Saida: A observacao do estado inicial do jogo 
    Inicia um jogo do zero, com a instancia de cada classe e dos jogadores 
    '''
    def reset(self, seed=None, options=None):
        # Inicializar o ambiente
        self.fab     = Factory_V3.Fabrica()  # Instanciar a fabrica
        self.players = [Player_V3.Jogador("AGENTE"), Player_V3.Jogador("JOGADO")]  # Instanciar o jogador
        self.truncated  = False
        self.terminated = False

        # Dados iniciais do ambiente
        self.dados = [self.fab, self.fab.pocket, self.players]

        # Estado inicial do jogo
        self.estado = State_V3.Estados(self.dados)

        # Retornar a observacao inicial do ambiente
        return self.observe(), self._get_info()


    def observation(self):
        
        pass
    
    def step(self):
        
        pass
    
    def render(self):
        
        pass
    
    
    def action_masks_fn(self):
        
        pass
    