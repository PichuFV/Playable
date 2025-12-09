import customtkinter as ctk
import subprocess
import sys
import os

# --- CONFIGURAÇÕES ---
APP_NAME = "PlayAble"
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
DARK_GRAY = "#242424"
BLUE = "#1F6AA5"

# Lista de teclas que o usuário pode escolher.
# Adicione outras teclas se necessário.
KEY_OPTIONS = [
    "up", "down", "left", "right",  # Teclas de seta
    "w", "a", "s", "d",
    "space", "enter", "shift", "ctrl",
    "e", "f", "q", "r",
    "1", "2", "3", "4"
]

# --- LÓGICA DA APLICAÇÃO ---

def start_main_script(key_mappings):
    """
    Inicia o script principal de detecção de movimento, passando os mapeamentos
    de teclas como argumentos de linha de comando.
    """
    # Encontra o caminho para o script playable_yolo_v2.py
    # Isso assume que run_app.py está na raiz e o script principal em 'classification/'
    script_path = os.path.join("classification", "playable_yolo_v2.py")

    if not os.path.exists(script_path):
        print(f"ERRO: Script não encontrado em '{script_path}'")
        # Opcional: mostrar um pop-up de erro na GUI
        return

    # Constrói o comando para executar o script
    # Ex: python classification/playable_yolo_v2.py --up w --down s --left a --right d
    command = [
        sys.executable,  # Caminho para o interpretador Python atual
        script_path,
        "--up", key_mappings["up"],
        "--down", key_mappings["down"],
        "--left", key_mappings["left"],
        "--right", key_mappings["right"]
    ]

    print(f"Iniciando script com o comando: {' '.join(command)}")

    subprocess.Popen(command)

    app.quit()



# Configurações iniciais da janela e tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(APP_NAME)
app.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
app.resizable(False, False)

def on_closing():
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# ------------ Conteúdo da Janela ------------

# título
title_label = ctk.CTkLabel(
    app,
    text=APP_NAME,
    font=ctk.CTkFont(size=40, weight="bold"),
    text_color=BLUE
)
title_label.pack(pady=(30, 10))

# descrição
description_label = ctk.CTkLabel(
    app,
    text="Use os movimentos da sua cabeça para controlar jogos e aplicativos.\n"
         "Configure abaixo qual tecla será acionada para cada direção.",
    font=ctk.CTkFont(size=14),
    wraplength=WINDOW_WIDTH - 40,
    justify="center"
)
description_label.pack(pady=10, padx=20)

# Mapeamento de teclas selecionadas pelo usuário
keys_frame = ctk.CTkFrame(app, fg_color="transparent")
keys_frame.pack(pady=20, padx=40, fill="x")

option_menus = {}
directions = {
    "up": "Virar o rosto para Cima",
    "down": "Virar o rosto para Baixo",
    "left": "Virar o rosto para Esquerda",
    "right": "Virar o rosto para Direita"
}
# Valores padrão
default_keys = {"up": "up", "down": "down", "left": "left", "right": "right"}

for i, (direction, text) in enumerate(directions.items()):
    label = ctk.CTkLabel(keys_frame, text=f"{text}:", font=ctk.CTkFont(size=14))
    label.grid(row=i, column=0, padx=10, pady=12, sticky="w")

    option_menu = ctk.CTkOptionMenu(keys_frame, values=KEY_OPTIONS, width=150)
    option_menu.set(default_keys[direction])
    option_menu.grid(row=i, column=1, padx=10, pady=12, sticky="e")
    option_menus[direction] = option_menu

keys_frame.grid_columnconfigure(0, weight=1)
keys_frame.grid_columnconfigure(1, weight=1)


def on_start_click():
    selected_keys = {direction: menu.get() for direction, menu in option_menus.items()}
    print("Mapeamentos selecionados:", selected_keys)
    start_main_script(selected_keys)

start_button = ctk.CTkButton(
    app,
    text="Iniciar Detecção",
    font=ctk.CTkFont(size=16, weight="bold"),
    command=on_start_click,
    height=40
)
start_button.pack(pady=20, padx=40, fill="x")


# Créditos
creators_frame = ctk.CTkFrame(app, fg_color=DARK_GRAY)
creators_frame.pack(side="bottom", fill="x", pady=(10, 0), ipady=10)

creators_label = ctk.CTkLabel(
    creators_frame,
    text="Fabio Vivarelli (github.com/PichuFV)",
    font=ctk.CTkFont(size=12)
).pack()

creators_label2 = ctk.CTkLabel(
    creators_frame,
    text="João Vitor (https://github.com/iamthewalrusz)",
    font=ctk.CTkFont(size=12)
).pack()

creators_label3 = ctk.CTkLabel(
    creators_frame,
    text="Nathan Guimarães (github.com/nathanhgo)",
    font=ctk.CTkFont(size=12)
).pack()

# Adicione mais labels se houver mais criadores
# Ex: ctk.CTkLabel(creators_frame, text="Outro Dev (github.com/outro)").pack()


# Inicia o loop da aplicação GUI
app.mainloop()
