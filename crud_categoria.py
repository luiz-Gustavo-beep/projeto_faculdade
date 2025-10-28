import customtkinter as ctk
from tkinter import messagebox
from conexao import get_connection

class CategoriaApp:
    def __init__(self, master=None, menu_principal=None):
        self.con = get_connection()
        self.menu_principal = menu_principal

        self.janela = ctk.CTkToplevel(master)
        self.janela.title("🎮 Gerenciar Categorias")
        self.janela.geometry("1000x500")

        # Título
        ctk.CTkLabel(self.janela, text="📁 Gerenciar Categorias", font=("Arial", 20, "bold")).pack(pady=15)

        # Frame campos
        self.frame_campos = ctk.CTkFrame(self.janela)
        self.frame_campos.pack(pady=10)

        ctk.CTkLabel(self.frame_campos, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nome = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Descrição:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_desc = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_desc.grid(row=1, column=1, pady=5)

        # Lista
        self.lista_categorias = ctk.CTkTextbox(self.janela, width=580, height=230)
        self.lista_categorias.pack(pady=10)

        # Frame botões
        self.frame_botoes = ctk.CTkFrame(self.janela)
        self.frame_botoes.pack(pady=10)

        ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar_categoria).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar_categoria).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir_categoria).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=3, padx=10)
        # Botão voltar no mesmo frame
        ctk.CTkButton(self.frame_botoes, text="Voltar", command=self.voltar).grid(row=0, column=4, padx=10)

        self.atualizar_lista()

    # Métodos CRUD
    def atualizar_lista(self):
        cur = self.con.cursor()
        cur.execute("SELECT idcategoria, nome, descricao FROM categoria ORDER BY idcategoria")
        categorias = cur.fetchall()
        self.lista_categorias.delete("1.0", "end")
        for cat in categorias:
            self.lista_categorias.insert("end", f"ID: {cat[0]} | {cat[1]} - {cat[2]}\n")

    def cadastrar_categoria(self):
        nome = self.entry_nome.get()
        desc = self.entry_desc.get()
        if not nome:
            messagebox.showwarning("Aviso", "O campo 'Nome' é obrigatório.")
            return
        cur = self.con.cursor()
        cur.execute("INSERT INTO categoria (nome, descricao) VALUES (%s, %s)", (nome, desc))
        self.con.commit()
        self.atualizar_lista()
        self.entry_nome.delete(0, "end")
        self.entry_desc.delete(0, "end")
        messagebox.showinfo("Sucesso", "✅ Categoria cadastrada com sucesso!")

    def editar_categoria(self):
        selecionado = self.lista_categorias.get("insert linestart", "insert lineend")
        if not selecionado.strip():
            messagebox.showwarning("Aviso", "Selecione uma categoria na lista para editar.")
            return
        idcategoria = selecionado.split(" | ")[0].replace("ID: ", "")
        novo_nome = self.entry_nome.get()
        nova_desc = self.entry_desc.get()
        if not novo_nome:
            messagebox.showwarning("Aviso", "Preencha o novo nome antes de editar.")
            return
        cur = self.con.cursor()
        cur.execute("UPDATE categoria SET nome=%s, descricao=%s WHERE idcategoria=%s", (novo_nome, nova_desc, idcategoria))
        self.con.commit()
        self.atualizar_lista()
        self.entry_nome.delete(0, "end")
        self.entry_desc.delete(0, "end")
        messagebox.showinfo("Sucesso", "✅ Categoria atualizada com sucesso!")

    def excluir_categoria(self):
        selecionado = self.lista_categorias.get("insert linestart", "insert lineend")
        if not selecionado.strip():
            messagebox.showwarning("Aviso", "Selecione uma categoria na lista para excluir.")
            return
        idcategoria = selecionado.split(" | ")[0].replace("ID: ", "")
        cur = self.con.cursor()
        cur.execute("DELETE FROM categoria WHERE idcategoria=%s", (idcategoria,))
        self.con.commit()
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", "🗑️ Categoria excluída com sucesso!")

    # Função voltar para menu
    def voltar(self):
        if self.menu_principal:
            self.menu_principal.deiconify()  # mostra o menu
        self.janela.destroy()


# Teste de execução
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    menu = ctk.CTk()
    menu.title("Menu Principal")
    menu.geometry("400x400")

    def abrir_categorias():
        menu.withdraw()
        CategoriaApp(menu_principal=menu)

    ctk.CTkButton(menu, text="Gerenciar Categorias", command=abrir_categorias, width=200).pack(pady=20)

    menu.mainloop()
