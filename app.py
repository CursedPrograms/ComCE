from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json 

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatroom.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

with app.app_context():
    db.create_all()

def update_users_json():
    users = User.query.all()
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'nickname': user.nickname,
            'password': user.password,
            'messages': []
        }

        messages = Message.query.filter_by(user_id=user.id).all()
        for message in messages:
            user_data['messages'].append({
                'id': message.id,
                'content': message.content,
                'timestamp': message.timestamp
            })

        users_data.append(user_data)

    with open('instance/users.json', 'w') as json_file:
        json.dump(users_data, json_file, indent=4, default=str)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    content = data['content']
    user_id = session['user_id']

    message = Message(content=content, user_id=user_id)
    db.session.add(message)
    db.session.commit()

    update_users_json()
    emit('message', {'content': content, 'nickname': User.query.get(user_id).nickname}, broadcast=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        nickname = request.form['nickname']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(name=name, surname=surname, email=email, nickname=nickname, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            update_users_json()
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            error_info = str(e.orig)
            
            if 'UNIQUE constraint failed: user.email' in error_info:
                flash('Email already exists. Please choose a different email.')
            elif 'UNIQUE constraint failed: user.nickname' in error_info:
                flash('Nickname already exists. Please choose a different nickname.')
            else:
                flash('Registration failed. Please check your information and try again.')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_identifier = request.form['login_identifier']
        password = request.form['password']

        user = User.query.filter((User.email == login_identifier) | (User.nickname == login_identifier)).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your email/nickname and password.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
