from flask_wtf import Form
from wtforms.validators import Required, Length
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
 
from flask_wysiwyg.wysiwyg import *

class EditForm(Form):
	title=StringField('Title',validators=[Required(), Length(1, 64)])
	body=WysiwygField("txteditor")
	submit=SubmitField("Submit")