# *- coding: utf-8 -*

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length

class LoginForm(Form):
    username = StringField(u'账号', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')
