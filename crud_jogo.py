import customtkinter as ctk
from tkinter import messagebox
from conexao import get_connection

class JogosApp(ctk.CTkToplevel):
    def __init__(self, master=None, menu_principal=None):
        super().__init__(master)
        self.menu_principal = menu_principal
        self.con = get_connection()

        # === Configurações da janela ===
        self.title("🎮 Gerenciar Jogos")
        self.geometry("1000x500")
        self.protocol("WM_DELETE_WINDOW", self.voltar)

        # === Título ===
        ctk.CTkLabel(self, text="🎮 Gerenciar Jogos", font=("Arial", 20, "bold")).pack(pady=15)

        # === Frame de campos ===
        self.frame_campos = ctk.CTkFrame(self)
        self.frame_campos.pack(pady=10)

        ctk.CTkLabel(self.frame_campos, text="Título:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_titulo = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_titulo.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Data (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.entry_data = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_data.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Desenvolvedor:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_desenvolvedor = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_desenvolvedor.grid(row=2, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Imagem/Capa:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_imagem = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_imagem.grid(row=3, column=1, pady=5)

        # === Frame de botões ===
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10)

        ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar_jogo).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir_jogo).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Voltar", command=self.voltar).grid(row=0, column=3, padx=10)

        # === Lista de jogos ===
        self.lista_jogos = ctk.CTkTextbox(self, width=500, height=200)
        self.lista_jogos.pack(pady=15)

        # Atualiza lista na abertura
        self.atualizar_lista()

    # ===================== CRUD =====================
    def cadastrar_jogo(self):
        titulo = self.entry_titulo.get()
        data = self.entry_data.get()
        dev = self.entry_desenvolvedor.get()
        img = self.entry_imagem.get()

        if not titulo:
            messagebox.showwarning("Aviso", "O campo 'Título' é obrigatório.")
            return

        cur = self.con.cursor()
        sql = "INSERT INTO jogo (titulo, data_lancamento, desenvolvedor, imagem_capa) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (titulo, data, dev, img))
        self.con.commit()

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "✅ Jogo cadastrado com sucesso!")

        # Limpa os campos
        self.entry_titulo.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_desenvolvedor.delete(0, "end")
        self.entry_imagem.delete(0, "end")

    def excluir_jogo(self):
        selecionado = self.lista_jogos.get("insert linestart", "insert lineend").strip()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um jogo na lista para excluir.")
            return

        id_jogo = selecionado.split(" | ")[0].replace("ID: ", "")
        cur = self.con.cursor()
        cur.execute("DELETE FROM jogo WHERE idjogo=%s", (id_jogo,))
        self.con.commit()

        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "🗑️ Jogo excluído com sucesso!")

    def atualizar_lista(self):
        cur = self.con.cursor()
        cur.execute("SELECT idjogo, titulo, desenvolvedor FROM jogo ORDER BY idjogo")
        jogos = cur.fetchall()
        self.lista_jogos.configure(state="normal")
        self.lista_jogos.delete("1.0", "end")
        for jogo in jogos:
            self.lista_jogos.insert("end", f"ID: {jogo[0]} | {jogo[1]} ({jogo[2]})\n")
        self.lista_jogos.configure(state="disabled")

    # ===================== Voltar =====================
    def voltar(self):
        if self.menu_principal:
            self.menu_principal.deiconify()
        self.destroy()


# ===================== Teste de execução =====================
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    menu = ctk.CTk()
    menu.title("Menu Principal")
    menu.geometry("400x400")

    def abrir_jogos():
        menu.withdraw()
        JogosApp(master=menu, menu_principal=menu)

    ctk.CTkButton(menu, text="Gerenciar Jogos", command=abrir_jogos, width=200).pack(pady=20)

    menu.mainloop()
