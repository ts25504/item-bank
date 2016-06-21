# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, current_app, \
        flash
from flask.ext.login import login_required
from app.main.forms import DeleteForm, TestPaperConstraintForm, \
        TestPaperReplaceForm, TestPaperNameForm
from app import db
from app.main import main
from app.model.single_choice_model import SingleChoice
from app.model.blank_fill_model import BlankFill
from app.model.essay_model import Essay
from app.model.point_model import Points
from app.model.subject_model import Subject
from app.model.test_paper_model import TestPaper

from genetic_algorithm.db import DB
from genetic_algorithm.paper import Paper
from genetic_algorithm.problem import Problem
from genetic_algorithm.main import Genetic


def handle_str(problems):
    problems = problems[1:]
    problems = problems[:-1]
    ids = problems.split(', ')
    for i in range(len(ids)):
        ids[i] = long(ids[i])
    return ids


@main.route('/test_papers')
@login_required
def test_papers():
    page = request.args.get('page', 1, type=int)
    pagination = TestPaper.query.order_by(
            TestPaper.timestamp.desc()).paginate(
            page, per_page=current_app.config['QUESTIONS_PER_PAGE'],
            error_out=False)
    test_papers = pagination.items
    return render_template('test_papers.html',
                           test_papers=test_papers, pagination=pagination)


@main.route('/test_paper/<int:id>')
@login_required
def test_paper(id):
    test_paper = TestPaper.query.get_or_404(id)
    sc = handle_str(test_paper.single_choice)
    bf = handle_str(test_paper.blank_fill)
    es = handle_str(test_paper.essay)
    name = test_paper.name
    single_choice = []
    blank_fill = []
    essay = []
    for sc_id in sc:
        item = SingleChoice.query.filter_by(id=sc_id).first()
        single_choice.append(item)
    for bf_id in bf:
        item = BlankFill.query.filter_by(id=bf_id).first()
        blank_fill.append(item)
    for es_id in es:
        item = Essay.query.filter_by(id=es_id).first()
        essay.append(item)

    return render_template('test_paper.html',
                           tp_id=test_paper.id,
                           name=name,
                           single_choice=single_choice,
                           blank_fill=blank_fill,
                           essay=essay)


