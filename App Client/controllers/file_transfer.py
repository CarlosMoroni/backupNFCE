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
            if not os.path.exists(caminho_arquivo):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
            
            
            if not os.access(caminho_arquivo, os.R_OK):
                raise PermissionError(f"Sem permissão de leitura para o arquivo: {caminho_arquivo}")
            
            
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
                print(f'Arquivo: {path} enviado com sucesso!')
                
        except FileNotFoundError as fnf_error:
            print(f"Erro: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Erro de permissão ao tentar acessar o arquivo: {perm_error}")
        except ConnectionRefusedError:
            print(f"Erro: Não foi possível conectar ao servidor {self.servidor_ip}:{self.servidor_porta}")
        except socket.timeout:
            print(f"Erro: Tempo de conexão com o servidor {self.servidor_ip} esgotado.")
        except Exception as e:
            print(f"Erro inesperado ao enviar o arquivo: {e}")