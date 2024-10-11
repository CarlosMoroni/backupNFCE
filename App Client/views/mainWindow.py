import customtkinter as ctk

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações básicas da janela
        self.title("Aplicação de Transferência de Arquivos")
        self.geometry("400x300")

        # Criando elementos da interface
        self.label = ctk.CTkLabel(self, text="Transferência de Arquivos", font=("Arial", 16))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Selecione o diretório")
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Enviar Arquivos", command=self.send_files)
        self.button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.teste = ctk.CTkLabel(self, text="teste",)
        self.teste.pack()
        
        
    def send_files(self):
        # Simulando o envio de arquivos
        directory = self.entry.get()
        if directory:
            self.status_label.configure(text=f"Enviando arquivos do diretório: {directory}")
        else:
            self.status_label.configure(text="Por favor, insira um diretório.")
