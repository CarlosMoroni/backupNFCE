import socket
import os

def iniciar_servidor(ip, porta, pasta_destino):

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

                # Recebe o nome do subdiretório (string enviada pelo cliente)
                nome_subdiretorio = conn.recv(1024).decode('utf-8')
                print(f"Nome do subdiretório recebido: {nome_subdiretorio}")
                
                caminho_completo = os.path.join(pasta_destino, nome_subdiretorio)
                
                if not os.path.exists(caminho_completo):
                    os.makedirs(caminho_completo)
                    print(f"Subdiretório {caminho_completo} criado.")
                    
                
                dados = b"" 
                while True:
                    parte = conn.recv(1024)  # Recebe os dados em blocos de 1024 bytes
                    if not parte:
                        break  # Encerra quando não há mais dados
                    dados += parte

                # Salva o arquivo na pasta de destino
                nome_arquivo = os.path.join(caminho_completo, "arquivo_recebido")
                with open(nome_arquivo, 'wb') as f:
                    f.write(dados)

                print(f"Arquivo salvo em: {nome_arquivo}")