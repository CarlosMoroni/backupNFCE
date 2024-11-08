import os
from utils.config import *
from controllers.file_transfer import *


if __name__ == "__main__":
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_caixa = config['nome_caixa']
    pasta_monitorada = config['path_files']
    
    caminho_audit = 'audit.txt'
    event_handler = FileHandler(servidor_ip, servidor_porta, nome_caixa, pasta_monitorada)

    event_handler.monitorar_pasta()
    
    if event_handler.mostrar_menu:
        while True:
            tipo_menu = checa_arquivo_audit()
            
            if tipo_menu == True:
                menu_primeira = menu_primeira_inicializacao()

                if menu_primeira == 1:
                    os.system('cls') 
                    valor_submenu = submenu_audit_ou_primeira_inicializacao()
                    
                    if valor_submenu == 1:
                        event_handler.primeira_inicializacao_em_blocos()
                    elif valor_submenu == 2:
                        event_handler.primeira_inicializacao()
                    elif valor_submenu == 3:
                        os.system('cls') 
                            
                elif menu_primeira == 2:
                    event_handler.monitorar_pasta()
                    
                elif menu_primeira == 3:
                    event_handler.processar_audit_txt_envia_arquivos(caminho_audit)
                    event_handler.monitorar_pasta()
                
                elif menu_primeira == 4:
                    event_handler.enviar_arquivos_de_pasta_especifica()
                    event_handler.monitorar_pasta()
                    
                elif menu_primeira == 5:
                    event_handler.manda_arquivos_atualizacao_mes_e_desliga_maquina()

                elif menu_primeira == 6:
                    print("Encerrando processos...")
                    break
                
                elif menu_primeira == 404:
                    os.system('cls') 
                    print('Ação cancelada pelo sistema, use apenas as opções do menu!')
                    
                else:
                    os.system('cls') 
                    print('opção invalida, por favor selecione novamente!')
                    
            else:
                menu_demais = menu_demais_chamados()
                
                if menu_demais == 1:
                    event_handler.monitorar_pasta()
                    
                elif menu_demais == 2:
                    event_handler.processar_audit_txt_envia_arquivos(caminho_audit)
                    event_handler.monitorar_pasta()
                    
                elif menu_demais == 3:
                    event_handler.enviar_arquivos_de_pasta_especifica()
                    event_handler.monitorar_pasta()
                    
                elif menu_demais == 4:
                    event_handler.manda_arquivos_atualizacao_mes_e_desliga_maquina()
                    
                elif menu_demais == 5:
                    print("Encerrando processos...")
                    break
                
                elif menu_demais == 404:
                    os.system('cls') 
                    print('Ação cancelada pelo sistema, use apenas as opções do menu!')
                    
                else:
                    os.system('cls') 
                    print('opção invalida, por favor selecione novamente!')