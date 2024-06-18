import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Carregar o BERTimbau
tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
model = AutoModelForSequenceClassification.from_pretrained("neuralmind/bert-base-portuguese-cased")

# Carregar o pipeline de análise de sentimento
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

MAX_USUARIOS = 2  # Número máximo de usuários que podem se conectar ao servidor
clientes_banidos = []  # Lista de IPs banidos
clientes = []

palavras_ofensivas = [
    "abestalhado", "arrombado", "baitola", "buceta", "cabaço",
    "carniça", "corno", "cuzão", "fidumaégua", "fuleiro",
    "fudido", "jumento", "lascado", "merda", "otário",
    "peste", "rapariga", "tabacudo", "viado", "xibiu"
]

def analisar_sentimento(mensagem):
    resultado = classifier(mensagem)
    sentimento = resultado[0]['label']
    if sentimento == 'LABEL_0':
        return 'Negativo'
    elif sentimento == 'LABEL_1':
        return 'Positivo'
    else:
        return 'Neutro'

def verificar_ofensiva(mensagem):
    for palavra in palavras_ofensivas:
        if palavra in mensagem.lower():
            return True
    return False

def receber_mensagens(client_socket, username, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            mensagem = data.decode('utf-8')
            sentimento = analisar_sentimento(mensagem)
            ofensiva = verificar_ofensiva(mensagem)

            if ofensiva:
                tipo_discurso = "Ofensiva"
            else:
                tipo_discurso = sentimento

            # Atualiza a janela de chat com a mensagem do usuário e o tipo de discurso
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, f"{username}: {mensagem} [{tipo_discurso}]\n")
            chat_window.see(tk.END)
            chat_window.config(state=tk.DISABLED)

            # Registra a mensagem no arquivo histórico com o tipo de discurso
            log_message(f"{username}: {mensagem} [{tipo_discurso}]")

            # Envia a mensagem recebida para todos os outros usuários
            enviar_para_todos(f"{username}: {mensagem} [{tipo_discurso}]", client_socket)
        except Exception as e:
            print(f"Erro na recepção de mensagens de {username}: {e}")
            break

    client_socket.close()
    remover_cliente(client_socket, username)

def enviar_para_todos(mensagem, remetente_socket):
    for cliente, user, addr in clientes:
        if cliente != remetente_socket:
            try:
                cliente.send(mensagem.encode('utf-8'))
            except Exception as e:
                print(f"Erro ao enviar mensagem para {user}: {e}")
                remover_cliente(cliente, user)

def remover_cliente(client_socket, username):
    global clientes
    clientes = [(cliente, user, addr) for cliente, user, addr in clientes if cliente != client_socket]
    log_message(f"{username} desconectado")
    print(f"{username} desconectado")

