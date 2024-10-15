import os

# Função para ler o arquivo de configuração
def ler_configuracoes():
    configuracoes = {}  
    with open('config.cliente.txt', 'r') as arquivo:  # Abre o arquivo de configuração
        for linha in arquivo:  # Percorre cada linha do arquivo
            chave, valor = linha.strip().split(': ')  # Divide a linha em chave e valor
            configuracoes[chave] = valor  # Armazena no dicionário
    return configuracoes  # Retorna o dicionário com as configurações
