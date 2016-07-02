from flask import render_template, redirect, url_for
from flask.ext.login import login_required
from app.main.forms import PointForm, DeleteForm
from app import db
from app.main import main
from app.model.point_model import Points
from app.model.subject_model import Subject


@main.route('/edit_point/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_point(id):
    point = Points.query.get_or_404(id)
    form = PointForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        point.name = form.name.data
        point.subject_id = form.subject.data

        db.session.add(point)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=point.subject_id))

    form.name.data = point.name
    form.subject.data = point.subject
    return render_template('manage/edit_point.html', form=form)


@main.route('/delete_point/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_point(id):
    point = Points.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(point)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=point.subject_id))
    return render_template('manage/delete_point.html', form=form)
