import socket
import os
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, servidor_ip, servidor_porta, nome_caixa, pasta_monitorada):
        self.servidor_ip = servidor_ip
        self.servidor_porta = servidor_porta
        self.nome_caixa = nome_caixa
        self.pasta_monitorada = pasta_monitorada

    def on_created(self, event):
        # Verifica se o evento é para um arquivo (não uma pasta)
        if not event.is_directory:
            print(f'Arquivo criado: {event.src_path}')
            self.enviar_arquivo(event.src_path)

    def enviar_arquivo(self, caminho_arquivo):
        nome_arquivo = os.path.basename(caminho_arquivo)
        caminho_relativo = os.path.relpath(caminho_arquivo, start=self.pasta_monitorada)
        caminho_completo = self.nome_caixa + '/' + caminho_relativo
        path= os.path.dirname(caminho_completo)
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.servidor_ip, int(self.servidor_porta)))
                
                # Abre o arquivo em modo binário
                with open(caminho_arquivo, 'rb') as f:
                    conteudo_arquivo = f.read()

                # Monta a requisição com o caminho relativo
                requisicao = f"{path} |||{nome_arquivo} |||".encode('utf-8') + conteudo_arquivo
                tamanho_requisicao = f"{len(requisicao):08}".encode('utf-8')
                
                # Envia o tamanho da requisição primeiro (cabeçalho)
                s.sendall(tamanho_requisicao)
                s.sendall(requisicao)
                print('tamanho do envio ', f"{tamanho_requisicao}")

                print(f'Arquivo: {path} enviado com sucesso!')
        
        except PermissionError:
            print(f"Erro de permissão ao tentar acessar o arquivo: {caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao enviar o arquivo: {e}")