import socket
import time
import random

# Datos de prueba
palabras_ejemplo = ["get", "set", "main", "init", "data", "process", "value", "update", "result", "connect"]

def start_mock_miner():
    host = "127.0.0.1"
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Miner de prueba esperando en el puerto {port}...")
        conn, addr = s.accept()
        with conn:
            print(f"Visualizer conectado desde {addr}")
            while True:
                # Elige una palabra al azar y la envía con \n
                palabra = random.choice(palabras_ejemplo)
                conn.sendall(f"{palabra}\n".encode("utf-8"))
                print(f"Enviado: {palabra}")
                time.sleep(0.5) # Envía una palabra cada medio segundo

if __name__ == "__main__":
    start_mock_miner()