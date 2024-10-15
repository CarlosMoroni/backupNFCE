import socket  # Biblioteca para comunicação via rede (sockets)
import os

def enviar_arquivo(servidor_ip, servidor_porta, caminho_arquivo):
    """
    Conecta-se ao servidor via socket e envia um arquivo binário.

    servidor_ip: IP do servidor para onde o arquivo será enviado.
    servidor_porta: Porta do servidor.
    caminho_arquivo: Caminho do arquivo a ser enviado.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Cria o socket TCP
        s.connect((servidor_ip, int(servidor_porta)))  # Conecta ao servidor com IP e porta

        with open(caminho_arquivo, 'rb') as f:  # Abre o arquivo no modo binário para leitura
            dados = f.read()  # Lê todo o conteúdo do arquivo
            s.sendall(dados)  # Envia os dados do arquivo para o servidor

        print(f'Arquivo {os.path.basename(caminho_arquivo)} enviado com sucesso!')
