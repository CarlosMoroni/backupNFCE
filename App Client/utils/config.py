import os
import ctypes

caminho_txt_audit = "audit.txt"

# Função para ler o arquivo de configuração
def ler_configuracoes():
    configuracoes = {}  
    with open('config.cliente.txt', 'r') as arquivo:  # Abre o arquivo de configuração
        for linha in arquivo:  # Percorre cada linha do arquivo
            chave, valor = linha.strip().split(': ')  # Divide a linha em chave e valor
            configuracoes[chave] = valor  # Armazena no dicionário
    return configuracoes  # Retorna o dicionário com as configurações


def captura_dados_config_cliente_txt():
    config = ler_configuracoes()
    servidor_ip = config['servidor_ip']
    servidor_porta = config['servidor_porta'] 
    nome_caixa = config['nome_caixa']
    pasta_monitorada = config['path_files']
    
    return servidor_ip, servidor_porta, nome_caixa, pasta_monitorada 


def menu_primeira_inicializacao():
    print("\nEscolha uma opção:")
    print("1. Primeira Inicialização")
    print("2. Modo Padrão")
    print("3. Auditoria")
    print("4. Envio de pasta especifica")
    print("5. Envio de pasta especifica e desligamento do computador")
    print("6. Sair")
    
    opcao = input("Digite o número da opção desejada: ")
    try:
        numero = int(opcao)
        return numero
    except ValueError:
        return 404


def menu_demais_chamados():
    print("\nEscolha uma opção:")
    print("1. Modo Padrão")
    print("2. Auditoria")
    print("3. Envio de pasta especifica")
    print("4. Envio de pasta especifica e desligamento do computador")
    print("5. Sair")
    
    opcao = input("Digite o número da opção desejada: ")
    try:
        numero = int(opcao)
        return numero
    except ValueError:
        return 404


def submenu_audit_ou_primeira_inicializacao():
    print("\nEscolha uma opção:")
    print("1. Horario comercial")
    print("2. Envio sem limitações")
    print("3. Voltar")
    
    opcao = input("Digite o número da opção desejada: ")
    return int(opcao)


def salvar_nome_arquivo_auditoria(nome_arquivo):
    try:
        # Abre o arquivo .txt em modo de adição (append)
        with open(caminho_txt_audit, 'a') as arquivo:
            arquivo.write(nome_arquivo + '\n')  # Escreve o nome do arquivo e pula uma linha
        print(f"Nome do arquivo '{nome_arquivo}' salvo com sucesso em '{caminho_txt_audit}'\n")
    except Exception as e:
        print(f"Erro ao salvar o nome do arquivo: {e}")
    except FileNotFoundError as erro:
        print(f'Arquivo nao encontrado: {erro}')


def checa_arquivo_audit():
    try:
        # Verifica se o arquivo existe e se está vazio
        if os.path.exists(caminho_txt_audit) and os.path.getsize(caminho_txt_audit) > 0:
            return False
        else:
            return True
    except Exception as e:
        print(f"Erro ao verificar o arquivo: {e}")
        return True
    

def minimizar_janela():
    """
    Minimiza a janela do console no Windows.
    """
    # Identificador da janela do console
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd:
        # Comando para minimizar a janela
        ctypes.windll.user32.ShowWindow(hWnd, 6)  # SW_MINIMIZE = 6


ascii_art = r"""
          _      _   _____  _     _        _ _           _     _                 
         | |    | | |  __ \(_)   | |      (_) |         (_)   | |                
         | |    | | | |  | |_ ___| |_ _ __ _| |__  _   _ _  __| | ___  _ __ __ _ 
     _   | |_   | | | |  | | / __| __| '__| | '_ \| | | | |/ _` |/ _ \| '__/ _` |
    | |__| | |__| | | |__| | \__ \ |_| |  | | |_) | |_| | | (_| | (_) | | | (_| |
     \____/ \____/  |_____/|_|___/\__|_|  |_|_.__/ \__,_|_|\__,_|\___/|_|  \__,_|
"""