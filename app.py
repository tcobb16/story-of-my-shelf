import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import AddUserForm, LoginForm, SearchForm, EditForm
from models import db, connect_db, Users, Books
from api import search_books

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///books'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """Add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = Users.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                profile_pic_url=form.image_url.data or Users.profile_pic_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/login")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/user-home")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash(f"Goodbye!", "success")

    return redirect("/login")


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Show Logged in user home page or general home page"""

    if g.user:

        return redirect(url_for('.user_homepage')) 

    else:
        return render_template('gen-home.html')


@app.route('/user-home', methods=['GET', 'POST'])
def user_homepage():
    """Show logged in user home page"""
    if request.form:
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        return redirect(url_for('.get_books', title=title, author=author, genre=genre))

    return render_template('user-home.html', user=g.user, form=SearchForm())


@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST'])
def favorites(user_id):
    """show list of user's favorite books or add books to list"""
    if request.method == 'POST':
        if request.form:
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            cover_img = request.form['cover_img']
            favorited_book = Books.query.filter_by(title=title, author=author, genre=genre).first()

            if favorited_book is None:
                db.session.add(Books(title, author, genre, cover_img=cover_img))
                db.session.commit()
                favorited_book = Books.query.filter_by(title=title, author=author, genre=genre).first()
                if not favorited_book:
                    return ('Error adding new book to database', 500)


            user = Users.query.get_or_404(user_id)
            if favorited_book in user.favorites:
                print (f'Removing {favorited_book.id} {title} from Favorites')
                user.favorites.remove(favorited_book)
            else:
                print (f'Adding {favorited_book.id} {title} to Favorites')
                user.favorites.append(favorited_book)
            db.session.commit()
            return render_template('favorites.html', books=user.favorites, user_id=user_id)

        
        else:
            return ('bad request', 400)

    user = Users.query.get_or_404(user_id)


    return render_template('favorites.html', books=user.favorites, user_id=user_id)


@app.route('/users/<int:user_id>/read', methods=['GET', 'POST'])
def readbooks(user_id):
    """show list of user's already read books"""

    if request.method == 'POST':
        if request.form:
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            cover_img = request.form['cover_img']
            read_book = Books.query.filter_by(title=title, author=author, genre=genre).first()

            if read_book is None:
                db.session.add(Books(title, author, genre, cover_img=cover_img))
                db.session.commit()
                read_book = Books.query.filter_by(title=title, author=author, genre=genre).first()
                if not read_book:
                    return ('Error adding new book to database', 500)


            user = Users.query.get_or_404(user_id)
            if read_book in user.read:
                print (f'Removing {read_book.id} {title} from Read')
                user.read.remove(read_book)
            else:
                print (f'Adding {read_book.id} {title} to Read')
                user.read.append(read_book)
            db.session.commit()
            return render_template('read.html', books=user.read, user_id=user_id)
    
        else:
            return ('bad request', 400)

    user = Users.query.get_or_404(user_id)

    return render_template('read.html', books=user.read, user_id=user_id)


@app.route('/users/<int:user_id>/want-to-read', methods=['GET', 'POST'])
def to_read(user_id):
    """show list of user's to be read books"""
    if request.method == 'POST':
        if request.form:
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            cover_img = request.form['cover_img']
            to_be_read_book = Books.query.filter_by(title=title, author=author, genre=genre).first()

            if to_be_read_book is None:
                db.session.add(Books(title, author, genre, cover_img=cover_img))
                db.session.commit()
                to_be_read_book = Books.query.filter_by(title=title, author=author, genre=genre).first()
                if not to_be_read_book:
                    return ('Error adding new book to database', 500)


            user = Users.query.get_or_404(user_id)
            if to_be_read_book in user.to_be_read:
                print (f'Removing {to_be_read_book.id} {title} from To Be Read')
                user.to_be_read.remove(to_be_read_book)
            else:
                print (f'Adding {to_be_read_book.id} {title} to To Be Read')
                user.to_be_read.append(to_be_read_book)
            db.session.commit()
            return render_template('to-be-read.html', books=user.to_be_read, user_id=user_id)

        else:
            return ('bad request', 400)

    user = Users.query.get_or_404(user_id)

    return render_template('to-be-read.html', books=user.to_be_read, user_id=user_id)


@app.route('/books')
def get_books():
    """search for books by title, author, and/or genre"""
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')

    returned_books = search_books(title=title, author=author, genre=genre)

    return render_template('search-results.html', user_id=g.user.id, books=returned_books)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """edit user profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = Users.query.get_or_404(user_id)

    if request.form:
        
        user.username = request.form['username']
        user.email = request.form['email']
        user.image_url = request.form['image_url'] if request.form['image_url'] else '/static/images/default-profile-pic.jpeg'

        db.session.commit()
        return redirect('/user-home')

    return render_template('edit.html', user=user, form=EditForm())