def log_message(message):
    with open("historico_chat.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def enviar_mensagem_boas_vindas(client_socket, username):
    mensagem_boas_vindas = f"Bem-vindo(a), {username}!"
    client_socket.send(mensagem_boas_vindas.encode('utf-8'))
    log_message(mensagem_boas_vindas)

def notificar_novo_usuario(username):
    messagebox.showinfo("Novo(a) Usuário(a)", f"Usuário(a) '{username}' conectou-se ao chat.")
    log_message(f"Usuário(a) '{username}' conectou-se ao chat.")

def banir_usuario():
    username_or_ip = simpledialog.askstring("Banir Usuário(a)", "Digite o nome de usuário ou IP do(a) usuário(a) a ser banido(a):")
    if username_or_ip:
        motivo = simpledialog.askstring("Banir Usuário(a)", "Digite o motivo do banimento:")
        if motivo:
            for i, (cliente, user, addr) in enumerate(clientes):
                if user == username_or_ip:
                    clientes.pop(i)
                    clientes_banidos.append(addr[0])
                    cliente.send(f"Você foi banido do chat. Motivo: {motivo}".encode('utf-8'))
                    cliente.close()
                    ban_attempts_text.insert(tk.END, f"O usuário '{username_or_ip}' foi banido do chat. Motivo: {motivo}\n")
                    log_message(f"Usuário '{username_or_ip}' foi banido do chat. Motivo: {motivo}")
                    return
            banir_ip(username_or_ip, motivo)

def banir_ip(ip_address, motivo):
    if ip_address not in clientes_banidos:
        clientes_banidos.append(ip_address)
        ban_attempts_text.insert(tk.END, f"O IP '{ip_address}' foi banido do chat. Motivo: {motivo}\n")
        log_message(f"IP '{ip_address}' foi banido do chat. Motivo: {motivo}")

def desbanir_usuario():
    username_or_ip = simpledialog.askstring("Desbanir Usuário(a)", "Digite o nome de usuário ou IP do(a) usuário(a) a ser desbanido(a):")
    if username_or_ip:
        desbanir_ip(username_or_ip)

def desbanir_ip(ip_address):
    if ip_address in clientes_banidos:
        clientes_banidos.remove(ip_address)
        ban_attempts_text.insert(tk.END, f"O IP '{ip_address}' foi desbanido do chat.\n")
        log_message(f"IP '{ip_address}' foi desbanido do chat.")

def iniciar_servidor():
    global socket_servidor, clientes
    host = '0.0.0.0'  # O servidor estará disponível em todas as interfaces de rede
    porta = 9999

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_servidor.bind((host, porta))
    socket_servidor.listen(MAX_USUARIOS)  # Definindo o número máximo de conexões pendentes

    ip_label.config(text=f"IP do servidor: {host}:{porta}")

    print(f"Servidor de chat iniciado em {host}:{porta}")

    while True:
        socket_cliente, client_address = socket_servidor.accept()

        if client_address[0] in clientes_banidos:
            tentativa_mensagem = f"IP banido {client_address[0]} tentou se conectar."
            socket_cliente.send("Você está banido do chat.".encode('utf-8'))
            socket_cliente.close()
            ban_attempts_text.insert(tk.END, f"{tentativa_mensagem}\n")
            log_message(tentativa_mensagem)
            continue

        if len(clientes) >= MAX_USUARIOS:
            socket_cliente.send("Número máximo de usuários atingido. Tente novamente mais tarde.".encode('utf-8'))
            socket_cliente.close()
            continue

        username = socket_cliente.recv(1024).decode('utf-8').lower()

        if username in [user[1] for cliente, user, addr in clientes]:
            socket_cliente.send("O nome de usuário já está em uso. Por favor, escolha outro nome.".encode('utf-8'))
            socket_cliente.close()
            continue

        clientes.append((socket_cliente, username, client_address))

        notificar_novo_usuario(username)
        enviar_mensagem_boas_vindas(socket_cliente, username)

        client_thread = threading.Thread(target=receber_mensagens, args=(socket_cliente, username, client_address))
        client_thread.start()

def encerrar_servidor():
    if messagebox.askyesno("Encerrar Servidor", "Deseja encerrar o servidor?"):
        socket_servidor.close()
        janela_servidor.quit()
        janela_servidor.destroy()

janela_servidor = tk.Tk()
janela_servidor.title("Servidor de Chat")

ip_label = tk.Label(janela_servidor, text="IP do servidor: Aguardando inicialização...")
ip_label.pack()

notebook = ttk.Notebook(janela_servidor)
notebook.pack(expand=True, fill=tk.BOTH)

frame_chat = tk.Frame(notebook)
notebook.add(frame_chat, text="Chat")

chat_window = scrolledtext.ScrolledText(frame_chat, width=50, height=20)
chat_window.pack(padx=10, pady=10)
chat_window.config(state=tk.DISABLED)

frame_banimentos = tk.Frame(notebook)
notebook.add(frame_banimentos, text="Banimentos")

ban_attempts_text = scrolledtext.ScrolledText(frame_banimentos, width=50, height=10)
ban_attempts_text.pack(pady=5)

botao_banir_usuario = tk.Button(frame_banimentos, text="Banir Usuário", command=banir_usuario)
botao_banir_usuario.pack(pady=5)

botao_desbanir_usuario = tk.Button(frame_banimentos, text="Desbanir Usuário", command=desbanir_usuario)
botao_desbanir_usuario.pack(pady=5)

botao_encerrar = tk.Button(janela_servidor, text="Encerrar Servidor", command=encerrar_servidor)
botao_encerrar.pack(pady=10)

thread_iniciar_servidor = threading.Thread(target=iniciar_servidor)
thread_iniciar_servidor.start()

janela_servidor.mainloop()
