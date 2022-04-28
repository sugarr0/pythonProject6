from flask import Flask, redirect, make_response, render_template, request, abort, jsonify
from data.Cities import City
from data.aboutSport import AboutSport
from data.sport import Sport
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.db_session import global_init, create_session
from forms.loginForm import LoginForm
from forms.user import RegisterForm
from forms.test import TestForm
from requests import get, post
from data import users_resources
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    global_init('db/my.db')
    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UsersResource, '/api/users/<int:users_id>')
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = TestForm()
    return render_template('test.html', title='Авторизация', form=form)


@app.route('/wow/<int:ind>', methods=['GET', 'POST'])
def teste(ind):
    form = TestForm()
    if ind == 1:
        current_user.city = 'Грязи'
        return redirect("/")
    else:
        current_user.city = 'Липецк'
        return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        res = post("http://127.0.0.1:5000/api/users", json={'email': form.email.data,
                                                            'password': form.password.data,
                                                            'name': form.name.data,
                                                            'surname': form.surname.data,
                                                            'city': form.city.data,
                                                            }).json()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['POST', 'GET'])
def index():
    db_sess = create_session()
    cities = db_sess.query(City).all()
    ct = [c.city for c in cities]
    ind = [c.id for c in cities if c.city == current_user.city]
    if ind:
        sports_in_city = db_sess.query(AboutSport).filter(AboutSport.city_id == ind[0]).all()
        sports_id = [s.sport_id for s in sports_in_city]
        sports = db_sess.query(Sport).filter(Sport.id.in_(sports_id)).all()
    if request.method == 'POST':
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.city = request.form['city']
        db_sess.commit()
        return redirect("/")
    return render_template('index.html', title='Домашняя страница', cities=ct, sports=sports)


if __name__ == '__main__':
    main()
