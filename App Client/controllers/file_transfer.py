import socket
import os

def enviar_arquivo(servidor_ip, servidor_porta, pasta, nome_subdiretorio):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((servidor_ip, int(servidor_porta)))
        requisicao = ''
        
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            nome_arquivo = os.path.basename(caminho_arquivo)
            
            with open(caminho_arquivo, 'r') as f: 
                conteudo_arquivo = f.read() 
            
            # Monta a requisição
            requisicao = f"{nome_subdiretorio} |||{nome_arquivo} |||{conteudo_arquivo}"
            tamanho_requisicao = len(requisicao)

            # Envia o tamanho da requisição primeiro (cabeçalho)
            s.sendall(f"{tamanho_requisicao:08}".encode('utf-8')) 
            s.sendall(requisicao.encode('utf-8'))
            
            print(f'Arquivo: {nome_arquivo} enviado com sucesso!')