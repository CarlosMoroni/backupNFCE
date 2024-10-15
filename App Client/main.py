from utils.config import *
from controllers.file_transfer import *

if __name__ == '__main__':
    # Ler as configurações do arquivo 'config.txt'
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']  # Obtém o IP do servidor
    servidor_porta = config['servidor_porta']  # Obtém a porta do servidor
    nome_subdiretorio = config['nome_subdiretorio'] # Obtem o nome do subdiretorio
    
    # Especifica o caminho da pasta que contém os arquivos a serem enviados
    pasta = config['path_files']  # Exemplo: 'C:/meus_arquivos'

    enviar_arquivo(servidor_ip, servidor_porta, pasta, nome_subdiretorio)  # Envia o arquivo
        