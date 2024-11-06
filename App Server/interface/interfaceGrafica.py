# interfaceGrafica.py
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import socket
import os
import threading
from utils.config import *
from PIL import Image, ImageTk


class AppInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("BackupNFE")
        self.root.state('zoomed')

        # Frame para os botões
        self.button_frame = ttk.Frame(self.root, padding="10")
        self.button_frame.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_frame.pack(fill=tk.Y, expand=True)
        self.button_frame.pack(fill=tk.X, expand=False)
        
        # Carrega a imagen e redimenciona
        image_path = "image/icone.png"
        tamanho_imagen = (100, 100)
        self.logo = Image.open(image_path)
        self.logo = self.logo.resize(tamanho_imagen)
        self.photo = ImageTk.PhotoImage(self.logo)
        
        self.image_label = tk.Label(self.button_frame, image=self.photo)
        self.image_label.place(x=0, y=0)

        # Criação do widget ScrolledText para simular o terminal
        self.scroll_text = ScrolledText(self.root, wrap=tk.WORD, bg="#2C2D2C", fg="white", font=("Consolas", 12))
        self.scroll_text.pack(fill=tk.BOTH, expand=True)

        # Botão para iniciar o servidor
        self.iniciar_button = ttk.Button(self.button_frame, text="Iniciar Servidor", cursor="hand2", command=self.start_server_thread)
        self.iniciar_button.pack(pady=(0,10))
        
        # Novo Frame entre os botões
        self.middle_frame = ttk.Frame(self.button_frame, padding="5")
        self.middle_frame.pack(pady=10)
        
        # Aqui você pode adicionar widgets ao middle_frame quando necessário
        label = ttk.Label(self.middle_frame, text="Conteúdo do Frame do Meio")
        label.pack()
        
        # Criação do botão para fechar o aplicativo
        self.fechar_button = ttk.Button(self.button_frame, text="Fechar", cursor="hand2", command=self.close_app)
        self.fechar_button.pack(pady=(10,0))
        



    def printScrollText(self, value_string):
        self.scroll_text.insert(tk.END, f"{value_string}\n")
        self.scroll_text.see(tk.END)


    def start_server_thread(self):
        config = ler_configuracoes()
        servidor_ip = config['servidor_ip']
        servidor_porta = config['servidor_porta']
        pasta_destino = config['pasta_destino']
        threading.Thread(target=self.iniciar_servidor, args=(servidor_ip, servidor_porta, pasta_destino), daemon=True).start()

    
    def close_app(self):
        self.root.destroy()

    def iniciar_servidor(self, ip, porta, pasta_destino):
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, int(porta)))
            s.listen(50)

            self.printScrollText(ascii_art)
            self.printScrollText(f"Servidor escutando em {ip}:{porta}...")

            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        self.printScrollText(f"Conectado por {addr}")
                        
                        # Recebe o tamanho da requisição
                        try:
                            tamanho_total_raw = conn.recv(8).decode('utf-8')
                            if not tamanho_total_raw.strip().isdigit():
                                self.printScrollText(f"Erro ao receber tamanho da requisição. Recebido: {tamanho_total_raw}")
                                conn.sendall(b"ERROR")
                                continue
                            tamanho_total = int(tamanho_total_raw)
                        except Exception as e:
                            self.printScrollText(f"Erro ao processar o tamanho da requisição: {e}")
                            conn.sendall(b"ERROR")
                            continue

                        # Recebe os dados
                        dados_recebidos = b""
                        while len(dados_recebidos) < tamanho_total:
                            parte = conn.recv(1024)
                            if not parte:
                                break
                            dados_recebidos += parte

                        # Processa a requisição
                        try:    
                            requisicao = dados_recebidos.decode('utf-8', errors='ignore')
                            arrayDataRequisicao = requisicao.split('|||')
                            
                            nome_subdiretorio, nome_arquivo, dados_arquivo = arrayDataRequisicao
                            nome_subdiretorio = nome_subdiretorio.strip()
                            nome_arquivo = nome_arquivo.strip()
                            dados_arquivo = dados_arquivo.strip()
                            
                            caminho_completo = os.path.join(pasta_destino, nome_subdiretorio)
                            if not os.path.exists(caminho_completo):
                                os.makedirs(caminho_completo)
                                self.printScrollText(f"Subdiretório: {caminho_completo} criado.")
                                
                            caminho_arquivo = os.path.join(caminho_completo, nome_arquivo)
                            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                                f.write(dados_arquivo)

                            self.printScrollText(f"Arquivo salvo em: {caminho_arquivo}")
                            conn.sendall(b"SUCCESS")
                        
                        except Exception as e:
                            self.printScrollText(f"Erro ao processar a requisição: {e}")
                            conn.sendall(b"ERROR")
                            continue
                except Exception as e:
                    self.printScrollText(f"Erro inesperado: {e}")
                    continue
                except UnicodeDecodeError as e:
                    print(f"Erro ao decodificar os dados recebidos: {e}")
                    continue