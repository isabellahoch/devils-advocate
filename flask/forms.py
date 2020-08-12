try:
	from flask_wtf import Form, FlaskForm
except:
	from flask_wtf import Form
from wtforms.validators import Required, Length, Email, InputRequired, EqualTo
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
 
# from flask_wysiwyg.wysiwyg import *

# class EditForm(FlaskForm):
# 	title=StringField('Title',validators=[Required(), Length(1, 64)])
# 	body=WysiwygField("txteditor")
# 	submit=SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField('Email',  validators=[Required(), Email(message='Invalid email'), Length(max=30)],render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[Length(min=4, max=25)],render_kw={'class': 'form-control'})
    submit = SubmitField('Submit', render_kw={'class': 'form-control btn btn-custom','style':'width:100%'})

# class RegForm(FlaskForm):
# 	email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control'})
# 	password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25)], render_kw={'class': 'form-control'})
# 	confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=4, max=25), EqualTo('password', message='Passwords must match.')], render_kw={'class': 'form-control'})
# 	submit = SubmitField('Submit', render_kw={'class': 'form-control btn btn-custom','style':'width:100%'})

class SubscribeForm(FlaskForm):
	name=StringField('Name',validators=[Required()], render_kw={'class': 'form-control'})
	email=StringField('Email',validators=[Required(), Email(message='Invalid email')], render_kw={'class': 'form-control'})
	affiliation = SelectField(u'Affiliation', choices=[('student', 'Student'), ('alum', 'Alum'), ('faculty', 'Faculty/Staff'), ('family', 'Parent/Family'), ('prospective_student', 'Prospective Student'), ('other', 'Other/Multiple Affiliations')], render_kw={'class': 'form-control'})
	submit = SubmitField('SUBSCRIBE', render_kw={'class': 'form-control btn btn-custom','style':'width:100%'})