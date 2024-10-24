import socket
import os
from utils.config import salvar_nome_arquivo_auditoria
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    
    def __init__(self, servidor_ip, servidor_porta, nome_caixa, pasta_monitorada):
        self.servidor_ip = servidor_ip
        self.servidor_porta = servidor_porta
        self.nome_caixa = nome_caixa
        self.pasta_monitorada = pasta_monitorada
        self.mostrar_menu = False


    def on_created(self, event):
        # Verifica se o evento é para um arquivo (não uma pasta)
        if not event.is_directory:
            print(f'Arquivo criado: {event.src_path}')
            self.enviar_arquivo(event.src_path)


    def enviar_arquivo(self, caminho_arquivo):
        nome_arquivo = os.path.basename(caminho_arquivo)
        caminho_relativo_diretorio_alvo = os.path.relpath(caminho_arquivo, start=self.pasta_monitorada)
        caminho_completo_arquivo_diretorio_destino = self.nome_caixa + '/' + caminho_relativo_diretorio_alvo
        path_arquivo_diretorio_destino = os.path.dirname(caminho_completo_arquivo_diretorio_destino)
        
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
                requisicao = f"{path_arquivo_diretorio_destino} |||{nome_arquivo} |||".encode('utf-8') + conteudo_arquivo
                tamanho_requisicao = f"{len(requisicao):08}".encode('utf-8')
                
                # Envia o tamanho da requisição primeiro (cabeçalho)
                s.sendall(tamanho_requisicao)
                s.sendall(requisicao)
                print(f'Arquivo: {nome_arquivo} enviado com sucesso!')
                
        except FileNotFoundError as fnf_error:
            print(f"Erro: {fnf_error}")
            salvar_nome_arquivo_auditoria(caminho_arquivo)
        except PermissionError as perm_error:
            print(f"Erro de permissão ao tentar acessar o arquivo: {perm_error}")
            salvar_nome_arquivo_auditoria(caminho_arquivo)
        except ConnectionRefusedError:
            print(f"Erro: Não foi possível conectar ao servidor {self.servidor_ip}:{self.servidor_porta}")
            salvar_nome_arquivo_auditoria(caminho_arquivo)
        except socket.timeout:
            print(f"Erro: Tempo de conexão com o servidor {self.servidor_ip} esgotado.")
            salvar_nome_arquivo_auditoria(caminho_arquivo)
        except Exception as e:
            print(f"Erro inesperado ao enviar o arquivo: {e}")
            salvar_nome_arquivo_auditoria(caminho_arquivo)
        
    
    def processar_audit_txt_envia_arquivos(self, caminho_audit):
        try:
            # Ler todas as linhas do arquivo audit.txt
            with open(caminho_audit, 'r') as arquivo:
                linhas = arquivo.readlines()

            # Reescrever o arquivo removendo as linhas de arquivos enviados com sucesso
            with open(caminho_audit, 'w') as arquivo:
                for linha in linhas:
                    caminho_arquivo = linha.strip()

                    # Tenta enviar o arquivo
                    try:
                        self.enviar_arquivo(caminho_arquivo)
                        print(f"Arquivo {caminho_arquivo} enviado e removido do audit.")
                    except Exception:
                        # Se falhar, mantém a linha no arquivo
                        arquivo.write(linha)
                        print(f"Arquivo {caminho_arquivo} falhou no envio. Mantido no audit.")

        except FileNotFoundError:
            print(f"Erro: O arquivo {caminho_audit} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao processar {caminho_audit}: {e}")