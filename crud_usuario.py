import customtkinter as ctk
from tkinter import messagebox
from conexao import get_connection

class UsuarioApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("🎮 Gerenciar Usuários")
        self.geometry("1000x500")
        self.protocol("WM_DELETE_WINDOW", self.voltar)
        
        # Conexão
        self.con = get_connection()
        self.usuario_selecionado = None  # Armazena ID do usuário selecionado
        
        # Título
        ctk.CTkLabel(self, text="📁 Gerenciar Usuários", font=("Arial", 20, "bold")).pack(pady=15)
        
        # Frame de campos
        self.frame_campos = ctk.CTkFrame(self)
        self.frame_campos.pack(pady=10)
        
        # Campos
        ctk.CTkLabel(self.frame_campos, text="Nome:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_nome.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_email.grid(row=1, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_senha = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_senha.grid(row=2, column=1, pady=5)

        ctk.CTkLabel(self.frame_campos, text="Foto:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_foto = ctk.CTkEntry(self.frame_campos, width=250)
        self.entry_foto.grid(row=3, column=1, pady=5)

        # Lista de usuários
        self.lista_usuarios = ctk.CTkTextbox(self, width=980, height=200)
        self.lista_usuarios.pack(pady=10)
        self.lista_usuarios.bind("<Button-1>", self.selecionar_usuario)

        # Frame de botões
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10)
        ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar_usuario).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar_usuario).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir_usuario).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=3, padx=10)
        ctk.CTkButton(self.frame_botoes, text="Voltar", command=self.voltar).grid(row=0, column=4, padx=10)
        
        # Atualiza lista na abertura
        self.atualizar_lista()
    
    # ========================= MÉTODOS =========================
    def atualizar_lista(self):
        try:
            cur = self.con.cursor()
            cur.execute("SELECT id_usuario, nome, email, senha, avatar_url, data_criacao FROM usuario ORDER BY id_usuario")
            usuarios = cur.fetchall()
            cur.close()
            
            self.lista_usuarios.configure(state="normal")
            self.lista_usuarios.delete("1.0", "end")
            for usuario in usuarios:
                self.lista_usuarios.insert(
                    "end", 
                    f"{usuario[0]} | {usuario[1]} | {usuario[2]} | {usuario[3]} | {usuario[4]} | {usuario[5]}\n"
                )
            self.lista_usuarios.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista: {e}")

    def selecionar_usuario(self, event):
        """Seleciona o usuário clicado na lista"""
        try:
            index = self.lista_usuarios.index(f"@{event.x},{event.y}")
            linha = self.lista_usuarios.get(f"{index} linestart", f"{index} lineend").strip()
            if linha:
                partes = linha.split(" | ")
                self.usuario_selecionado = int(partes[0])
                # Preenche os campos com os dados
                self.entry_nome.delete(0, "end")
                self.entry_nome.insert(0, partes[1])
                self.entry_email.delete(0, "end")
                self.entry_email.insert(0, partes[2])
                self.entry_senha.delete(0, "end")
                self.entry_senha.insert(0, partes[3])
                self.entry_foto.delete(0, "end")
                self.entry_foto.insert(0, partes[4])
        except:
            self.usuario_selecionado = None

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        foto = self.entry_foto.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Os campos 'Nome' e 'Email' são obrigatórios.")
            return

        try:
            cur = self.con.cursor()
            # Inserção sem data_criacao, o banco preenche automaticamente
            cur.execute(
                "INSERT INTO usuario (nome, email, senha, avatar_url) VALUES (%s, %s, %s, %s)",
                (nome, email, senha, foto)
            )
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "✅ Usuário cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    def editar_usuario(self):
        if not self.usuario_selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário na lista para editar.")
            return

        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        foto = self.entry_foto.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Os campos 'Nome' e 'Email' são obrigatórios.")
            return

        try:
            cur = self.con.cursor()
            cur.execute(
                "UPDATE usuario SET nome=%s, email=%s, senha=%s, avatar_url=%s WHERE id_usuario=%s",
                (nome, email, senha, foto, self.usuario_selecionado)
            )
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "✅ Usuário atualizado com sucesso!")
            self.usuario_selecionado = None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar: {e}")

    def excluir_usuario(self):
        if not self.usuario_selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário na lista para excluir.")
            return

        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?")
        if not confirmar:
            return

        try:
            cur = self.con.cursor()
            cur.execute("DELETE FROM usuario WHERE id_usuario=%s", (self.usuario_selecionado,))
            self.con.commit()
            cur.close()

            self.atualizar_lista()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "🗑️ Usuário excluído com sucesso!")
            self.usuario_selecionado = None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

    def limpar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.entry_foto.delete(0, "end")

    def voltar(self):
        if self.master:
            self.master.deiconify()
        self.destroy()
