from flask import render_template, redirect, url_for
from flask.ext.login import login_required
from app.main.forms import SubjectForm, PointForm, DeleteForm
from app import db
from app.main import main
from app.model.subject_model import Subject
from app.model.point_model import Points


@main.route('/manage/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def manage(subject_id):
    subject = Subject.query.all()
    if subject_id == 0:
        Points_query = Points.query
    else:
        Points_query = Points.query.filter_by(subject=subject_id)

    points = Points_query.all()

    point_form = PointForm()
    subject_form = SubjectForm()
    point_form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if point_form.validate_on_submit():
        s = Subject.query.filter_by(id=point_form.subject.data).first()
        point = Points(name=point_form.name.data,
                       subject=point_form.subject.data, subject_name=s.name)
        db.session.add(point)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=point.subject))

    if subject_form.validate_on_submit():
        subject = Subject(name=subject_form.name.data)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=0))

    return render_template('manage.html', points=points, subject=subject,
                           point_form=point_form, subject_form=subject_form)


@main.route('/delete_subject/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=0))
    return render_template('delete_subject.html', form=form)
