from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.db")
    db_sess = db_session.create_session()
    # app.run()
    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user1 = User()
    user1.name = "Rich"
    user1.surname = "Kay"
    user1.age = 20
    user1.position = "engineer"
    user1.speciality = "research engineer"
    user1.address = "module_2"
    user1.email = "kay_rich@mars.ru"
    db_sess.add(user1)

    user2 = User()
    user2.name = "Holly"
    user2.surname = "Kay"
    user2.age = 19
    user2.position = "engineer"
    user2.speciality = "research engineer"
    user2.address = "module_2"
    user2.email = "kay_holly@mars.ru"
    db_sess.add(user2)

    user3 = User()
    user3.name = "Maurice"
    user3.surname = "Bay"
    user3.age = 27
    user3.position = "deputy captain"
    user3.speciality = "doctor"
    user3.address = "module_1"
    user3.email = "maurice_chief2@mars.org"
    db_sess.add(user3)

    jobs = Jobs()
    jobs.team_leader = 1
    jobs.job = "deployment of residential modules 1 and 2"
    jobs.work_size = 15
    jobs.collaborators = "2, 3"
    # jobs.start_date = datetime.datetime.now
    jobs.is_finished = False
    db_sess.add(jobs)

    db_sess.commit()


if __name__ == '__main__':
    main()
