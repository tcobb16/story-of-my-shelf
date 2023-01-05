from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=4)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4)])


class EditForm(FlaskForm):
    """Form for editing profile"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=4)])
    image_url = StringField('(Optional) Image URL')



class SearchForm(FlaskForm):
    """Form for searching for book(s)"""

    title = StringField('title')
    author = StringField('author')
    genre = StringField('genre')


class ReturnedBooks(FlaskForm):
    """Return list of dicts of search results"""
    title = StringField('title')
    author = StringField('author')
    genre = StringField('genre')
    cover_img = StringField('thumbnail')


class FavoriteBooks(FlaskForm):
    title = StringField('title')
    author = StringField('author')
    genre = StringField('genre')
    cover_img = StringField('thumbnail')


class ToBeRead(FlaskForm):
    title = StringField('title')
    author = StringField('author')
    genre = StringField('genre')
    cover_img = StringField('thumbnail')


class ReadBooks(FlaskForm):
    title = StringField('title')
    author = StringField('author')
    genre = StringField('genre')
    cover_img = StringField('thumbnail')
