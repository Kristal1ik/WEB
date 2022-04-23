from flask import Flask, render_template, redirect, request, make_response, session, url_for
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/j")
def index():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/home_page")
        return render_template('index.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('index.html', title='Авторизация', form=form)


# @app.route("/8")
# def index():
#     db_sess = db_session.create_session()
#     if current_user.is_authenticated:
#         news = db_sess.query(News).filter(
#             (News.user == current_user) | (News.is_private != True))
#     else:
#         news = db_sess.query(News).filter(News.is_private != True)
#     return render_template("index.html", news=news)


@app.route('/')
def start():
    return render_template('baseNEW.html')


@app.route('/home_page')
def home():
    return render_template('home_page.html')


@app.route('/subjects_page')
def subjects_page():
    return render_template('subjects_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/home_page")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/choice')
def choice():
    return render_template('choice.html')


@app.route('/test_create3')
def test_create3():
    return render_template('test_create3.html')


@app.route('/test_create5')
def test_create5():
    return render_template('test_create5.html')


@app.route('/test_create10')
def test_create10():
    return render_template('test_create10.html')


@app.route("/login2", methods=["POST", "GET"])
def login2():
    if request.method == "POST":
        userr = request.form["sm"]
        return redirect(url_for("user", usr=userr))
    else:
        return render_template("test_create3.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    main()
    app.run(port=4007, host='127.0.0.1')
