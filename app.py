#taskkill /f /im python.exe

import datetime
import sqlite3


from flask import Flask, render_template, flash, redirect, session, url_for, request, abort, g

from fdatabase import FDataBase
from forms import LoginForm
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'fdb.db')))
app.pergament_session_lifetime = datetime.timedelta(seconds=60)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
def get_db():
    if not  hasattr(g,'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()



@app.route('/kuku')
def hi():  # put application's code here
    return 'sdfsdf!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    database = FDataBase(db)
    # put application's code here
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flash(f"Зашел пользователь под логином {form.username.data}, запомнить = {form.remember_me.data}")
        return redirect('/index')

    return render_template('login.html', title='Авторизация пользователя', form=form,menu=database.getMenu())

@app.route('/login2',methods=['POST','GET'])
def login2():
    db = get_db()
    database = FDataBase(db)
    if 'userlogged' in session:
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'kolya' and request.form['psw'] == '111':
        session['userlogged'] = request.form['username']
    return render_template('login_2var.html', title='Авторизация пользователя',menu=database.getMenu())


@app.route('/post', methods=['POST', 'GET'])
def post():
    db = get_db()
    database = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['post']) > 10:
            res = database.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ты дурак', category='error')
            else:
                flash('Ты не дурак', category='success')
        else:
            flash('Ты полный дурак', category='error')

    return render_template('post.html', title='Добавить статью', menu=database.getMenu())


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f"<h1> Пользователь {username} зашел"


@app.route('/')
@app.route('/index')
def index():  # put application's code here
    db = get_db()
    database = FDataBase(db)


    return render_template('index.html',menu=database.getMenu())


@app.route('/allposts')
def allposts():  # put application's code here
    db = get_db()
    database = FDataBase(db)
    return render_template('allposts.html', title='Список постов', menu=database.getMenu(),
                           posts=database.getPostsAnnonce())



@app.route('/post/<int:id_post>')
def showPosts(id_post):  # put application's code here
    db = get_db()
    database = FDataBase(db)
    title, aticle = database.getPost(id_post)
    if not title:
        abort(404)

    return render_template('aticle.html', title='Список постов', menu=database.getMenu(),
                           post=aticle)


@app.route('/p')
def p():
    # put application's code here
    return render_template('p.html')


# @app.route('/user/<username>')
# def user_profile(username):  # put application's code here
#     return f"<h1>Здраствуй дорогой пользователь {username}</h1>"
#
#
# @app.route('/user/<int:post_id>')
# def show_post(post_id):  # put application's code here
#     return f"<h1>Горячая и свежая новость № {post_id}</h1>"


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена,уходи')

@app.errorhandler(401)
def page_not_found(error):
    return render_template('errlog.html', title='Сначала войдите в систему')


if __name__ == '__main__':
    app.run(debug=True)
