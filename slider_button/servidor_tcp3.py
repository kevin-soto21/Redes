import serial, socket, threading

SERIAL_PORT = '/dev/ttyACM0'
TCP_PORT = 5001
ultimo_evento = ""

try:
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=0.1)
except:
    print("ERROR: No se pudo conectar con el Arduino")

def leer_arduino():
    global ultimo_evento
    while True:
        try:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').strip()
                if linea: ultimo_evento = linea
        except: pass

def iniciar():
    global ultimo_evento
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', TCP_PORT))
    s.listen(5)
    while True:
        c, a = s.accept()
        data = c.recv(1024).decode().strip()
        if data == "CHECK":
            c.send(ultimo_evento.encode())
            ultimo_evento = ""
        elif ":" in data:
            ser.write((data + "\n").encode())
            c.send(b"OK")
        c.close()

threading.Thread(target=leer_arduino, daemon=True).start()
iniciar()
