# *- coding: utf-8 -*

from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, \
        SelectField
from wtforms.validators import Required, Length
from ..models import SingleChoice, BlankFill, Essay

class SingleChoiceForm(Form):
    question = TextAreaField(u'新试题', validators=[Required()])
    A = StringField('A', validators=[Required(), Length(1, 255)])
    B = StringField('B', validators=[Required(), Length(1, 255)])
    C = StringField('C', validators=[Required(), Length(1, 255)])
    D = StringField('D', validators=[Required(), Length(1, 255)])
    difficult_level = SelectField(u'难度',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')], default='C')
    faq = TextAreaField(u'解析')
    answer = SelectField(u'答案', choices=[('A', 'A'), ('B', 'B'),
        ('C', 'C'), ('D', 'D')], validators=[Required()])
    submit = SubmitField(u'提交')

class BlankFillForm(Form):
    question = TextAreaField(u'新试题', validators=[Required()])
    difficult_level = SelectField(u'难度',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')], default='C')
    faq = TextAreaField(u'解析')
    answer = StringField(u'答案', validators=[Required(), Length(1, 255)])
    submit = SubmitField(u'提交')

class EssayForm(Form):
    question = TextAreaField(u'新试题', validators=[Required()])
    difficult_level = SelectField(u'难度',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')], default='C')
    faq = TextAreaField(u'解析')
    answer = TextAreaField(u'答案', validators=[Required()])
    submit = SubmitField(u'提交')

class DeleteForm(Form):
    submit = SubmitField(u'确定')

class TestPaperConstraintForm(Form):
    single_choice_number = IntegerField(u'单选题数量',
            validators=[Required()])
    blank_fill_number = IntegerField(u'填空题数量',
            validators=[Required()])
    essay_number = IntegerField(u'问答题数量', validators=[Required()])
    submit = SubmitField(u'提交')
