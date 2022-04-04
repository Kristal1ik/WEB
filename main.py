import json

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/8")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/')
def start():
    return render_template('base.html')

@app.route('/home_page')
def home():
    return render_template('home_page.html')

if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
