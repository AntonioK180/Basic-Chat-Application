from flask import Flask
from flask import render_template, request, redirect, url_for
import logging
from message import Message
from friend import Friend


app = Flask(__name__)


logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
fileHandler = logging.FileHandler("flask-app.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)

app.logger.info("Logging is set up.")


my_id = 9
my_name = "Antonio"


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
        added_friend = Friend(None, name, None).create()

    app.logger.debug('Friend with name: %s was just added.', added_friend.name)
    return redirect(url_for('show_friends'))


@app.route('/friends/<int:friend_id>/delete', methods=['POST'])
def delete_friend(friend_id):
    friend = Friend.find(friend_id)
    friend.delete()

    app.logger.debug('Friend with name: %s was just deleted.', friend.name)
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

        app.logger.debug('The nickname for %s was edited.', friend.name)
        return redirect(url_for('show_chat', friend_id=friend.friend_id))


@app.route('/message/new', methods=['POST'])
def new_message():
    if request.method == 'POST':
        friend = Friend.find(request.form['friend_id'])
        values = (None, my_id, friend.friend_id, my_name, request.form['message'])
        Message(*values).create()

        app.logger.debug('%s just received a new message.', friend.name)
        return redirect(url_for('show_chat', friend_id=friend.friend_id))
