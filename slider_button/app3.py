from flask import Flask, render_template, request, session, redirect, url_for
import socket

app = Flask(__name__, template_folder='templates3')
app.secret_key = 'uacj_ingenieria_key'

# Datos de acceso
USUARIO_CORRECTO = "admin"
PASSWORD_CORRECTO = "123"

def enviar_a_servidor(msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 5001))
        s.send(msg.encode())
        res = s.recv(1024).decode()
        s.close()
        return res
    except:
        return ""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == USUARIO_CORRECTO and pw == PASSWORD_CORRECTO:
            session['logeado'] = True
            return redirect(url_for('panel'))
        return "Usuario o contraseña incorrectos"
    return render_template('login.html')

@app.route('/panel')
def panel():
    if not session.get('logeado'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/set_led')
def set_led():
    if not session.get('logeado'): return "401"
    enviar_a_servidor(f"LED{request.args.get('led')}:{request.args.get('valor')}")
    return "OK"

@app.route('/check_button')
def check_button():
    if not session.get('logeado'): return ""
    res = enviar_a_servidor("CHECK")
    if "BTN1_ACTIVE" in res: return "SISTEMA ENCENDIDO|LED1_ON"
    if "BTN1_OFF" in res: return "SISTEMA APAGADO|LED1_OFF"
    if "BTN2_ACTIVE" in res: return "RED ENCENDIDA|LED2_ON"
    if "BTN2_OFF" in res: return "RED APAGADA|LED2_OFF"
    return ""

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
