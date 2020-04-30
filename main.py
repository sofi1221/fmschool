import flask
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask import render_template, Flask, request
import users_api
import base64
from flask_login import current_user
from datetime import datetime

from .data import db_session
from .data.users import User, RegisterForm, LoginForm, InfoForm, News, AddNews, Messages, \
    SendMessage, Groups

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
                follow="",
                messages_ids='',
                chat_with=''
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
        arr1 = [int(x) for x in current_user.follow.split(',')[1:]]
        news = session.query(News).filter(News.user_id == user_id).all()
        news.reverse()
        arr = []
        for i in news:
            arr += [[int(x) for x in i.ids.split(',')[1:]]]
        return render_template('user.html', user=user, xxx=0, arr=arr, arr1=arr1, news=news)

    @app.route('/info/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_user(id):
        form = InfoForm()
        if request.method == "GET":
            session = db_session.create_session()
            job = session.query(User).filter(User.id == id).first()
            if job:
                form.name.data = job.name
                form.surname.data = job.surname
                form.email.data = job.email
                form.position.data = job.position
                form.phone.data = job.phone
                form.school_year.data = job.school_year
                form.liter.data = job.liter
                form.profile.data = job.profile
                form.photo_url.data = job.photo_url
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            job = session.query(User).filter(User.id == id).first()
            if job:
                job.name = form.name.data
                job.surname = form.surname.data
                job.email = form.email.data
                job.position = form.position.data
                job.phone = form.phone.data
                job.school_year = form.school_year.data
                job.liter = form.liter.data
                job.profile = form.profile.data
                job.photo_url = form.photo_url.data
                session.commit()
                return redirect('/user/' + str(id))
            else:
                abort(404)
        return render_template('info.html', form=form, xxx=0)

    @app.route('/follows/<int:id>')
    @login_required
    def friends(id):
        session = db_session.create_session()
        f = session.query(User).all()
        u = session.query(User).filter(User.id == id).first()
        arr_self = []
        arr_other = []
        for i in f:
            if str(i.id) in u.follow.split(','):
                arr_self += [i.id]
            if str(u.id) in i.follow.split(','):
                arr_other += [i.id]
        # print(arr_other, arr_self)
        return render_template('friends.html', friends=f, xxx=0, arr_self=arr_self,
                               arr_other=arr_other)

    @app.route('/to_follow/<int:id_self>/<int:id_other>', methods=['GET', 'POST'])
    @login_required
    def follow(id_self, id_other):
        session = db_session.create_session()
        f = session.query(User).filter(User.id == id_self).first()
        f.follow = f.follow + ',' + str(id_other)
        session.commit()
        return redirect('/follows/' + str(id_self))

    @app.route('/from_follow/<int:id_self>/<int:id_other>', methods=['GET', 'POST'])
    @login_required
    def unfollow(id_self, id_other):
        session = db_session.create_session()
        f = session.query(User).filter(User.id == id_self).first()
        f.follow = f.follow.split(',' + str(id_other))[0] + f.follow.split(',' + str(id_other))[-1]
        session.commit()
        return redirect('/follows/' + str(id_self))

    @app.route('/like/<int:id_self>/<int:id_news>', methods=['GET', 'POST'])
    @login_required
    def like(id_self, id_news):
        session = db_session.create_session()
        f = session.query(News).filter(News.id == id_news).first()
        if str(id_self) in f.ids.split(','):
            f.ids = f.ids.split(',' + str(id_self))[0] + f.ids.split(',' + str(id_self))[-1]
            f.likes -= 1
        else:
            f.ids = f.ids + ',' + str(id_self)
            f.likes += 1
        session.commit()
        return redirect('/#id_' + str(id_news))

    @app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def news_delete(id):
        session = db_session.create_session()
        job = session.query(News).filter(News.id == id).first()
        if job:
            session.delete(job)
            session.commit()
        else:
            # print(111)
            abort(404)
        return redirect('/user/' + str(current_user.id))

    @app.route('/add_news', methods=['GET', 'POST'])
    @login_required
    def add_news():
        form = AddNews()
        if form.validate_on_submit():
            session = db_session.create_session()
            job = News(
                text=form.text.data,
                user_id=current_user.id,
                img_url=form.img_url.data,
                likes=0,
                ids='',
                date=datetime.now().strftime("%d/%m/%y %H:%M")
            )
            session.add(job)
            session.commit()
            return redirect('/')
        return render_template('add_news.html', form=form)

    @app.route('/news_edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_news(id):
        form = AddNews()
        if request.method == "GET":
            session = db_session.create_session()
            job = session.query(News).filter(News.id == id).first()
            if job:
                form.text.data = job.text
                form.img_url.data = job.img_url
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            job = session.query(News).filter(News.id == id).first()
            if job:
                job.text = form.text.data
                job.img_url = form.img_url.data
                session.commit()
                return redirect('/user/' + str(current_user.id))
            else:
                abort(404)
        return render_template('add_news.html', form=form)

    @app.route('/messages/<int:id>', methods=['GET', 'POST'])
    @login_required
    def messages(id):
        form = SendMessage()

        if form.validate_on_submit():
            session = db_session.create_session()
            job = Messages(
                text=form.text.data,
                user_from=current_user.id,
                date=datetime.now().strftime("%d/%m/%y %H:%M"),
                is_read=0
            )
            # print(datetime.now().strftime("%d/%m/%y %H:%M"))
            session.add(job)
            session.commit()

            session = db_session.create_session()
            g = session.query(Groups).get(id)
            g.messages += ',' + str(session.query(Messages).all()[-1].id)
            g.last_time = datetime.now().strftime("%d/%m/%y %H:%M")
            s = form.text.data
            if len(s) >= 50:
                s = s[:47] + '...'
            g.last = s
            session.commit()
            form.text.data = ''
        session = db_session.create_session()
        g = session.query(Groups).get(id)
        arr = g.messages.split(',')[1:]
        session = db_session.create_session()
        x1 = session.query(Messages).filter(Messages.user_from != current_user.id, Messages.is_read == 0).all()
        for w in x1:
            if str(w.id) in arr:
                w.is_read = 1
                session.commit()
        f = [session.query(Messages).get(int(x)) for x in arr]
        return render_template('messages.html', messages=f, xxx=0, form=form)

    @app.route('/messages')
    @login_required
    def messages_g():
        session = db_session.create_session()
        arr = [int(x) for x in session.query(User).get(current_user.id).messages_ids.split(',')[1:]]
        m = [session.query(Groups).get(x) for x in arr]
        m.sort(key=lambda x: datetime.strptime(x.last_time, "%d/%m/%y %H:%M"), reverse=True)
        x = [[session.query(User).get(int(y)) for y in x.users.split(',')[1:] if
              y != str(current_user.id)][0] for x in m]
        arr_count = []
        for i in m:
            x1 = session.query(Messages).filter(Messages.user_from != current_user.id,
                                                Messages.is_read == 0).all()
            s = 0
            arr__ = i.messages.split(',')[1:]
            for w in x1:
                if str(w.id) in arr__:
                    s += 1
            arr_count += [s]
        arr_my_read = []
        for i in m:
            try:
                mess = session.query(Messages).get(int(i.messages.split(',')[-1]))
                if mess.user_from == current_user.id and mess.is_read == 0:
                    arr_my_read += [1]
                else:
                    arr_my_read += [0]
            except Exception as e:
                arr_my_read += [0]
        return render_template('groups.html', xxx=0, m=m, x=x, c=arr_count, amr=arr_my_read)

    @app.route('/is_message/<int:id>')
    @login_required
    def messages_is(id):
        session = db_session.create_session()
        other = session.query(User).get(id)
        arr = [int(x) for x in session.query(User).get(current_user.id).chat_with.split(',')[1:]]
        if other.id in arr:
            return redirect('/messages')
        else:
            me = session.query(User).get(current_user.id)
            me.chat_with += ',' + str(id)
            session.commit()
            group = Groups(
                messages='',
                users=f',{current_user.id},{id}',
                last='No messages',
                last_time=datetime.now().strftime("%d/%m/%y %H:%M")
            )
            session.add(group)
            session.commit()
            m = session.query(Groups).all()
            m1 = [x.id for x in m]
            me = session.query(User).get(current_user.id)
            me.messages_ids += ',' + str(m1[-1])
            session.commit()
            me = session.query(User).get(id)
            me.messages_ids += ',' + str(m1[-1])
            session.commit()
            return redirect('/messages')

    app.run()


if __name__ == '__main__':
    main()
