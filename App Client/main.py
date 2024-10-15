from utils.config import *
from controllers.file_transfer import *

if __name__ == '__main__':
    # Ler as configurações do arquivo 'config.txt'
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']  # Obtém o IP do servidor
    servidor_porta = config['servidor_porta']  # Obtém a porta do servidor
    
    # Especifica o caminho da pasta que contém os arquivos a serem enviados
    pasta = config['path_files']  # Exemplo: 'C:/meus_arquivos'

    # Percorre todos os arquivos da pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)  # Concatena a pasta com o nome do arquivo
        enviar_arquivo(servidor_ip, servidor_porta, caminho_arquivo)  # Envia o arquivo
        