#taskkill /f /im python.exe


from flask import Flask, render_template, flash, redirect, session, url_for, request, abort
from forms import LoginForm

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/kuku')
def hi():  # put application's code here
    return 'sdfsdf!'


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flash(f"Зашел пользователь под логином {form.username.data}, запомнить = {form.remember_me.data}")
        return redirect('/index')

    return render_template('login.html', title='Авторизация пользователя', form=form)

@app.route('/login2',methods=['POST','GET'])
def login2():
    if 'userlogged' in session:
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'kolya' and request.form['psw'] == '111':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'vasya' and request.form['psw'] == '112':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'tolya' and request.form['psw'] == '113':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'igor' and request.form['psw'] == '114':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'maks' and request.form['psw'] == '115':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] == 'og buda' and request.form['psw'] == '111':
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile',username=session['userlogged']))




    return render_template('login_2var.html', title='Авторизация пользователя')

@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f"<h1> Пользователь {username} зашел"


@app.route('/')
@app.route('/index')
def index():  # put application's code here


    return render_template('index.html')


@app.route('/petya/')
def petya():  # put application's code here
    return ''' <h2> Александр Твардовский

Василий Теркин. Сборник

Лирика

РОДНОЕ

<br>Дорог израненные спины, </br>
<br>О дальних шумных городах. </br>
    </h2> '''


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
