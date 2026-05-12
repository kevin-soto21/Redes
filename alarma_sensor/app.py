import serial
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'uacj_ingenieria'
socketio = SocketIO(app)

# Conexión Serial
try:
    # Recuerda que en Ubuntu suele ser /dev/ttyACM0
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    ser = None
    print("⚠️ Arduino no detectado.")

def monitor_serial():
    global ser
    while True:
        if ser and ser.in_waiting > 0:
            try:
                linea = ser.readline().decode('utf-8').strip()
                if "ALERTA" in linea:
                    socketio.emit('aviso')
            except:
                pass

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'kevin' and request.form['password'] == 'uacj':
            session['logged_in'] = True
            return redirect(url_for('monitor'))
        return "<h3>Credenciales incorrectas</h3>"
    return render_template('login.html')

@app.route('/monitor')
def monitor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=monitor_serial, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
