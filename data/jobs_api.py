import flask
from flask import jsonify

from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'user.name', 'user.surname'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        return jsonify(
            {
                'jobs':
                    job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'user.name', 'user.surname'))
            }
        )
    return jsonify({'error': 'Not found'})
