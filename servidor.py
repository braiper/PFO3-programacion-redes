import socket
from concurrent.futures import ThreadPoolExecutor
import time

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 65432
MAX_WORKERS = 5 # Nuestro pool de hilos tendrá 5 workers disponibles

def procesar_tarea(conn, addr):
    """
    Esta función representa el trabajo de un Worker.
    Se ejecuta en un hilo separado para cada cliente.
    """
    print(f"[WORKER] Nueva conexión asignada desde {addr}")
    try:
        # Recibir datos del cliente
        datos = conn.recv(1024).decode('utf-8')
        if datos:
            print(f"[WORKER] Tarea recibida de {addr}: {datos}")
            
            # Simulamos que el worker tarda un tiempo en procesar la tarea (ej. guardando en DB)
            time.sleep(2) 
            
            # Resultado de la tarea
            respuesta = f"Tarea '{datos}' procesada con éxito por el servidor."
            conn.sendall(respuesta.encode('utf-8'))
            print(f"[WORKER] Respuesta enviada a {addr}")
    except Exception as e:
        print(f"[ERROR] Problema con el cliente {addr}: {e}")
    finally:
        # Cerramos la conexión específica de este cliente
        conn.close()
        print(f"[WORKER] Conexión cerrada con {addr}\n")

def iniciar_servidor():
    # 1. Crear el socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        # Evita el error de "puerto en uso" si reinicias rápido el script
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 2. Vincular a la IP y Puerto (Bind)
        servidor_socket.bind((HOST, PORT))
        
        # 3. Escuchar conexiones entrantes (Listen)
        servidor_socket.listen()
        print(f"[*] Servidor distribuido escuchando en {HOST}:{PORT}")
        print(f"[*] Pool de hilos configurado con {MAX_WORKERS} workers...\n")

        # 4. Crear el Pool de Hilos para manejar clientes concurrentes
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ejecutor:
            while True:
                # 5. Aceptar la conexión (Accept)
                conn, addr = servidor_socket.accept()
                
                # 6. Distribuir a los workers: Enviamos la conexión al pool de hilos
                # El servidor principal sigue libre inmediatamente para aceptar otro cliente
                ejecutor.submit(procesar_tarea, conn, addr)

if __name__ == "__main__":
    iniciar_servidor()