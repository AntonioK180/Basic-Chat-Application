from flask import Flask
from flask import render_template, request, redirect, url_for
from message import Message
from friend import Friend


app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('show_friends'))

@app.route('/messages')
def list_messages():
    return render_template('messages.html', messages=Message.all())

@app.route('/friends')
def show_friends():
    return render_template('friends.html', friends=Friend.all())

@app.route('/friends/<int:friend_id>')
def show_chat(friend_id):
    friend = Friend.find(friend_id)

    return render_template('friend.html', friend=friend, messages=Message.all())

@app.route('/message/new', methods=['POST'])
def new_message():
    if request.method == 'POST':
        friend = Friend.find(request.form['friend_id'])
        values = (None, friend.friend_id, friend.name, request.form['message'])
        Message(*values).create()

        return redirect(url_for('show_chat', friend_id=friend))
