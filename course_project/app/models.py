from datetime import datetime
from app import db, login, app
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from sqlalchemy import PrimaryKeyConstraint
import sqlite3
from time import time
import jwt
import sys
#import flask_whooshalchemyplus as whooshalchemy


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    fio = db.Column(db.String(128))
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    image = db.Column(db.Text)

    book = db.relationship('Book', secondary='status', backref='users', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'http://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def get_book(id):
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        # нужно добавить какой-то способ указывать состояние книги
        # если пользователь не читал ее, то таблицы не будут связаны
        # придумать как это проверять
        cursor.execute("select title, author, image from book where id = %d", id)
        res = cursor.fetchall()
        print(res)
        return res

    def get_books(self):
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("select author, title, username, book.image, book.id from (user left outer join status on user.id == status.user_id) as us \
                    join book on us.book_id == book.id \
                    where us.id = (?)", (current_user.id, ))
        res = cursor.fetchall()
        return res

    def get_books_count(self):
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        cursor.execute("select count(book.id) from (user left outer join status on user.id == status.user_id) as us \
                    join book on us.book_id == book.id\
                    where us.id = (?)", (current_user.id, ))
        res = cursor.fetchall()
        return res[0][0]

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithm=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)



    # def user_books(self):
    #     return

    # def add(book):
    #     if not self.is_added(book):
    #         self.books.append(user)
    #
    # def is_added(self, book):
    #     return self.books.filter(status.book_id == user.id).count() > 0
    # нужно добавить функции добавления и удаления книг, но пока не знаю как
    # потому тчо в примере используется только одна таблица, а у меня их 2


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Book(db.Model):
    #__searchable__ = ['title']
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), index = True)
    about_book = db.Column(db.String(150))  # мб надо будет сделать больше
    author = db.Column(db.String(60), index = True)
    location = db.relationship('Location', uselist=False, backref='books')
    image = db.Column(db.Text)

    user = db.relationship(
        'User', secondary='status',
        backref='books', lazy='dynamic')

    def __repr__(self):
        return '<Book {}>'.format(self.image)

    def get_book(self, id):
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        # нужно добавить какой-то способ указывать состояние книги
        # если пользователь не читал ее, то таблицы не будут связаны
        # придумать как это проверять
        cursor.execute("select title, author, image from book where id = %d", id)
        res = cursor.fetchall()
        print(res)
        return res

#whooshalchemy.whoosh_index(app, Book)
    # @staticmethod
    # def read_image(filename):
    #     try:
    #         fin = open(filename, "rb")
    #         img = fin.read()
    #         return img
    #     except EOError, e:
    #         print('Error {}: {}'.format(e.args[0], e.args[1]))
    #         sys.exit(1)
    #     finally:
    #         if fin:
    #             fin.close
    #
    # # очень сомнительная функция, ее работу я не проверяла
    # # иначе можно сделать varchar(max) и хранить base64      $("#product_image").attr("src", "data:image/png;base64," + data["img"]);
    # def save_image(self, img, id):
    #     try:
    #         conn = sqlite3.connect('app.db')
    #         cursor = conn.cursor()
    #         data = read_image(img)
    #         binary = sqlite3.Binary(data)
    #         cur.execute("UPDATE book SET image = '(?)' WHERE id = (?)", binary, id)
    #         conn.commit()
    #     except lite.Error, e:
    #         if con:
    #             con.rollback()
    #
    #             print "Error %s:" % e.args[0]
    #             sys.exit(1)
    #     finally:
    #         if con:
    #             con.close()




class Status(db.Model):
    __tablename__ = 'status'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'book_id'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    status = db.Column(db.Integer)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelving = db.Column(db.Integer, index=True)
    shelf = db.Column(db.Integer, index=True)
    column = db.Column(db.Integer, index=True)
    position = db.Column(db.Integer, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
