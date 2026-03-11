#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import signal
import time
import threading
import serial

HOST = "0.0.0.0"
PORT = 5001

BAUD = 115200
SERIAL_PORT = "/dev/ttyACM0"   # Ajusta a /dev/ttyACM1 o /dev/ttyUSB0 si es necesario

_running = True
_lock = threading.Lock()

def handle_sig(*_):
    global _running
    _running = False

def open_serial():
    # Aumentamos el timeout a 7 segundos para que dé tiempo al movimiento suave (5s)
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=7)
    time.sleep(2.0)  # Espera a que el Arduino termine de resetearse
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    print(f"[SERIAL] Conectado a {SERIAL_PORT} @ {BAUD}")
    return ser

def send_to_arduino(ser, cmd):
    # Limpiamos basura previa del buffer para leer la respuesta fresca
    ser.reset_input_buffer() 
    
    ser.write((cmd.strip() + "\n").encode("utf-8"))
    ser.flush()
    
    # Leemos la línea de respuesta del Arduino
    resp = ser.readline().decode("utf-8", errors="ignore").strip()
    
    # Si resp está vacío después de 7 segundos, devolvemos error
    if not resp:
        return "ERR: Timeout (Arduino no respondió)"
    return resp

def main():
    global _running
    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    try:
        ser = open_serial()
    except Exception as e:
        print(f"[ERROR] No se pudo abrir el puerto serial: {e}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        s.settimeout(0.5)

        print(f"[TCP] Escuchando en {HOST}:{PORT}")

        while _running:
            try:
                conn, _ = s.accept()
            except socket.timeout:
                continue

            with conn:
                conn.settimeout(8.0) # Tiempo de espera del socket ligeramente mayor al serial
                data = b""
                try:
                    while True:
                        chunk = conn.recv(1024)
                        if not chunk:
                            break
                        data += chunk
                        if b"\n" in data:
                            break
                except socket.timeout:
                    pass

                msg = data.decode("utf-8", errors="ignore").strip()
                if not msg:
                    conn.sendall(b"ERR comando vacio\n")
                    continue

                # Procesar comando
                parts = msg.split()
                if len(parts) == 1:
                    cmd = f"A {parts[0]}"
                else:
                    cmd = f"{parts[0].upper()} {parts[-1]}"

                try:
                    with _lock:
                        # Enviamos a Arduino y esperamos la respuesta (hasta 7s)
                        resp = send_to_arduino(ser, cmd)
                    
                    # Enviamos la respuesta real del Arduino de vuelta al app.py -> index.html
                    conn.sendall((resp + "\n").encode("utf-8"))
                except Exception as e:
                    conn.sendall((f"ERR {e}\n").encode("utf-8"))

    try:
        ser.close()
    except Exception:
        pass
    print("Servidor TCP cerrado correctamente.")

if __name__ == "__main__":
    main()
