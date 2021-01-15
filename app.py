from flask import Flask
from flask import render_template, request, redirect, url_for
from message import Message
from friend import Friend

my_id = 9
my_name = "Antonio"

app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('show_friends'))

@app.route('/friends')
def show_friends():
    return render_template('friends.html', friends=Friend.all())

@app.route('/friends/<int:friend_id>')
def show_chat(friend_id):
    friend = Friend.find(friend_id)

    return render_template('friend.html', friend=friend, messages=Message.all_with(friend_id))

@app.route('/message/new', methods=['POST'])
def new_message():
    if request.method == 'POST':
        friend = Friend.find(request.form['friend_id'])
        values = (None, my_id, friend.friend_id, my_name, request.form['message'])
        Message(*values).create()

        return redirect(url_for('show_chat', friend_id=friend.friend_id))
