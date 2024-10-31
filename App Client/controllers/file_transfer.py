import socket
import os
import time
import keyboard
from utils.config import *
from watchdog.observers import Observer
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

                # Aguarda a resposta do servidor
                resposta = s.recv(7).decode('utf-8') 
                if resposta == "ERROR":
                    salvar_nome_arquivo_auditoria(caminho_arquivo)  # Salva o caminho em audit.txt
                else:
                    print(f'Arquivo: {nome_arquivo} enviado com sucesso!')
                
                time.sleep(0.1)
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

    
    def monitorar_pasta(self):
        observer = Observer()
        observer.schedule(self, self.pasta_monitorada, recursive=True)  # Monitoramento recursivo
        observer.start()

        os.system('cls')
        print(ascii_art)
        print('Cliente rodando! \n(Mantenha precionado ctrl + alt + F12 para abrir o menu de Administrador)')

        try:
            while True:
                time.sleep(0.5) # Mantém o programa rodando

                #verifica se a tecla 'd' foi precionanda
                if keyboard.is_pressed('ctrl+alt+f12'):
                    self.mostrar_menu = True
                    observer.stop()
                    break
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    
    def enviar_arquivos_existentes(self):
        # Itera sobre os arquivos na pasta monitorada e os envia
        for root, dirs, files in os.walk(self.pasta_monitorada):
            for item in files:
                caminho_arquivo = os.path.join(root, item)
                self.enviar_arquivo(caminho_arquivo)
    
    
    def enviar_arquivos_existentes_em_blocos(self):
        try:
            blocos = int(input("Quantos arquivos por vez deseja enviar?\n"))
            pausa = int(input("Quantos segundos em cada execução?\n"))
        except ValueError as erro:
            print(f'#############################################################')
            print(f'Erro de execução do codigo, por favor digite valores corretos')
            print(f'#############################################################')
            self.enviar_arquivos_existentes_em_blocos()
            
        
        contador = 0

        for root, dirs, files in os.walk(self.pasta_monitorada):
            for item in files:
                caminho_arquivo = os.path.join(root, item)
                self.enviar_arquivo(caminho_arquivo)
                contador += 1

                if contador % blocos == 0:
                    print(f"\nPausa de {pausa} segundos após o envio de {blocos} arquivos...")
                    time.sleep(pausa)
        print("Envio de todos os arquivos concluído.")
    
    
    def primeira_inicializacao(self):
        self.enviar_arquivos_existentes()
        self.monitorar_pasta()

    
    def primeira_inicializacao_em_blocos(self):
        self.enviar_arquivos_existentes_em_blocos()
        self.monitorar_pasta()
    
        
    def processar_audit_txt_envia_arquivos(self, caminho_audit):
        try:
            with open(caminho_audit, 'r') as arquivo:
                linhas = arquivo.readlines()

            with open(caminho_audit, 'w') as arquivo:
                for linha in linhas:
                    caminho_arquivo = linha.strip()
                    
                    # Tenta enviar o arquivo
                    try:
                        self.enviar_arquivo(caminho_arquivo)
                        print(f"Arquivo {caminho_arquivo} enviado e removido do audit.")
                        
                    except Exception as e:
                        arquivo.write(linha)
                        print(f"Arquivo {caminho_arquivo} falhou no envio. Mantido no audit. ERROR: {e}")
                        continue
                
                print('\n\n  PROCESSO FINALIZADO!')
                time.sleep(3)
                self.monitorar_pasta()
                    

        except FileNotFoundError:
            print(f"Erro: O arquivo {caminho_audit} não foi encontrado.")
        except Exception as e:
            print(f"Erro ao processar {caminho_audit}: {e}")
    
    
    def enviar_arquivos_de_pasta_especifica(self):
        """
        Envia arquivos de uma pasta específica. Pode incluir ou excluir subpastas.

        Args:
            pasta (str): Caminho da pasta para enviar arquivos.
            incluir_subpastas (bool): Se True, envia arquivos também das subpastas.
        """
        try:
            pasta_value = input("Qual a pasta que deseja enviar?\n")
            incluir_subpastas_value = int(input("Executar envios de subpastas?, digite 1 para sim e qualquer outro para nao!\n"))
        except ValueError as erro:
            print(f'\n#############################################################')
            print(f'Erro de execução do codigo, por favor digite valores corretos')
            print(f'#############################################################\n')
            self.enviar_arquivos_de_pasta_especifica()
            
        pasta = self.pasta_monitorada + '/' + pasta_value
        
        if incluir_subpastas_value == 1:
            incluir_subpastas = True
        else:
            incluir_subpastas = False   
        
        for root, dirs, files in os.walk(pasta):
            try:
                if incluir_subpastas == False and root != pasta:
                    continue  # Ignora subpastas se incluir_subpastas for False
                
                for item in files:
                    caminho_arquivo = os.path.join(root, item)
                    self.enviar_arquivo(caminho_arquivo)

            except Exception as e:
                print(f'Erro na execução da função, ERRO: {e}')
    
          
    def enviar_a_partir_da_pasta(self):
        """
        Envia arquivos a partir de uma pasta específica e continua enviando 
        em todos os diretórios subsequentes da `pasta_monitorada`.

        Args:
            pasta_inicio (str): Caminho da pasta de início do envio.
        """
        enviar = False
        pasta_inicio_value = input('A partir de qual pasta deseja enviar?\n')
        pasta_inicio = self.pasta_monitorada + '/' + pasta_inicio_value
        
        # Percorre todos os diretórios e arquivos dentro de `self.pasta_monitorada`
        for root, dirs, files in os.walk(self.pasta_monitorada):

            # Verifica se estamos na pasta de início ou se já começamos o envio
            if root == pasta_inicio or enviar:
                enviar = True  # Marca que estamos enviando a partir de agora

                for item in files:
                    caminho_arquivo = os.path.join(root, item)
                    self.enviar_arquivo(caminho_arquivo)
