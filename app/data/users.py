import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase, create_session


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    school_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    liter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    follow = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    messages_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chat_with = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


class InfoForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    school_year = StringField('Class', validators=[DataRequired()])
    liter = StringField('Liter', validators=[DataRequired()])
    profile = StringField('Profile', validators=[DataRequired()])
    photo_url = StringField('Photo url', validators=[DataRequired()])
    submit = SubmitField('Submit')


class News(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    img_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    likes = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')


class AddNews(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    img_url = StringField('Photo url', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Messages(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_from = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_read = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relation('User')


class Groups(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'messages_groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    messages = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class SendMessage(FlaskForm):
    text = StringField('', validators=[DataRequired()])
    submit = SubmitField('➤')
