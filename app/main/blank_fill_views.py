# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, \
        flash
from flask.ext.login import login_required
from app.main.forms import BlankFillForm, DeleteForm
from app import db
from app.main import main
from app.model.blank_fill_model import BlankFill
from app.model.point_model import Points
from app.model.subject_model import Subject


@main.route('/blank_fill', methods=['GET', 'POST'])
@login_required
def blank_fill():
    form = BlankFillForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.blank_fill'))

        blank_fill = BlankFill(
            question=form.question.data,
            difficult_level=form.difficult_level.data,
            faq=form.faq.data,
            knowledge_points=form.knowledge_points.data,
            subject=form.subject.data,
            answer=form.answer.data)

        p = Points.query.filter_by(id=blank_fill.knowledge_points).first()
        blank_fill.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=blank_fill.subject).first()
        blank_fill.subject_name = s.name

        db.session.add(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))
    page = request.args.get('page', 1, type=int)
    pagination = BlankFill.query.order_by(
            BlankFill.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    blank_fill = pagination.items
    return render_template('blank_fill/blank_fill.html', form=form,
                           blank_fill=blank_fill, pagination=pagination)


@main.route('/edit_blank_fill/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blank_fill(id):
    blank_fill = BlankFill.query.get_or_404(id)
    form = BlankFillForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.blank_fill'))
        blank_fill.question = form.question.data
        blank_fill.difficult_level = form.difficult_level.data
        blank_fill.faq = form.faq.data
        blank_fill.knowledge_points = form.knowledge_points.data
        blank_fill.subject = form.subject.data
        blank_fill.answer = form.answer.data

        p = Points.query.filter_by(id=blank_fill.knowledge_points).first()
        blank_fill.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=blank_fill.subject).first()
        blank_fill.subject_name = s.name

        db.session.add(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))

    form.question.data = blank_fill.question
    form.difficult_level.data = blank_fill.difficult_level
    form.faq.data = blank_fill.faq
    form.knowledge_points.data = blank_fill.knowledge_points
    form.subject.data = blank_fill.subject
    form.answer.data = blank_fill.answer
    return render_template('blank_fill/edit_blank_fill.html', form=form)


@main.route('/delete_blank_fill/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blank_fill(id):
    blank_fill = BlankFill.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))
    return render_template('blank_fill/delete_blank_fill.html', form=form)
