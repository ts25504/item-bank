from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from app.main import main


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
