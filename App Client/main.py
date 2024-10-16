from utils.config import *
import time
from watchdog.observers import Observer
from controllers.file_transfer import *


def monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_subdiretorio):
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_subdiretorio)
    observer = Observer()
    observer.schedule(event_handler, pasta_monitorada, recursive=True)  # Monitoramento recursivo

    observer.start()
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
    nome_subdiretorio = config['nome_subdiretorio']
    pasta_monitorada = config['path_files']

    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_subdiretorio)