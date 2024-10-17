import socket
import os

def iniciar_servidor(ip, porta, pasta_destino):

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, int(porta)))
        s.listen()
        
        print(f"Servidor escutando em {ip}:{porta}...")

        while True:
            conn, addr = s.accept()
            
            with conn:
                print(f"Conectado por {addr}")
                
                tamanho_total_raw = conn.recv(8).decode('utf-8')

                # Valida se o tamanho recebido é um número
                if not tamanho_total_raw.strip().isdigit():
                    print(f"Erro ao receber tamanho da requisição. Recebido: {tamanho_total_raw}")
                    return
                
                tamanho_total = int(tamanho_total_raw)

                dados_recebidos = b""
                while len(dados_recebidos) < tamanho_total:
                    parte = conn.recv(1024)
                    if not parte:
                        break
                    dados_recebidos += parte

                requisicao = dados_recebidos.decode('utf-8')

                arrayDataRequisicao = requisicao.split('|||')

                nome_subdiretorio, nome_arquivo, dados_arquivo = arrayDataRequisicao
                nome_subdiretorio = nome_subdiretorio.strip()
                nome_arquivo = nome_arquivo.strip()
                dados_arquivo = dados_arquivo.strip()

                # print(f"Nome do subdiretório: {nome_subdiretorio}")
                # print(f"Nome do arquivo: {nome_arquivo}")
                # print(f"Dados do arquivo: {dados_arquivo[50]}...")  # Exibe apenas os primeiros 50 caracteres dos dados

                # Salva o arquivo na pasta de destino
                caminho_completo = os.path.join(pasta_destino, nome_subdiretorio)
                
                if not os.path.exists(caminho_completo):
                    os.makedirs(caminho_completo)
                    print(f"Subdiretório: {caminho_completo} criado.")
                    
                caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)
                with open(caminho_arquivo, 'w') as f:
                    f.write(dados_arquivo)

                print(f"Arquivo salvo em: {caminho_arquivo}")