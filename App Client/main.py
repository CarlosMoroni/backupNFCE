from utils.config import *
from controllers.file_transfer import *

if __name__ == '__main__':
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_subdiretorio = config['nome_subdiretorio']
    
    pasta = config['path_files']

    enviar_arquivo(servidor_ip, servidor_porta, pasta, nome_subdiretorio)
        