from flask import render_template, redirect, url_for
from flask.ext.login import login_required
from app.main.forms import PointForm, DeleteForm
from app import db
from app.main import main
from app.model.point_model import Points
from app.model.subject_model import Subject
from app.model.single_choice_model import SingleChoice
from app.model.blank_fill_model import BlankFill
from app.model.essay_model import Essay


@main.route('/edit_point/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_point(id):
    point = Points.query.get_or_404(id)
    form = PointForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        point.name = form.name.data
        point.subject = form.subject.data
        s = Subject.query.filter_by(id=point.subject).first()
        point.subject_name = s.name
        sc = SingleChoice.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(sc)):
            if sc[i].subject == point.subject:
                sc[i].knowledge_points_name = point.name
            else:
                sc[i].knowledge_points = 0
                sc[i].knowledge_points_name = ""
            db.session.add(sc[i])
        bf = BlankFill.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(bf)):
            if bf[i].subject == point.subject:
                bf[i].knowledge_points_name = point.name
            else:
                bf[i].knowledge_points = 0
                bf[i].knowledge_points_name = ""
            db.session.add(bf[i])
        es = Essay.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(es)):
            if es[i].subject == point.subject:
                es[i].knowledge_points_name = point.name
            else:
                es[i].knowledge_points = 0
                es[i].knowledge_points_name = ""
            db.session.add(es[i])
        db.session.add(point)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=point.subject))

    form.name.data = point.name
    form.subject.data = point.subject
    return render_template('manage/edit_point.html', form=form)


@main.route('/delete_point/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_point(id):
    point = Points.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        sc = SingleChoice.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(sc)):
            sc[i].knowledge_points = 0
            sc[i].knowledge_points_name = ""
            db.session.add(sc[i])
        bf = BlankFill.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(bf)):
            bf[i].knowledge_points = 0
            bf[i].knowledge_points_name = ""
            db.session.add(bf[i])
        es = Essay.query.filter_by(knowledge_points=point.id).all()
        for i in range(len(es)):
            es[i].knowledge_points = 0
            es[i].knowledge_points_name = ""
            db.session.add(es[i])
        db.session.delete(point)
        db.session.commit()
        return redirect(url_for('main.manage', subject_id=point.subject))
    return render_template('manage/delete_point.html', form=form)
