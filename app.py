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


@app.route('/friends/new', methods=['POST'])
def new_friend():
    if request.method == 'POST':
        name = request.form['friend_name']
        Friend(None, name, None).create()

    return redirect(url_for('show_friends'))


@app.route('/friends/<int:friend_id>')
def show_chat(friend_id):
    friend = Friend.find(friend_id)

    return render_template('friend.html', friend=friend, messages=Message.all_with(friend_id))


@app.route('/friends/<int:friend_id>/edit', methods=['GET', 'POST'])
def edit_nickname(friend_id):
    friend = Friend.find(friend_id)
    if request.method == 'GET':

        return render_template('edit_nickname.html', friend=friend)
    elif request.method == 'POST':
        friend.nickname = request.form['nickname']
        friend.save()

        return redirect(url_for('show_chat', friend_id=friend.friend_id))


@app.route('/friends/<int:friend_id>/delete', methods=['POST'])
def delete_friend(friend_id):
    friend = Friend.find(friend_id)
    friend.delete()

    return redirect(url_for('show_friends'))


@app.route('/message/new', methods=['POST'])
def new_message():
    if request.method == 'POST':
        friend = Friend.find(request.form['friend_id'])
        values = (None, my_id, friend.friend_id, my_name, request.form['message'])
        Message(*values).create()

        return redirect(url_for('show_chat', friend_id=friend.friend_id))
