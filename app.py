import webview
import threading
from multiprocessing import Process
from flask import Flask, render_template, request, session
from player import Player

WINDOW_TITLE = 'FakePiano'

app = Flask(__name__)
app.secret_key = 'secret-key-session-encryption'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    if not 'midi' in session or not 'sf2' in session:
        session['error'] = 'MIDI or SF2 not loaded'
    try:
        player = Player(session['sf2'], synth_gain=2)
        player.load_midi(session['midi'])
        player.load_track('right_hand', load_threshold=1)
        player.set_threshold(0.002)
        player.set_midi_in(b'Piano')
        player.start()
    except Exception as e:
        session['error'] = str(e)
    return index()

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if 'midi_file' in request.files:
        f = request.files['midi_file']
        session['midi'] = 'midi_files/'+f.filename
    elif 'sf2_file' in request.files:
        f = request.files['sf2_file']
        session['sf2'] = 'soundfonts/'+f.filename
    return index()

# Start flask
def start_flask():
    app.run()
server = Process(target=start_flask)
server.start()

# Start Program window
window = webview.create_window(WINDOW_TITLE, 'http://127.0.0.1:5000/')
webview.start()
window.toggle_fullscreen()

server.terminate()
server.join()