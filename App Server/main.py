# main.py
import tkinter as tk
from interface.interfaceGrafica import AppInterface

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInterface(root)
    root.mainloop()

# from utils.config import *
# from controllers.init_server import *
# from interface.interfaceGrafica import *


# if __name__ == '__main__':
#     config = ler_configuracoes()
#     servidor_ip = config['servidor_ip']
#     servidor_porta = config['servidor_porta']
#     pasta_destino = config['pasta_destino']
    
#     iniciar_servidor(servidor_ip, servidor_porta, pasta_destino)
#     print(ascii_art)


# # def button_init_server():   