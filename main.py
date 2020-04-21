import flask
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask import render_template, Flask, request
import users_api

from WEB.data import db_session
from WEB.data.users import User, RegisterForm, LoginForm, InfoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

def main():
    def load_user(user_id):
        pass

    def reqister():
        pass

    def login():
        pass

    def logout():
        pass

    def users():
        pass

if __name__ == '__main__':
    main()
