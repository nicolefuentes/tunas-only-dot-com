from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/messageboard')
def messageboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id'],
    }
    user=User.get_by_id(data)
    all_users=User.get_by_id_except(data)
    messages=Message.get_by_conversation(data)
    return render_template("messageboard.html", user=user, all_users=all_users, messages=messages)


@app.route('/send-message', methods=['POST'])
def create_new():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        'message': request.form['message'],
        'sender_id': request.form['sender_id'],
        'recipient_id': request.form['recipient_id']
    }
    Message.save(data)
    return redirect('/messageboard')

@app.route('/destroy/<int:message_id>')
def destroy(message_id):
    data ={
        'message_id': message_id
    }
    Message.destroy(data)
    return redirect('/messageboard')