from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


favorites = db.Table(
    'favorites', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', primary_key=True)),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', primary_key=True)),
)


to_be_read = db.Table(
    'to_be_read',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', primary_key=True)),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', primary_key=True)),
)


read = db.Table(
    'read',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', primary_key=True)),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id', primary_key=True)),
)


class Users(db.Model):
    """User of app"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    profile_pic_url = db.Column(
        db.Text,
        default="/static/images/default-profile-pic.png",
    )

    favorites = db.relationship('Books', secondary=favorites, lazy='subquery', backref=db.backref('users_favorites', lazy=True))

    to_be_read = db.relationship('Books', secondary=to_be_read, lazy='subquery', backref=db.backref('users_to_be_read', lazy=True))

    read = db.relationship('Books', secondary=read, lazy='subquery', backref=db.backref('users_read', lazy=True))

    @classmethod
    def signup(cls, username, email, password, profile_pic_url):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
            username=username,
            email=email,
            password=hashed_pwd,
            profile_pic_url=profile_pic_url,
        )

        db.session.add(user)
        return user
        
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Books(db.Model):
    """Individual books"""

    __tablename__ = 'books'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    author = db.Column(
        db.Integer,
        db.ForeignKey('authors.id'),
        unique=True,
    )

    genre = db.Column(
        db.Text,
    )

    cover_img = db.Column(
        db.Text,
    )


class Authors(db.Model):
    """Authors"""

    __tablename__ = 'authors'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )


def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)


    