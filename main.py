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
    db_session.global_init("db/fmschool.sqlite")
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/')
    def index():
        return render_template('index.html')

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
