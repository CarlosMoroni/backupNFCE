import socket
import os

def iniciar_servidor(ip, porta, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, int(porta)))
        s.listen(50)
        print(f"Servidor escutando em {ip}:{porta}...")

        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Conectado por {addr}")
                    
                    # Recebe o tamanho da requisição
                    try:
                        tamanho_total_raw = conn.recv(8).decode('utf-8')
                        
                        if not tamanho_total_raw.strip().isdigit():
                            print(f"Erro ao receber tamanho da requisição. Recebido: {tamanho_total_raw}")
                            conn.sendall(b"ERROR")
                            continue
                        
                        tamanho_total = int(tamanho_total_raw)
                    except Exception as e:
                        print(f"Erro ao processar o tamanho da requisição: {e}")
                        conn.sendall(b"ERROR")
                        continue

                    # Recebe os dados
                    dados_recebidos = b""
                    while len(dados_recebidos) < tamanho_total:
                        parte = conn.recv(1024)
                        if not parte:
                            break
                        dados_recebidos += parte

                    # Processa a requisição
                    try:    
                        requisicao = dados_recebidos.decode('utf-8', errors='ignore')
                        arrayDataRequisicao = requisicao.split('|||')
                        
                        nome_subdiretorio, nome_arquivo, dados_arquivo = arrayDataRequisicao
                        nome_subdiretorio = nome_subdiretorio.strip()
                        nome_arquivo = nome_arquivo.strip()
                        dados_arquivo = dados_arquivo.strip()
                        
                        caminho_completo = os.path.join(pasta_destino, nome_subdiretorio)
                        
                        if not os.path.exists(caminho_completo):
                            os.makedirs(caminho_completo)
                            print(f"Subdiretório: {caminho_completo} criado.")
                            
                        caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)
                        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                            f.write(dados_arquivo)

                        print(f"Arquivo salvo em: {caminho_arquivo}")
                        conn.sendall(b"SUCCESS")
                    
                    except Exception as e:
                        print(f"Erro ao processar a requisição: {e}")
                        conn.sendall(b"ERROR")
                        continue
            except Exception as e:
                print(f"Erro inesperado: {e}")
                continue
            except UnicodeDecodeError as e:
                print(f"Erro ao decodificar os dados recebidos: {e}")
                continue