import socket

HOST = '127.0.0.1'
PORT = 65432

def enviar_tarea(tarea):
    # 1. Crear el socket TCP del cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        try:
            # 2. Conectar al servidor
            cliente_socket.connect((HOST, PORT))
            print(f"[*] Conectado al servidor {HOST}:{PORT}")
            
            # 3. Enviar la tarea al servidor
            print(f"[*] Enviando tarea: '{tarea}'")
            cliente_socket.sendall(tarea.encode('utf-8'))
            
            # 4. Recibir el resultado del worker
            resultado = cliente_socket.recv(1024).decode('utf-8')
            print(f"[*] Resultado recibido del servidor: {resultado}")
            
        except ConnectionRefusedError:
            print("[ERROR] No se pudo conectar al servidor. Asegúrate de que esté corriendo.")

if __name__ == "__main__":
    print("=== CLIENTE DE TAREAS ===")
    tarea_ingresada = input("Ingresa una descripción para la nueva tarea: ")
    enviar_tarea(tarea_ingresada)