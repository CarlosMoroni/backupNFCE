from utils.config import *
from controllers.init_server import *


if __name__ == '__main__':
    config = ler_configuracoes()

    # Inicia o servidor com os valores lidos do arquivo de configuração
    iniciar_servidor(config['servidor_ip'], config['servidor_porta'], config['pasta_destino'])