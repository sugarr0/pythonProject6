from flask import Flask, redirect, render_template
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user
from data.db_session import global_init, create_session
from forms.loginForm import LoginForm
from forms.user import RegisterForm
from forms.addJobForm import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    global_init('db/mars.db')
    db_sess = create_session()
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
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = create_session()
        if form.start_date.data == '':
            job = Jobs(
                team_leader=form.team_leader.data,
                job=form.job.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data
            )
        else:
            job = Jobs(
                team_leader=form.team_leader.data,
                job=form.job.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                start_date=form.start_date.data
            )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addJob.html', title='Регистрация работы', form=form)


@app.route('/')
@app.route('/index')
def index():
    user = "новый Колонист"
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    ind = [el.team_leader for el in jobs]
    team_leaders_names = []
    for indx in ind:
        use = db_sess.query(User).filter(User.id == indx).first()
        team_leaders_names.append(use.name + ' ' + use.surname)
    return render_template('index.html', title='Домашняя страница',
                           username=user, jobs=jobs, names=team_leaders_names)


if __name__ == '__main__':
    main()
