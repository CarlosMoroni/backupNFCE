import socket
import os
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, servidor_ip, servidor_porta, nome_subdiretorio):
        self.servidor_ip = servidor_ip
        self.servidor_porta = servidor_porta
        self.nome_subdiretorio = nome_subdiretorio

    def on_created(self, event):
        # Verifica se o evento é para um arquivo (não uma pasta)
        if not event.is_directory:
            print(f'Arquivo criado: {event.src_path}')
            self.enviar_arquivo(event.src_path)

    def enviar_arquivo(self, caminho_arquivo):
        # Obtém o nome do arquivo e o caminho relativo
        nome_arquivo = os.path.basename(caminho_arquivo)
        caminho_relativo = os.path.relpath(caminho_arquivo, start=os.path.dirname(caminho_arquivo))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.servidor_ip, int(self.servidor_porta)))
            with open(caminho_arquivo, 'r') as f:
                conteudo_arquivo = f.read()

            # Monta a requisição com o caminho relativo
            requisicao = f"{self.nome_subdiretorio} |||{caminho_relativo} |||{conteudo_arquivo}"
            tamanho_requisicao = len(requisicao)

            # Envia o tamanho da requisição primeiro (cabeçalho)
            s.sendall(f"{tamanho_requisicao:08}".encode('utf-8'))
            s.sendall(requisicao.encode('utf-8'))

            print(f'Arquivo: {caminho_relativo} enviado com sucesso!')