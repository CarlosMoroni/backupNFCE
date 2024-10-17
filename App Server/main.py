from utils.config import *
from controllers.init_server import *


if __name__ == '__main__':
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta']
    pasta_destino = config['pasta_destino']
    
    print(ascii_art)
    # Inicia o servidor com os valores lidos do arquivo de configuração
    iniciar_servidor(servidor_ip, servidor_porta, pasta_destino)