from flask import Flask
from flask import render_template, request, redirect, url_for
from message import Message


app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('list_messages'))

@app.route('/messages')
def list_messages():
    return render_template('messages.html', messages = Message.all())
