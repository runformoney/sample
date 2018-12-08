
from flask import Flask, render_template, session, request,flash,redirect,url_for
from flask_socketio import SocketIO, emit, disconnect

import scipy.io.wavfile
import numpy as np
from collections import OrderedDict
import sys
import json
from dbStuff import DBHelper
import sklearn

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, binary=True)

db = DBHelper()
db.setup()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register.html')
def index2():
    return render_template('register.html')

@app.route('/addRegion', methods=['GET', 'POST'])
def addRegion():
    data = json.dumps(dict(request.form))
    a = list(json.loads(data).values())
    dataToQuery = []
    for element in a:
        dataToQuery.append(element[0])
    print(dataToQuery)
    if len(dataToQuery) > 0:
        resp = db.check_details(dataToQuery)
    else:
        resp = 0

    if resp == 1:
        return render_template('success.html')
    else:
        return render_template('failure.html')

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    #global thread
    #with thread_lock:
    #    if thread is None:
    #        thread = socketio.start_background_task(target=background_thread)
    session['audio'] = []
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('sample_rate', namespace='/test')
def handle_my_sample_rate(sampleRate):
    session['sample_rate'] = sampleRate
    # send some message to front
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': "sampleRate : %s" % sampleRate, 'count': session['receive_count'] })

@socketio.on('audio', namespace='/test')
def handle_my_custom_event(audio):
    #session['audio'] += audio
    #session['audio'] += audio.values()
    values = OrderedDict(sorted(audio.items(), key=lambda t:int(t[0]))).values()
    session['audio'] += values

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    #my_audio = np.array(session['audio'], np.float32)
    #scipy.io.wavfile.write('out.wav', 44100, my_audio.view('int16'))
    #print(my_audio.view('int16'))

    # https://stackoverflow.com/a/18644461/466693
    sample_rate = session['sample_rate']
    my_audio = np.array(session['audio'], np.float32)
    sindata = np.sin(my_audio)
    scaled = np.round(32767*sindata)
    newdata = scaled.astype(np.int16)
    scipy.io.wavfile.write('out.wav', sample_rate, newdata)

    session['audio'] = []
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)
