import os

# Função para ler o arquivo de configuração
def ler_configuracoes():
    configuracoes = {}  
    with open('config.cliente.txt', 'r') as arquivo:  # Abre o arquivo de configuração
        for linha in arquivo:  # Percorre cada linha do arquivo
            chave, valor = linha.strip().split(': ')  # Divide a linha em chave e valor
            configuracoes[chave] = valor  # Armazena no dicionário
    return configuracoes  # Retorna o dicionário com as configurações


ascii_art = r"""
          _      _   _____  _     _        _ _           _     _                 
         | |    | | |  __ \(_)   | |      (_) |         (_)   | |                
         | |    | | | |  | |_ ___| |_ _ __ _| |__  _   _ _  __| | ___  _ __ __ _ 
     _   | |_   | | | |  | | / __| __| '__| | '_ \| | | | |/ _` |/ _ \| '__/ _` |
    | |__| | |__| | | |__| | \__ \ |_| |  | | |_) | |_| | | (_| | (_) | | | (_| |
     \____/ \____/  |_____/|_|___/\__|_|  |_|_.__/ \__,_|_|\__,_|\___/|_|  \__,_|
"""