@main.route('/edit_test_paper_name/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_test_paper_name(id):
    form = TestPaperNameForm()
    if form.validate_on_submit():
        test_paper = TestPaper.query.filter_by(id=id).first()
        test_paper.name = form.name.data
        db.session.add(test_paper)
        db.session.commit()
        return redirect(url_for('main.test_paper', id=id))
    return render_template('edit_test_paper.html', form=form)


@main.route('/edit_test_paper_sc/<int:tp_id>.<int:id>',
            methods=['GET', 'POST'])
@login_required
def edit_test_paper_sc(tp_id, id):
    form = TestPaperReplaceForm()
    if form.validate_on_submit():
        new_id = form.new_id.data
        test_paper = TestPaper.query.filter_by(id=tp_id).first()
        p = handle_str(test_paper.single_choice)
        for i in range(len(p)):
            if p[i] == new_id:
                flash(u'试题重复')
                return redirect(url_for('main.test_paper', id=tp_id))

        for i in range(len(p)):
            if p[i] == id:
                p[i] = new_id
        p_str = u'['
        p_str += u', '.join(unicode(e) for e in p)
        p_str += u']'
        test_paper.single_choice = p_str
        db.session.add(test_paper)
        db.session.commit()
        return redirect(url_for('main.test_paper', id=tp_id))
    return render_template('edit_test_paper.html', form=form)


@main.route('/edit_test_paper_bf/<int:tp_id>.<int:id>',
            methods=['GET', 'POST'])
@login_required
def edit_test_paper_bf(tp_id, id):
    form = TestPaperReplaceForm()
    if form.validate_on_submit():
        new_id = form.new_id.data
        test_paper = TestPaper.query.filter_by(id=tp_id).first()
        p = handle_str(test_paper.blank_fill)
        for i in range(len(p)):
            if p[i] == id:
                p[i] = new_id
        p_str = u'['
        p_str += u', '.join(unicode(e) for e in p)
        p_str += u']'
        test_paper.blank_fill = p_str
        db.session.add(test_paper)
        db.session.commit()
        return redirect(url_for('main.test_paper', id=tp_id))
    return render_template('edit_test_paper.html', form=form)


@main.route('/edit_test_paper_es/<int:tp_id>.<int:id>',
            methods=['GET', 'POST'])
@login_required
def edit_test_paper_es(tp_id, id):
    form = TestPaperReplaceForm()
    if form.validate_on_submit():
        new_id = form.new_id.data
        test_paper = TestPaper.query.filter_by(id=tp_id).first()
        p = handle_str(test_paper.essay)
        for i in range(len(p)):
            if p[i] == id:
                p[i] = new_id
        p_str = u'['
        p_str += u', '.join(unicode(e) for e in p)
        p_str += u']'
        test_paper.essay = p_str
        db.session.add(test_paper)
        db.session.commit()
        return redirect(url_for('main.test_paper', id=tp_id))
    return render_template('edit_test_paper.html', form=form)


@main.route('/delete_test_paper/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_test_paper(id):
    test_paper = TestPaper.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(test_paper)
        db.session.commit()
        return redirect(url_for('main.test_papers'))
    return render_template('delete_test_paper.html', form=form)


@main.route(
    '/new_test_paper/<name>.<subject>.<float:difficulty>.<sc>.<bf>.<es>',
    methods=['POST', 'GET'])
@login_required
def new_test_paper(name, subject, difficulty, sc, bf, es):
    sub = Subject.query.filter_by(id=subject).first()
    subject_name = sub.name
    test_paper = TestPaper(name=name, subject=subject,
                           subject_name=subject_name,
                           single_choice=sc, blank_fill=bf, essay=es)
    db.session.add(test_paper)
    db.session.commit()
    return render_template('index.html')


@main.route('/generate_test_paper', methods=['GET', 'POST'])
@login_required
def generate_test_paper():
    single_choice = []
    blank_fill = []
    essay = []
    sc_ids = []
    bf_ids = []
    es_ids = []
    each_point_score = []
    form = TestPaperConstraintForm()
    form.subject.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        name = form.name.data
        subject = form.subject.data
        single_choice_number = form.single_choice_number.data
        single_choice_score = form.single_choice_score.data
        blank_fill_number = form.blank_fill_number.data
        blank_fill_score = form.blank_fill_score.data
        essay_number = form.essay_number.data
        essay_score = form.essay_score.data
        difficulty = form.difficulty.data
        points = form.points.data
        each_point_score = form.each_point_score.data

        paper = Paper()
        paper.id = 1
        paper.difficulty = difficulty
        for p in points:
            pp = Points.query.filter_by(name=p).first()
            paper.points.append(pp.id)
        for eps in each_point_score:
            paper.each_point_score.append(int(eps))

        paper.each_type_count = [single_choice_number,
                                 blank_fill_number, essay_number]
        paper.each_type_score = [single_choice_score,
                                 blank_fill_score, essay_score]
        paper.total_score = single_choice_score + blank_fill_score + \
            essay_score

        single_choice = SingleChoice.query.filter_by(subject=subject).all()
        blank_fill = BlankFill.query.filter_by(subject=subject).all()
        essay = Essay.query.filter_by(subject=subject).all()

        problem_list = []
        for sc in single_choice:
            p = Problem()
            p.id = sc.id
            p.type = 1
            p.difficulty = sc.difficult_level
            p.points.append(sc.knowledge_points)
            p.score = single_choice_score / single_choice_number
            problem_list.append(p)

        for bf in blank_fill:
            p = Problem()
            p.id = bf.id
            p.type = 2
            p.difficulty = bf.difficult_level
            p.points.append(bf.knowledge_points)
            p.score = blank_fill_score / blank_fill_number
            problem_list.append(p)

        for es in essay:
            p = Problem()
            p.id = es.id
            p.type = 3
            p.difficulty = es.difficult_level
            p.points.append(es.knowledge_points)
            p.score = essay_score / essay_number
            problem_list.append(p)

        db = DB()
        db.create_from_problem_list(problem_list)
        genetic = Genetic(paper, db)
        u = genetic.run(0.98)

        single_choice = []
        blank_fill = []
        essay = []
        for p in u.problem_list:
            if p.type == 1:
                sc = SingleChoice.query.filter_by(id=p.id).all()
                single_choice += sc
                for item in sc:
                    sc_ids.append(item.id)
            if p.type == 2:
                bf = BlankFill.query.filter_by(id=p.id).all()
                blank_fill += bf
                for item in bf:
                    bf_ids.append(item.id)
            if p.type == 3:
                es = Essay.query.filter_by(id=p.id).all()
                essay += es
                for item in es:
                    es_ids.append(item.id)

        return render_template('new_test_paper.html',
                               name=name,
                               single_choice=single_choice,
                               blank_fill=blank_fill,
                               essay=essay,
                               sc_ids=sc_ids,
                               bf_ids=bf_ids,
                               es_ids=es_ids,
                               subject=subject,
                               difficulty=difficulty)
    return render_template('generate_test_paper.html', form=form)
