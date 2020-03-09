from flask_wtf import Form
from wtforms.validators import Required, Length, Email
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
 
from flask_wysiwyg.wysiwyg import *

class EditForm(Form):
	title=StringField('Title',validators=[Required(), Length(1, 64)])
	body=WysiwygField("txteditor")
	submit=SubmitField("Submit")


class LoginForm(Form):
    email = StringField('Email',  validators=[Required(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password', validators=[Required(), Length(min=4, max=25)])
    submit = SubmitField('Submit')
