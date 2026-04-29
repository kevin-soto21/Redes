import socket
import serial
import time

HOST = "0.0.0.0"
PORT = 5001

SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 9600

def conectar_arduino():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
        time.sleep(2)
        print("Arduino conectado en", SERIAL_PORT)
        return arduino
    except Exception as e:
        print("Error al conectar Arduino:", e)
        return None

arduino = conectar_arduino()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Servidor TCP escuchando en {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print("Cliente conectado:", addr)

    try:
        data = conn.recv(1024).decode().strip()
        print("Dato recibido:", data)

        if data in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if arduino is not None:
                arduino.write((data + "\n").encode())

                respuesta = arduino.readline().decode().strip()
                print("Arduino respondió:", respuesta)

                conn.sendall(respuesta.encode())
            else:
                conn.sendall("ERR:ARDUINO_NO_CONECTADO".encode())
        else:
            conn.sendall("ERR:NUMERO_INVALIDO".encode())

    except Exception as e:
        print("Error:", e)
        conn.sendall("ERR:SERVIDOR_TCP".encode())

    finally:
        conn.close()
