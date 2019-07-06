from flask import Flask, render_template, Response, request, redirect, url_for
from flask_login import login_user, login_required, current_user, UserMixin, LoginManager, logout_user
import os
import wmi
import pythoncom
import time
import threading

class User(UserMixin):
    pass

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

os.environ['WERKZEUG_RUN_MAIN'] = 'true'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(login):
    print(login)
    if login != 'andermirik':
        return;
    user = User()
    user.id = login
    return user

c = wmi.WMI()
processes = c.Win32_Process()
def process_thread():
    print('started')
    while True:
        try:
            pythoncom.CoInitialize()
            print('check')
            c = wmi.WMI()
            processes = c.Win32_Process()
            time.sleep(60)
        finally:
            pythoncom.CoUninitialize()

thread = threading.Thread(target=process_thread)
thread.start()

@app.route("/")
def index():
    return render_template('index.html', processes = processes)

@app.route("/trolling_message")
@login_required
def trolling_message_page():
    return render_template('trolling_message_page.html', processes = processes)

@app.route("/system")
@login_required
def system_page():
    return render_template('system_page.html', processes = processes)

@app.route("/task_manager")
@login_required
def task_manager_page():
    return render_template('task_manager_page.html', processes = processes)

@app.route("/login")
def login():
    return render_template('login.html', processes = processes)

@app.route("/login", methods=['POST'])
def authorization():
    login = request.form.get('login')
    password = request.form.get('password')
    rememberme = True if request.form.get('rememberme') else False

    if login=='andermirik' and password=='helloworld':
        user = User()
        user.id = login
        login_user(user, rememberme)
    return redirect(url_for('system_page'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=['POST'])
def shutdown():
    os.system('shutdown /s /t 0')
    return redirect(url_for('system_page'))

app.run(host='0.0.0.0', port=27003, debug=True)


















#
