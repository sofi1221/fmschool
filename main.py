import flask
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask import render_template, Flask, request
import users_api
from flask_login import current_user

from WEB.data import db_session
from WEB.data.users import User, RegisterForm, LoginForm, InfoForm, News

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
        session = db_session.create_session()
        news = session.query(News).all()
        news.reverse()
        arr = []
        for i in news:
            arr += [[int(x) for x in i.ids.split(',')[1:]]]
        return render_template('index.html', xxx=0, news=news, arr=arr)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                position=form.position.data,
                email=form.email.data,
                phone=form.phone.data,
                photo_url="https://ramcotubular.com/wp-content/uploads/default-avatar.jpg",
                follow=""
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', form=form, xxx=1)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', form=form, xxx=1)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/user/<int:user_id>', methods=['GET', 'POST'])
    def users(user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        arr = [int(x) for x in current_user.follow.split(',')[1:]]
        return render_template('user.html', user=user, xxx=0, arr=arr)



if __name__ == '__main__':
    main()
