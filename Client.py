#!/usr/bin/env python3
from tkinter import *
import ssl
import threading
import socket
from tkinter.scrolledtext import ScrolledText

def send_message(x, client_socket, username, text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} » {message}".encode())

    entry_widget.delete(0, END)
    text_widget.configure(state='normal')
    text_widget.insert(END, f"{username} »» {message}\n")
    text_widget.see(END)
    text_widget.configure(state='disabled')

def List_users(client_socket):
    client_socket.sendall("!usuarios".encode())

def Exit_request(client_socket, username, root):
    
    client_socket.sendall(f"\n[!] El usuario {username} ha abandonado el chat\n".encode())
    
    client_socket.close()
    root.quit()
    root.destroy()


def receive_message(client_socket, text_widget):
    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            text_widget.configure(state='normal')
            text_widget.insert(END, message)
            text_widget.see(END)
            text_widget.configure(state='disabled')

        except:
           break 



def client_program():

    host = 'localhost'
    port = 1234

    #conexion + encriptado
    context = ssl._create_unverified_context()
    client_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=host)
    client_socket.connect((host, port))



    username = input("\n[+] Introduce tu nombre de usuario: ")
    client_socket.sendall(username.encode())

    # tkinter
    root = Tk()
    root.title("Chat")
    
    text_widget= ScrolledText(root, state='disabled', font=("Arial", 14))
    text_widget.pack(padx=10, pady=10, fill=BOTH, expand=1)

    frame_widget=Frame(root, bg="#6495DE")
    frame_widget.pack(padx=4, pady=5, fill=BOTH)

    entry_widget=Entry(frame_widget, font=("Arial", 14))
    entry_widget.bind("<Return>", lambda x: send_message(x, client_socket, username, text_widget, entry_widget))
    entry_widget.pack(side=LEFT, fill=BOTH, expand=True, pady=5, padx=5)

    thread = threading.Thread(target=receive_message, args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()

    # Botones

    button = Button(frame_widget, text="Enviar", command=lambda : send_message(None, client_socket, username, text_widget, entry_widget))
    button.pack(padx=5, pady=5, side=RIGHT)

    button_users = Button(root, text="Listar usuarios", command=lambda : List_users(client_socket))
    button_users.pack(padx=5, pady=5)

    button_salir = Button(root, text="salir", command=lambda : Exit_request(client_socket, username, root))
    button_salir.pack(padx=5, pady=5)


    root.mainloop()
    client_socket.close()

if __name__ == '__main__':
    client_program()



#si requieres hacer tu propio encriptado, usa:

# openssl genpkey -algorithm RSA -out server-key.key -aes256
# openssl req -new -key server-key.key -out server.csr
# openssl x509 -req -days 365 -in server.csr -signkey server-key.key -out server-cert.pem
# openssl rsa -in server-key.key -out server-key.key
# 
# Si quieres verificar que sea la conexion segura por man in the middle, puedes verific ar en encriptado con tshark
# 
# tshark -i lo -Tfields -e data.data 
#
# para cuando no tenga encriptado normalmenta haciendo: 
# 
# echo -n "<cadena en hex>" | tr -d ':' | xxd -ps -r; 
# sale el texto 
# 
# sale el texto, como esta encriptado y es de data, no se puede ver, entonces
#  tshark -i lo -Tfields -e data.json
# la cadena larga en hexadecimal es lo encriptado 
# y si tratamos de traducir no sale texto legible
# echo -n "<cadena en hex>" | tr -d ':' | xxd -ps -r; echo 
