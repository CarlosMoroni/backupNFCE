import socket
import os

def iniciar_servidor(ip, porta, pasta_destino):
    """
    Inicia o servidor para receber arquivos de clientes.

    ip: Endereço IP onde o servidor irá escutar.
    porta: Porta onde o servidor ficará escutando.
    pasta_destino: Pasta onde os arquivos recebidos serão salvos.
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)  # Cria a pasta de destino se não existir

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, int(porta)))  # Associa o socket ao IP e porta especificados
        s.listen()  # Coloca o servidor no modo de escuta

        print(f"Servidor escutando em {ip}:{porta}...")

        while True:
            conn, addr = s.accept()  # Aceita uma conexão de um cliente
            with conn:
                print(f"Conectado por {addr}")

                # Recebe os dados do arquivo
                dados = b""
                while True:
                    parte = conn.recv(1024)  # Recebe os dados em blocos de 1024 bytes
                    if not parte:
                        break  # Encerra quando não há mais dados
                    dados += parte

                # Salva o arquivo na pasta de destino
                nome_arquivo = os.path.join(pasta_destino, "arquivo_recebido")
                with open(nome_arquivo, 'wb') as f:
                    f.write(dados)

                print(f"Arquivo salvo em: {nome_arquivo}")