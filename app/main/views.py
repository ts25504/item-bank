from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from . import main
from ..models import SingleChoice
from forms import SingleChoiceForm
from .. import db

@main.route('/')
def index_or_login():
    if current_user.is_authenticated():
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('auth.login'))

@main.route('/index')
@login_required
def index():
    return render_template('index.html')

@main.route('/single_choice', methods=['GET', 'POST'])
@login_required
def single_choice():
    form = SingleChoiceForm()
    if form.validate_on_submit():
        single_choice = SingleChoice(question=form.question.data,
                difficult_level=form.difficult_level.data,
                faq=form.faq.data, score=form.score.data, A=form.A.data,
                B=form.B.data, C=form.C.data, D=form.D.data,
                answer=form.answer.data)
        db.session.add(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    single_choice = SingleChoice.query.order_by(
            SingleChoice.add_date.desc()).all()
    return render_template('single_choice.html', form=form,
            single_choice=single_choice)

@main.route('/edit_single_choice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    form = SingleChoiceForm()
    if form.validate_on_submit():
        single_choice.question = form.question.data
        single_choice.difficult_level = form.difficult_level.data
        single_choice.faq = form.faq.data
        single_choice.score = form.score.data
        single_choice.A = form.A.data
        single_choice.B = form.B.data
        single_choice.C = form.C.data
        single_choice.D = form.D.data
        db.session.add(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    form.question.data = single_choice.question
    form.difficult_level.data = single_choice.difficult_level
    form.faq.data = single_choice.faq
    form.score.data = single_choice.score
    form.A.data = single_choice.A
    form.B.data = single_choice.B
    form.C.data = single_choice.C
    form.D.data = single_choice.D
    return render_template('edit_single_choice.html', form=form)
