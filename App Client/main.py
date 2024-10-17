from utils.config import *
import time
from watchdog.observers import Observer
from controllers.file_transfer import *


def monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
    # event_handler.enviar_arquivos_existentes()
    
    observer = Observer()
    observer.schedule(event_handler, pasta_monitorada, recursive=True)  # Monitoramento recursivo
    observer.start()
    print('Serviço rodando!')
    try:
        while True:
            # Mantém o programa rodando
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def enviar_arquivos_existentes(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    # Itera sobre os arquivos na pasta monitorada e os envia
    for root, dirs, files in os.walk(pasta_monitorada):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            file_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
            file_handler.enviar_arquivo(caminho_arquivo)


def primeira_inicializacao(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    enviar_arquivos_existentes(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
    
def menu_principal():
    print("Escolha uma opção:")
    print("1. Primeira Inicialização")
    print("2. Modo Padrão")
    print("3. Sair")  # Você pode adicionar mais opções mais tarde

    opcao = input("Digite o número da opção desejada: ")
    return opcao


if __name__ == "__main__":
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_caixa = config['nome_caixa']
    pasta_monitorada = config['path_files']

    print(ascii_art)
    
    while True:
        opcao = menu_principal()
        
        if opcao == '1':
            primeira_inicializacao(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
        elif opcao == '2':
            monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
        elif opcao == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")