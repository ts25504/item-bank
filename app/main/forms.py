from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, \
        SelectField
from wtforms.validators import Required, Length
from ..models import SingleChoice, BlankFill, Essay

class SingleChoiceForm(Form):
    question = PageDownField('New Question', validators=[Required()])
    A = StringField('A', validators=[Required(), Length(1, 255)])
    B = StringField('B', validators=[Required(), Length(1, 255)])
    C = StringField('C', validators=[Required(), Length(1, 255)])
    D = StringField('D', validators=[Required(), Length(1, 255)])
    score = IntegerField('score', validators=[Required()])
    difficult_level = SelectField('difficult_level',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')])
    faq = PageDownField('faq')
    answer = SelectField('answer', choices=[('A', 'A'), ('B', 'B'),
        ('C', 'C'), ('D', 'D')], validators=[Required()])
    submit = SubmitField('Submit')

class BlankFillForm(Form):
    question = PageDownField('New Question', validators=[Required()])
    difficult_level = SelectField('difficult_level',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')])
    faq = PageDownField('faq')
    score = IntegerField('score', validators=[Required()])
    answer = StringField('answer', validators=[Required(), Length(1, 255)])
    submit = SubmitField('Submit')

class EssayForm(Form):
    question = PageDownField('New Question', validators=[Required()])
    difficult_level = SelectField('difficult_level',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')])
    faq = PageDownField('faq')
    score = IntegerField('score', validators=[Required()])
    answer = PageDownField('answer', validators=[Required()])
    submit = SubmitField('Submit')

class DeleteForm(Form):
    submit = SubmitField('Yes')
