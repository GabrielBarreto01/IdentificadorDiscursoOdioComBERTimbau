import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

def receber_mensagens():
    while True:
        try:
            data = cliente_socket.recv(1024)
            if not data:
                raise Exception("Servidor desconectado")
            mensagem = data.decode('utf-8')
            if mensagem.startswith("###encerrar###"):
                nome_desconectado = mensagem.split("###")[1]
                messagebox.showinfo("Aviso", f"{nome_desconectado} saiu da conversa.")
                cliente_socket.close()
                janela_cliente.destroy()
                break
            else:
                janela_chat.insert(tk.END, f"{mensagem}\n")
        except Exception as e:
            print(f"Erro na recepção de mensagens: {e}")
            messagebox.showinfo("Aviso", "O servidor foi desconectado.")
            cliente_socket.close()
            janela_cliente.destroy()
            break

def enviar_mensagem(event=None):
    if cliente_socket:
        mensagem = entrada_mensagem.get().strip()
        if mensagem:
            cliente_socket.send(mensagem.encode('utf-8'))
            janela_chat.insert(tk.END, f"{nome_usuario}: {mensagem}\n")
            entrada_mensagem.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma mensagem antes de enviar.")
    else:
        messagebox.showwarning("Aviso", "Você está desconectado do servidor.")

def desconectar(nome_usuario):
    global cliente_socket, janela_cliente
    if cliente_socket:
        mensagem = f"{nome_usuario} SAIU."
        cliente_socket.send(mensagem.encode('utf-8'))
        cliente_socket.close()
        janela_cliente.destroy()

def obter_nome_usuario():
    global nome_usuario, cliente_socket, janela_cliente, janela_chat, entrada_mensagem
    nome_usuario = simpledialog.askstring("Nome de Usuário", "Digite seu nome de usuário:")
    if nome_usuario:
        host = simpledialog.askstring("IP do Servidor", "Digite o IP do servidor:")
        porta = simpledialog.askinteger("Porta", "Digite a porta de conexão do servidor:")
        if host and porta:
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                cliente_socket.connect((host, porta))
                print("Conexão estabelecida com o servidor")
                cliente_socket.send(nome_usuario.encode('utf-8'))

                janela_cliente = tk.Tk()
                janela_cliente.title("Cliente de Chat")

                janela_chat = scrolledtext.ScrolledText(janela_cliente, width=50, height=20)
                janela_chat.pack(padx=10, pady=10)

                entrada_mensagem = tk.Entry(janela_cliente, width=40)
                entrada_mensagem.pack(pady=10)
                entrada_mensagem.bind("<Return>", enviar_mensagem)

                botao_enviar = tk.Button(janela_cliente, text="Enviar", command=enviar_mensagem)
                botao_enviar.pack()

                botao_desconectar = tk.Button(janela_cliente, text="Desconectar", command=lambda: desconectar(nome_usuario))
                botao_desconectar.pack()
                janela_cliente.protocol("WM_DELETE_WINDOW", lambda: desconectar(nome_usuario))

                receber_thread = threading.Thread(target=receber_mensagens)
                receber_thread.start()

                janela_cliente.mainloop()

            except Exception as e:
                print(f"Erro ao conectar ao servidor: {e}")
                exit()
        else:
            print("IP do servidor ou porta não fornecidos.")
            exit()
    else:
        print("Nome de usuário inválido.")

obter_nome_usuario()
