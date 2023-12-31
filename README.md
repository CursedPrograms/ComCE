# ComCE

## ComCE - Flask Chatroom Application

ComCE is a simple Flask chatroom application with real-time messaging, user registration/login, and message history. It utilizes Flask-SocketIO for WebSocket communication and SQLAlchemy for database management. The application includes features such as secure password hashing, flash messages, and JSON data persistence.

## Getting Started

To run the ComCE chatroom locally, follow these steps:

## Clone the repository:

git clone https://github.com/CursedPrograms/ComCE.git
Navigate to the project directory:
cd ComCE
Install the required dependencies:
pip install -r requirements.txt
Run the application:
python app.py
Open your web browser and go to http://localhost:5000 to access the chatroom.

## Features

Real-time messaging with Flask-SocketIO.
User registration and login functionality.
Message history and user data persistence using a SQLite database.
Secure password hashing for user authentication.

## Project Structure

app.py
: The main application file containing the Flask application and routes.
static/styles
: Directory for CSS stylesheets.
templates
: Directory for HTML templates.
instance/users.json
: JSON file for storing user data persistently.
##Dependencies
Flask
Flask-SocketIO
SQLAlchemy
Werkzeug
