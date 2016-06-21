# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, \
        flash
from flask.ext.login import login_required
from app.main.forms import EssayForm, DeleteForm
from app import db
from app.main import main
from app.model.essay_model import Essay
from app.model.point_model import Points
from app.model.subject_model import Subject


@main.route('/essay', methods=['GET', 'POST'])
@login_required
def essay():
    form = EssayForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.essay'))

        essay = Essay(
            question=form.question.data,
            difficult_level=form.difficult_level.data,
            faq=form.faq.data,
            knowledge_points=form.knowledge_points.data,
            subject=form.subject.data,
            answer=form.answer.data)

        p = Points.query.filter_by(id=essay.knowledge_points).first()
        essay.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=essay.subject).first()
        essay.subject_name = s.name

        db.session.add(essay)
        db.session.commit()
        return redirect(url_for('main.essay'))
    page = request.args.get('page', 1, type=int)
    pagination = Essay.query.order_by(
            Essay.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    essay = pagination.items
    return render_template('essay.html', form=form,
                           essay=essay, pagination=pagination)


@main.route('/edit_essay/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_essay(id):
    essay = Essay.query.get_or_404(id)
    form = EssayForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.essay'))
        essay.question = form.question.data
        essay.difficult_level = form.difficult_level.data
        essay.faq = form.faq.data
        essay.knowledge_points = form.knowledge_points.data
        essay.subject = form.subject.data
        essay.answer = form.answer.data

        p = Points.query.filter_by(id=essay.knowledge_points).first()
        essay.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=essay.subject).first()
        essay.subject_name = s.name

        db.session.add(essay)
        db.session.commit()
        return redirect(url_for('main.essay'))

    form.question.data = essay.question
    form.difficult_level.data = essay.difficult_level
    form.faq.data = essay.faq
    form.knowledge_points.data = essay.knowledge_points
    form.subject.data = essay.subject
    form.answer.data = essay.answer
    return render_template('edit_essay.html', form=form)


@main.route('/delete_essay/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_essay(id):
    essay = Essay.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(essay)
        db.session.commit()
        return redirect(url_for('main.essay'))
    return render_template('delete_essay.html', form=form)
