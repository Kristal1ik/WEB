from flask import Flask, render_template, redirect, request, make_response, session, url_for
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session
from templates.news import NewsForm
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


@app.route("/index")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user))
        print('l')

    else:
        news = db_sess.query(News)
        print(news)
        print('ll')

    return render_template("index.html", news=news)


@app.route('/')
def start():
    return render_template('baseNEW.html')


@app.route('/home_page')
@login_required
def home():
    return render_template('home_page.html')


@app.route('/subjects_page')
@login_required
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
@login_required
def choice():
    return render_template('choice.html')


@app.route("/test_create3", methods=["POST", "GET"])
@login_required
def test_create3():
    if request.method == "POST":
        user = request.form["one"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("test_create3.html")


@app.route("/test_create5", methods=["POST", "GET"])
@login_required
def test_create5():
    if request.method == "POST":
        user = request.form["one"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("test_create5.html")


@app.route("/test_create10", methods=["POST", "GET"])
@login_required
def test_create10():
    if request.method == "POST":
        user = request.form["one"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("test_create10.html")


@app.route('/question', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        # news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/recorded')
    return render_template('question.html',
                           form=form, title='Добавить вопрос')


@app.route('/recorded')
@login_required
def recorded():
    return render_template('recorded.html')


@app.route('/question/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/index')
        else:
            abort(404)
    return render_template('question.html',
                           form=form, title='Редактирование вопроса')


@app.route('/question_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/index')


@app.route("/subjects_page/<usr>")
@login_required
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == '__main__':
    main()
    app.run(port=4020, host='127.0.0.1')
