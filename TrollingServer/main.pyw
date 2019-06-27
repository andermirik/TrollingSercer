from flask import Flask, render_template, Response, request, redirect, url_for
import os
import wmi
import pythoncom
import time
import threading

app = Flask(__name__)

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
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


@app.route("/")
def index():
    pythoncom.CoInitialize()
    return render_template('index.html', processes = processes)

@app.route("/trolling_message")
def trolling_message_page():
    pythoncom.CoInitialize()
    return render_template('trolling_message_page.html', processes = processes)

@app.route("/system")
def system_page():
    pythoncom.CoInitialize()
    return render_template('system_page.html', processes = processes)

@app.route("/task_manager")
def task_manager_page():
    pythoncom.CoInitialize()
    return render_template('task_manager_page.html', processes = processes)


@app.route("/", methods=['POST'])
def move_forward():
    os.system('shutdown /s /t 0')
    return render_template('index.html')

os.environ['WERKZEUG_RUN_MAIN'] = 'true'


thread = threading.Thread(target=process_thread)
thread.start()
app.run(host='0.0.0.0', port=27003)
