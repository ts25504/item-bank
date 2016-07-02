# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, \
        flash
from flask.ext.login import login_required
from app.main.forms import SingleChoiceForm, DeleteForm
from app import db
from app.main import main
from app.model.single_choice_model import SingleChoice
from app.model.point_model import Points
from app.model.subject_model import Subject


@main.route('/single_choice', methods=['GET', 'POST'])
@login_required
def single_choice():
    form = SingleChoiceForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.single_choice'))
        if form.A.data[:3] == "<p>":
            form.A.data = form.A.data[3:-6]
        if form.B.data[:3] == "<p>":
            form.B.data = form.B.data[3:-6]
        if form.C.data[:3] == "<p>":
            form.C.data = form.C.data[3:-6]
        if form.D.data[:3] == "<p>":
            form.D.data = form.D.data[3:-6]

        single_choice = SingleChoice(
            question=form.question.data,
            difficult_level=form.difficult_level.data,
            faq=form.faq.data,
            A=form.A.data,
            B=form.B.data,
            C=form.C.data,
            D=form.D.data,
            knowledge_points=form.knowledge_points.data,
            subject=form.subject.data,
            answer=form.answer.data)

        p = Points.query.filter_by(id=single_choice.knowledge_points).first()
        single_choice.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=single_choice.subject).first()
        single_choice.subject_name = s.name

        db.session.add(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    page = request.args.get('page', 1, type=int)
    pagination = SingleChoice.query.order_by(
            SingleChoice.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    single_choice = pagination.items
    return render_template('single_choice/single_choice.html', form=form,
                           single_choice=single_choice, pagination=pagination)


@main.route('/edit_single_choice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    form = SingleChoiceForm()
    form.knowledge_points.choices = [
        (p.id, p.name) for p in Points.query.all()]
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        p = Points.query.filter_by(id=form.knowledge_points.data).first()
        if p.subject != form.subject.data:
            flash(u'知识点与课程不符')
            return redirect(url_for('main.single_choice'))
        if form.A.data[:3] == "<p>":
            form.A.data = form.A.data[3:-6]
        if form.B.data[:3] == "<p>":
            form.B.data = form.B.data[3:-6]
        if form.C.data[:3] == "<p>":
            form.C.data = form.C.data[3:-6]
        if form.D.data[:3] == "<p>":
            form.D.data = form.D.data[3:-6]
        single_choice.question = form.question.data
        single_choice.difficult_level = form.difficult_level.data
        single_choice.faq = form.faq.data
        single_choice.A = form.A.data
        single_choice.B = form.B.data
        single_choice.C = form.C.data
        single_choice.D = form.D.data
        single_choice.knowledge_points = form.knowledge_points.data
        single_choice.subject = form.subject.data,
        single_choice.answer = form.answer.data
        p = Points.query.filter_by(id=single_choice.knowledge_points).first()
        single_choice.knowledge_points_name = p.name
        s = Subject.query.filter_by(id=single_choice.subject).first()
        single_choice.subject_name = s.name

        db.session.add(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))

    form.question.data = single_choice.question
    form.difficult_level.data = single_choice.difficult_level
    form.faq.data = single_choice.faq
    form.A.data = single_choice.A
    form.B.data = single_choice.B
    form.C.data = single_choice.C
    form.D.data = single_choice.D
    form.knowledge_points.data = single_choice.knowledge_points
    form.subject.data = single_choice.subject
    form.answer.data = single_choice.answer
    return render_template('single_choice/edit_single_choice.html', form=form)


@main.route('/delete_single_choice/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    return render_template('single_choice/delete_single_choice.html',
                           form=form)
