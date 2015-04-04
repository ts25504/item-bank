from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, \
        SelectField
from wtforms.validators import Required, Length
from ..models import SingleChoice

class SingleChoiceForm(Form):
    question = TextAreaField('Question', validators=[Required()])
    A = StringField('A', validators=[Required(), Length(1, 64)])
    B = StringField('B', validators=[Required(), Length(1, 64)])
    C = StringField('C', validators=[Required(), Length(1, 64)])
    D = StringField('D', validators=[Required(), Length(1, 64)])
    score = IntegerField('score', validators=[Required()])
    difficult_level = SelectField('difficult_level',
            choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
                ('E', 'E')])
    faq = TextAreaField('faq')
    answer = SelectField('answer', choices=[('A', 'A'), ('B', 'B'),
        ('C', 'C'), ('D', 'D')], validators=[Required()])
    submit = SubmitField('Submit')
