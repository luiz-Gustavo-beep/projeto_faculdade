import customtkinter as ctk
from tkinter import messagebox
from conexao import get_connection

class PlataformasApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("🎮 Gerenciar Plataformas")
        self.geometry("1000x500")
        self.protocol("WM_DELETE_WINDOW", self.voltar)

        # Conexão com o banco
        self.con = get_connection()

        # Título
        ctk.CTkLabel(self, text="📁 Gerenciar Plataformas", font=("Arial", 20, "bold")).pack(pady=15)

        # Frame de campos
        self.frame_campos = ctk.CTkFrame(self)
        self.frame_campos.pack(pady=10)

        ctk.CTkLabel(self.frame_campos, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nome = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Fabricante:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_fabricante = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_fabricante.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Descrição:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_desc = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_desc.grid(row=2, column=1, pady=5)

        # Lista de plataformas
        self.lista_plataformas = ctk.CTkTextbox(self, width=580, height=230)
        self.lista_plataformas.pack(pady=10)

        # Frame de botões
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10)
        ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar_plataforma).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar_plataforma).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir_plataforma).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=3, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Voltar", command=self.voltar).grid(row=0, column=4, padx=10)

        # Atualiza lista na abertura
        self.atualizar_lista()

    # ---------------- MÉTODOS ----------------
    def atualizar_lista(self):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT idplataforma, nome, fabricante, descricao FROM plataforma ORDER BY idplataforma")
            plataformas = cur.fetchall()
            cur.close()

            self.lista_plataformas.configure(state="normal")
            self.lista_plataformas.delete("1.0", "end")
            for plat in plataformas:
                self.lista_plataformas.insert("end", f"ID: {plat[0]} | {plat[1]} - {plat[2]} - {plat[3]}\n")
            self.lista_plataformas.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista: {e}")

    def cadastrar_plataforma(self):
        nome = self.entry_nome.get().strip()
        fabricante = self.entry_fabricante.get().strip()
        desc = self.entry_desc.get().strip()

        if not nome or not fabricante:
            messagebox.showwarning("Aviso", "Os campos 'Nome' e 'Fabricante' são obrigatórios.")
            return

        try:
            cur = self.con.cursor()
            cur.execute(
                "INSERT INTO plataforma (nome, fabricante, descricao) VALUES (%s, %s, %s)",
                (nome, fabricante, desc)
            )
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.entry_nome.delete(0, "end")
            self.entry_fabricante.delete(0, "end")
            self.entry_desc.delete(0, "end")
            messagebox.showinfo("Sucesso", "✅ Plataforma cadastrada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    def pegar_selecionado(self):
        try:
            selecionado = self.lista_plataformas.get("insert linestart", "insert lineend").strip()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione uma plataforma na lista.")
                return None
            idplataforma = selecionado.split(" | ")[0].replace("ID: ", "")
            return idplataforma
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao pegar plataforma selecionada: {e}")
            return None

    def editar_plataforma(self):
        idplataforma = self.pegar_selecionado()
        if not idplataforma:
            return

        novo_nome = self.entry_nome.get().strip()
        novo_fabricante = self.entry_fabricante.get().strip()
        nova_desc = self.entry_desc.get().strip()

        if not novo_nome or not novo_fabricante:
            messagebox.showwarning("Aviso", "Os campos 'Nome' e 'Fabricante' são obrigatórios.")
            return

        try:
            cur = self.con.cursor()
            cur.execute(
                "UPDATE plataforma SET nome=%s, fabricante=%s, descricao=%s WHERE idplataforma=%s",
                (novo_nome, novo_fabricante, nova_desc, idplataforma)
            )
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.entry_nome.delete(0, "end")
            self.entry_fabricante.delete(0, "end")
            self.entry_desc.delete(0, "end")
            messagebox.showinfo("Sucesso", "✅ Plataforma atualizada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar: {e}")

    def excluir_plataforma(self):
        idplataforma = self.pegar_selecionado()
        if not idplataforma:
            return

        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta plataforma?")
        if not confirmar:
            return

        try:
            cur = self.con.cursor()
            cur.execute("DELETE FROM plataforma WHERE idplataforma=%s", (idplataforma,))
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.entry_nome.delete(0, "end")
            self.entry_fabricante.delete(0, "end")
            self.entry_desc.delete(0, "end")
            messagebox.showinfo("Sucesso", "🗑️ Plataforma excluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def voltar(self):
        if self.master:
            self.master.deiconify()
        self.destroy()

