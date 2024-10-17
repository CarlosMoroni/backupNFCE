from utils.config import *
import time
from watchdog.observers import Observer
from controllers.file_transfer import *


def monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
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

if __name__ == "__main__":
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_caixa = config['nome_caixa']
    pasta_monitorada = config['path_files']

    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)