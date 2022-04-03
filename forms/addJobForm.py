from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = StringField('Организатор', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = StringField('Часы работы', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    start_date = StringField('Дата начала')
    submit = SubmitField('Добавить')
