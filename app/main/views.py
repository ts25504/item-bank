import os
import re
import json
import random
import urllib
import datetime

from flask import render_template, redirect, url_for, request, current_app, \
        make_response
from flask.ext.login import login_required, current_user
from . import main
from ..models import SingleChoice, BlankFill, Essay
from forms import SingleChoiceForm, BlankFillForm, EssayForm, DeleteForm, \
        TestPaperConstraintForm
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
                faq=form.faq.data, A=form.A.data,
                B=form.B.data, C=form.C.data, D=form.D.data,
                answer=form.answer.data)
        db.session.add(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    page = request.args.get('page', 1, type=int)
    pagination = SingleChoice.query.order_by(
            SingleChoice.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    single_choice = pagination.items
    return render_template('single_choice.html', form=form,
            single_choice=single_choice, pagination=pagination)

@main.route('/edit_single_choice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    form = SingleChoiceForm()
    if form.validate_on_submit():
        single_choice.question = form.question.data
        single_choice.difficult_level = form.difficult_level.data
        single_choice.faq = form.faq.data
        single_choice.A = form.A.data
        single_choice.B = form.B.data
        single_choice.C = form.C.data
        single_choice.D = form.D.data
        single_choice.answer = form.answer.data
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
    form.answer.data = single_choice.answer
    return render_template('edit_single_choice.html', form=form)

@main.route('/delete_single_choice/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_single_choice(id):
    single_choice = SingleChoice.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(single_choice)
        db.session.commit()
        return redirect(url_for('main.single_choice'))
    return render_template('delete_single_choice.html', form=form)

@main.route('/blank_fill', methods=['GET', 'POST'])
@login_required
def blank_fill():
    form = BlankFillForm()
    if form.validate_on_submit():
        blank_fill = BlankFill(question=form.question.data,
                difficult_level=form.difficult_level.data,
                faq=form.faq.data,
                answer=form.answer.data)
        db.session.add(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))
    page = request.args.get('page', 1, type=int)
    pagination = BlankFill.query.order_by(
            BlankFill.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    blank_fill = pagination.items
    return render_template('blank_fill.html', form=form,
            blank_fill=blank_fill, pagination=pagination)

@main.route('/edit_blank_fill/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blank_fill(id):
    blank_fill = BlankFill.query.get_or_404(id)
    form = BlankFillForm()
    if form.validate_on_submit():
        blank_fill.question = form.question.data
        blank_fill.difficult_level = form.difficult_level.data
        blank_fill.faq = form.faq.data
        blank_fill.answer = form.answer.data
        db.session.add(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))
    form.question.data = blank_fill.question
    form.difficult_level.data = blank_fill.difficult_level
    form.faq.data = blank_fill.faq
    form.answer.data = blank_fill.answer
    return render_template('edit_blank_fill.html', form=form)

@main.route('/delete_blank_fill/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blank_fill(id):
    blank_fill = BlankFill.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(blank_fill)
        db.session.commit()
        return redirect(url_for('main.blank_fill'))
    return render_template('delete_blank_fill.html', form=form)

@main.route('/essay', methods=['GET', 'POST'])
@login_required
def essay():
    form = EssayForm()
    if form.validate_on_submit():
        essay = Essay(question=form.question.data,
                difficult_level=form.difficult_level.data,
                faq=form.faq.data,
                answer=form.answer.data)
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
    if form.validate_on_submit():
        essay.question = form.question.data
        essay.difficult_level = form.difficult_level.data
        essay.faq = form.faq.data
        essay.answer = form.answer.data
        db.session.add(essay)
        db.session.commit()
        return redirect(url_for('main.essay'))
    form.question.data = essay.question
    form.difficult_level.data = essay.difficult_level
    form.faq.data = essay.faq
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

@main.route('/about')
@login_required
def about():
    return render_template('about.html')

@main.route('/generate_test_paper', methods=['GET', 'POST'])
@login_required
def generate_test_paper():
    single_choice = []
    blank_fill = []
    essay = []
    form = TestPaperConstraintForm()
    if form.validate_on_submit():
        single_choice_number = form.single_choice_number.data
        blank_fill_number = form.blank_fill_number.data
        essay_number = form.essay_number.data
        single_choice = SingleChoice.query.limit(single_choice_number).all()
        blank_fill = BlankFill.query.limit(blank_fill_number).all()
        essay = Essay.query.limit(essay_number).all()
        return render_template('new_test_paper.html',
                single_choice=single_choice,
                blank_fill=blank_fill,
                essay=essay)
    return render_template('generate_test_paper.html', form=form)

def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
