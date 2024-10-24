import time
import os
import keyboard
from utils.config import *
from watchdog.observers import Observer
from controllers.file_transfer import *

mostrar_menu = False

def monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
    
    observer = Observer()
    observer.schedule(event_handler, pasta_monitorada, recursive=True)  # Monitoramento recursivo
    observer.start()
    
    os.system('cls')
    print(ascii_art)
    print('Cliente rodando! \n(Mantenha precionado ctrl + alt + F12 para abrir o menu de Administrador)')
    
    try:
        while True:
            time.sleep(0.5) # Mantém o programa rodando
            
            #verifica se a tecla 'd' foi precionanda
            if keyboard.is_pressed('ctrl+alt+f12'):
                global mostrar_menu
                mostrar_menu = True
                observer.stop()
                break
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def enviar_arquivos_existentes(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    # Itera sobre os arquivos na pasta monitorada e os envia
    for root, dirs, files in os.walk(pasta_monitorada):
        for item in files:
            caminho_arquivo = os.path.join(root, item)
            file_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
            file_handler.enviar_arquivo(caminho_arquivo)
            time.sleep(0.1)
        
            
def enviar_arquivos_existentes_em_blocos(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    blocos = int(input("Quantos arquivos por vez deseja enviar?\n"))
    pausa = int(input("Quantos segundos em cada execução?\n"))
    contador = 0
    
    file_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)
    
    for root, dirs, files in os.walk(pasta_monitorada):
        for item in files:
            caminho_arquivo = os.path.join(root, item)
            file_handler.enviar_arquivo(caminho_arquivo)
            contador += 1
            time.sleep(0.1)
            if contador % blocos == 0:
                print(f"\nPausa de {pausa} segundos após o envio de {blocos} arquivos...")
                time.sleep(pausa)
    print("Envio de todos os arquivos concluído.")


def primeira_inicializacao(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    enviar_arquivos_existentes(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)


def primeira_inicializacao_em_blocos(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa):
    enviar_arquivos_existentes_em_blocos(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)


if __name__ == "__main__":
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_caixa = config['nome_caixa']
    pasta_monitorada = config['path_files']
    
    caminho_audit = 'audit.txt'
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)

    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
    
    if mostrar_menu:
        while True:
            tipo_menu = checa_arquivo_audit()
            
            if tipo_menu == True:
                menu_primeira = menu_primeira_inicializacao()

                if menu_primeira == 1:
                    os.system('cls') # limpa o console
                    valor_submenu = submenu_audit_ou_primeira_inicializacao()
                    
                    if valor_submenu == 1:
                        primeira_inicializacao_em_blocos(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
                    elif valor_submenu == 2:
                        primeira_inicializacao(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
                    elif valor_submenu == 3:
                        os.system('cls') # limpa o console
                            
                elif menu_primeira == 2:
                    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
                    
                elif menu_primeira == 3:
                    event_handler.processar_audit_txt_envia_arquivos(caminho_audit)
                    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
                    
                elif menu_primeira == 4:
                    print("Encerrando processos...")
                    break
                
                elif menu_primeira == 404:
                    os.system('cls') # limpa o console
                    print('Ação cancelada pelo sistema, use apenas as opções do menu!')
                    
                else:
                    os.system('cls') # limpa o console
                    print('opção invalida, por favor selecione novamente!')
                    
            else:
                menu_demais = menu_demais_chamados()
                
                if menu_demais == 1:
                    monitorar_pasta(servidor_ip, servidor_porta, pasta_monitorada, nome_caixa)
                    
                elif menu_demais == 2:
                    event_handler.processar_audit_txt_envia_arquivos(caminho_audit)
                    
                elif menu_demais == 3:
                    print("Encerrando processos...")
                    break
                
                elif menu_demais == 404:
                    os.system('cls') # limpa o console
                    print('Ação cancelada pelo sistema, use apenas as opções do menu!')
                    
                else:
                    os.system('cls') # limpa o console
                    print('opção invalida, por favor selecione novamente!')