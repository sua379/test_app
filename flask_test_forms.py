# -*- coding: utf-8 -*-
from wtforms import StringField,SubmitField, IntegerField,EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_ckeditor import CKEditorField

#Defining a form that collects user information during sign up
class UserForm(FlaskForm):
    name=StringField('Name?', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired()])
    about_author=TextAreaField('About Author')
    age=IntegerField('Age', validators=[DataRequired()])
    email=EmailField('Email', validators=[DataRequired()])
    passion=StringField('Passion', validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(), EqualTo('password2','Passwords must be a match')])
    password2=PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic=FileField('Profile Picture')
    submit=SubmitField('Submit')
    
#Defining the login form to be used in on the webpage
class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Login')
#defining the form that will collect the information to be searched 
class SearchForm(FlaskForm):
    searched=StringField('searched',validators=[DataRequired()])
    submit=SubmitField('Login')
#a class that defines the web form and contains the information to be collected 
class NamerForm(FlaskForm):
    name=StringField('What is your name?', validators=[DataRequired()])
    email=EmailField('Email', validators=[DataRequired()])
    age=IntegerField('How old are you?', validators=[DataRequired()])
    passion=StringField('what interests you?')
    username=StringField('Username', validators=[DataRequired()])
    about_author=TextAreaField('About Author')
    profile_pic=FileField('Profile Picture')
    submit=SubmitField('Submit')

#define a form that collects the blog information from the users.
class BlogForm(FlaskForm):
    title=StringField('Blog Title', validators=[DataRequired()])
    #author=StringField('Author', validators=[DataRequired()])
    slug=StringField('Slug', validators=[DataRequired()])
    content = CKEditorField('Content',validators=[DataRequired()])
    submit=SubmitField('Publish') 
    
