import customtkinter as ctk
from crud_jogo import JogosApp
from crud_categoria import CategoriaApp
from crud_plataforma import PlataformasApp
from crud_usuario import UsuarioApp  # CRUD de usuários

# ---------------- Configuração ----------------
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

# ---------------- Janela Principal ----------------
app = ctk.CTk()
app.title('Sistema de Gerenciamento')
app.geometry('1000x500')

# ---------------- Título ----------------
ctk.CTkLabel(app, text='🎮 SISTEMA DE GERENCIAMENTO', font=('Arial', 16, 'bold')).pack(pady=20)

# ---------------- Funções dos Botões ----------------
def abrir_jogos():
    app.withdraw()
    janela = JogosApp(master=app)
    app.wait_window(janela)
    app.deiconify()

def abrir_categorias():
    app.withdraw()
    janela = CategoriaApp(master=app)
    app.wait_window(janela)
    app.deiconify()

def abrir_plataformas():
    app.withdraw()
    janela = PlataformasApp(master=app)
    app.wait_window(janela)
    app.deiconify()

def abrir_usuarios():
    app.withdraw()
    janela = UsuarioApp(master=app)
    app.wait_window(janela)
    app.deiconify()

def sair():
    app.destroy()

# ---------------- Botões ----------------
ctk.CTkButton(app, text='Gerenciar Jogos', command=abrir_jogos, width=300).pack(pady=10)
ctk.CTkButton(app, text='Gerenciar Categorias', command=abrir_categorias, width=300).pack(pady=10)
ctk.CTkButton(app, text='Gerenciar Plataformas', command=abrir_plataformas, width=300).pack(pady=10)
ctk.CTkButton(app, text='Gerenciar Usuários', command=abrir_usuarios, width=300).pack(pady=10)  # botão do CRUD de usuários
ctk.CTkButton(app, text='Sair', command=sair, fg_color='red', hover_color='#a83232', width=300).pack(pady=10)

# ---------------- Rodapé ----------------
ctk.CTkLabel(app, text='Escolha uma opção para gerenciar', font=('Arial', 12)).pack(pady=10)

# ---------------- Iniciar App ----------------
app.mainloop()
