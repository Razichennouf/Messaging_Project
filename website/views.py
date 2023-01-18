from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Message
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        message = request.form.get('message')

        if len(message) < 1:
            flash('Write a message !.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent !', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-message', methods=['POST'])
def delete_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return jsonify({})
