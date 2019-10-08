from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import Email, Length, InputRequired, EqualTo, Regexp, URL
from wtforms.widgets import TextArea


categories_list = ['Art','Crafts','Design','Fashion','Film & Video','Food','Games','News','Music','Photography','Publishing','Technology','Theater','Other']
categories = [(None, 'All')]
radii_list = ['5', '10', '25', '50', '100']
radii = []
locations = [('San Francisco', 'San Francisco'), ('Sydney', 'Sydney')]

update_btn_value = "update"
update_btn_value = update_btn_value.upper()

for item in categories_list:
    new_item = (item, item)
    categories.append(new_item)

for item in radii_list:
    new_item = (item, item+" miles")
    radii.append(new_item)

class ContactForm(FlaskForm):
  name = StringField("name", render_kw={'class': 'form-control'})
  email = StringField("_replyto", render_kw={'class': 'form-control'})
  subject = StringField("Subject", render_kw={'class': 'form-control'})
  message = TextAreaField("Message", render_kw={'class': 'form-control'})
  submit = SubmitField("Send", render_kw={'class': 'btn btn-incub8','style':'width:100%'})

class DonateForm(FlaskForm):
  amount = StringField("amount", validators=[InputRequired()], render_kw={'class': 'form-control', 'id':'donation_amount'})
  email = StringField("email_address", validators=[InputRequired(), Email(message='Invalid email')], render_kw={'class': 'form-control'})
  message = TextAreaField("Message", render_kw={'class': 'form-control'})

class FilterForm(FlaskForm):
    category = SelectField('Class', render_kw={'class': 'form-control', 'onchange':'get_category()', 'id':'category'}, choices=categories)
    query = StringField('Search', render_kw={'class':'form-control', 'id':'search-members'})
    location = StringField('Location', render_kw={'class': 'form-control', 'id':'location-address', 'onchange':'get_location'})
    radius = SelectField('Radius', render_kw={'class': 'form-control', 'id':'location-radius'}, choices = radii)
    go = SubmitField('GO', render_kw={'class':'btn btn-incub8 go-button','style':'min-width: fit-content; margin-top:20px'})

class AccountForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25)], render_kw={'class': 'form-control'})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')], render_kw={'class': 'form-control'})
    name = StringField('Full Name (First Last)',  validators=[InputRequired()], render_kw={'class': 'form-control'})
    bio = StringField('Bio',  validators=[InputRequired(), Length(max=500)], render_kw={'class': 'form-control', 'style':'height:250px'}, widget=TextArea())
    mentor_goal = BooleanField('Mentor', render_kw={'class':'form-control'})
    funding_goal = BooleanField('Funding', render_kw={'class':'form-control'})
    awareness_goal = BooleanField('Awareness', render_kw={'class':'form-control'})
    location = StringField('Location', render_kw={'class': 'form-control', 'placeholder':'e.g. San Francisco, CA','id':'startup-location'})
    image = StringField('Image', render_kw={'class': 'form-control', 'id':'form-image'})
    facebook = StringField('Facebook', render_kw={'class':'form-control social-input', 'id':'facebook-link', 'placeholder':'e.g. https://www.facebook.com/incub8sf'})
    instagram = StringField('Instagram', render_kw={'class':'form-control social-input', 'id':'instagram-link', 'placeholder':'e.g. https://www.instagram.com/incub8sf/'})
    twitter = StringField('Twitter', render_kw={'class':'form-control social-input', 'id':'twitter-link', 'placeholder':'e.g. https://twitter.com/incub8sf'})
    pinterest = StringField('Pinterest', render_kw={'class':'form-control social-input', 'id':'pinterest-link', 'placeholder':'e.g. https://www.pinterest.com/incub8sf/'})
    website = StringField('Website', render_kw={'class':'form-control social-input', 'id':'website-link', 'placeholder':'e.g. https://www.incub8.herokuapp.com/'})
    update = SubmitField(update_btn_value, render_kw = {'class':'btn-black-border update'})
    submit = SubmitField('Save Changes', render_kw={'class': 'form-control btn btn-incub8'})

class InvestorAccountForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=25)], render_kw={'class': 'form-control'})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')], render_kw={'class': 'form-control'})
    name = StringField('Full Name (First Last)',  validators=[InputRequired()], render_kw={'class': 'form-control'})
    bio = StringField('Bio',  validators=[InputRequired(), Length(max=500)], render_kw={'class': 'form-control', 'style':'height:250px'}, widget=TextArea())
    image = StringField('Image', render_kw={'class': 'form-control', 'id':'form-image'})
    update = SubmitField(update_btn_value, render_kw = {'class':'btn-black-border update'})
    submit = SubmitField('Save Changes', render_kw={'class': 'form-control btn btn-incub8'})

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)], render_kw={'class': 'form-control', 'id':'comment_name', 'placeholder':'Your Name'})
    email = StringField('Email', validators=[Email(message='Invalid email'), Length(max=50)], render_kw={'class': 'form-control', 'id': 'comment_email', 'placeholder':'Email'})
    text = StringField('Comment', validators=[InputRequired(), Length(max=1000)], render_kw={'class': 'form-control', 'id':'comment_text', 'placeholder':'Comment'}, widget=TextArea())
    submit = SubmitField('Post Comment', render_kw={'class': 'btn btn-outline-secondary', 'id':'comment_submit'})


class AddAdminForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email')], render_kw={'class': 'form-control','id':'add_admin','placeholder':'User Email'})
    submit = SubmitField(update_btn_value, render_kw={'class': 'btn-black-border update','id':'add-admin-btn','style':'width: 300px; margin-top: 15px;'})

class RemoveAdminForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control','id':'remove_admin','placeholder':'User Email'})
    submit = SubmitField(update_btn_value, render_kw={'class': 'btn-black-border update','id':'add-admin-btn','style':'width: 300px; margin-top: 15px;'})

class DeleteUserForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)], render_kw={'class': 'form-control','id':'delete_user','placeholder':'User Email'})
    submit = SubmitField(update_btn_value, render_kw={'class': 'btn-black-border update','id':'delete-user-btn','style':'width: 300px; margin-top: 15px;'})
