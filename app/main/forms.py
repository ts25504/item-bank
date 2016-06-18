# *- coding: utf-8 -*

import re
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import widgets
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, \
        SelectField, FloatField, Field
from wtforms.validators import Required, Length, NumberRange
from app.models import SingleChoice, BlankFill, Essay, Points

class SingleChoiceForm(Form):
    subject = SelectField(u'科目', coerce=int)
    question = TextAreaField(u'新试题', validators=[Required()])
    A = TextAreaField('A', validators=[Required(), Length(1, 255)])
    B = TextAreaField('B', validators=[Required(), Length(1, 255)])
    C = TextAreaField('C', validators=[Required(), Length(1, 255)])
    D = TextAreaField('D', validators=[Required(), Length(1, 255)])
    knowledge_points = SelectField(u'知识点', coerce=int)
    difficult_level = FloatField(u'难度', validators=[Required(),
        NumberRange(min=0, max=1)])
    faq = TextAreaField(u'解析')
    answer = SelectField(u'答案', choices=[('A', 'A'), ('B', 'B'),
        ('C', 'C'), ('D', 'D')], validators=[Required()])
    submit = SubmitField(u'提交')

class BlankFillForm(Form):
    subject = SelectField(u'科目', coerce=int)
    question = TextAreaField(u'新试题', validators=[Required()])
    knowledge_points = SelectField(u'知识点', coerce=int)
    difficult_level = FloatField(u'难度', validators=[Required(),
        NumberRange(min=0, max=1)])
    faq = TextAreaField(u'解析')
    answer = StringField(u'答案', validators=[Required(), Length(1, 255)])
    submit = SubmitField(u'提交')

class EssayForm(Form):
    subject = SelectField(u'科目', coerce=int)
    question = TextAreaField(u'新试题', validators=[Required()])
    knowledge_points = SelectField(u'知识点', coerce=int)
    difficult_level = FloatField(u'难度', validators=[Required(),
        NumberRange(min=0, max=1)])
    faq = TextAreaField(u'解析')
    answer = TextAreaField(u'答案', validators=[Required()])
    submit = SubmitField(u'提交')

class DeleteForm(Form):
    submit = SubmitField(u'确定')

class TagListField(Field):
    widget = widgets.TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in re.split(u'[,，]', valuelist[0])]
        else:
            self.data = []

class TestPaperConstraintForm(Form):
    name = StringField(u'试卷名称')
    subject = SelectField(u'科目', coerce=int)
    single_choice_number = IntegerField(u'单选题数量',
            validators=[Required()])
    single_choice_score = IntegerField(u'单选题分数',
            validators=[Required()])
    blank_fill_number = IntegerField(u'填空题数量',
            validators=[Required()])
    blank_fill_score = IntegerField(u'填空题分数',
            validators=[Required()])
    essay_number = IntegerField(u'问答题数量', validators=[Required()])
    essay_score = IntegerField(u'问答题分数', validators=[Required()])
    difficulty = FloatField(u'难度', validators=[Required()])
    points = TagListField(u'知识点', validators=[Required()])
    each_point_score = TagListField(u'各知识点分数', validators=[Required()])
    submit = SubmitField(u'提交')

class PointForm(Form):
    name = StringField(u'知识点',
            validators=[Required(), Length(1, 127)])
    subject = SelectField(u'科目', coerce=int)
    submit = SubmitField(u'提交')

class SubjectForm(Form):
    name = StringField(u'课程名', validators=[Required(), Length(1, 127)])
    submit = SubmitField(u'提交')

class TestPaperReplaceForm(Form):
    new_id = IntegerField(u'题号', validators=[Required()])
    submit = SubmitField(u'提交')

class TestPaperNameForm(Form):
    name = StringField(u'新名称', validators=[Required(), Length(1, 255)])
    submit = SubmitField(u'提交')
