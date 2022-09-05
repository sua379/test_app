# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 22:06:13 2022

@author: sua
"""

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_test_forms import UserForm, LoginForm, NamerForm, BlogForm, SearchForm, ProjectForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import os
import uuid



#just testing


app=Flask(__name__)
#Initializing the CKEditor with the flask app
ckeditor = CKEditor(app)
#conect the data base to be used on the script'
#Old SQLight database
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.database'
#New MYSQL database...for production purpose.
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://jgjvusceixdcud:34118260ddd50899f27a7eea8d236b8c5e1dfcf14c2de705f567618ee5d33a70@ec2-44-195-100-240.compute-1.amazonaws.com:5432/de2m36p9ko3677'
#create a secret key that protects all forms
app.config['SECRET_KEY']='the secret key that i am using for this test app'
UPLOAD_FOLDER='static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

db=SQLAlchemy(app)
migrate=Migrate(app, db)

#integrating the flask login interface with our application
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


#define the function that handles the admin page
@app.route('/admin')
@login_required
def admin():
    id=current_user.id
    users=db_model()
    if id==1:
        users=users.query.order_by(users.id)
        return render_template('admin.html', users=users) 
    else:
        flash('Only the admin can access this page')
        return redirect(url_for('dashboard'))

@login_manager.user_loader
def load_user(user_id):
    return db_model.query.get(int(user_id))

#defining the function that handles the login page
@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=db_model.query.filter_by(username=form.username.data).first()
        #if there is a user that matches the username submitted, proceed to check the password hash and see if it matches 
        if user:
            check=check_password_hash(user.hash_password, form.password.data)
            if check ==True:
                login_user(user)
                flash('Login sucessfully')
                #if the form is filled and submitted, redirect to the dashboard page
                return redirect(url_for('dashboard'))
            else:
                flash('password is not correct!!! 3 more trials for you mf')
        else:
            flash('Username is not correct, are you that dumb?')
        #if the form is filled and submitted, redirect to the dashboard page
        return redirect(url_for('dashboard'))
    return render_template('login.html',form=form)

#defining the fucntion that handles the dashboard page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form=NamerForm()
    #collect an instance of the database using an id that is passed with the url
    name_to_update=db_model.query.get_or_404(current_user.id)
    #if the user submits a new form, update the content of the existing record with the new
    #information
    #if request.method=='POST':
    if form.validate_on_submit():
        name_to_update.name=request.form['name']
        name_to_update.email=request.form['email']
        name_to_update.age=request.form['age']
        name_to_update.passion=request.form['passion']
        name_to_update.username=request.form['username']
        name_to_update.about_author=request.form['about_author']
        name_to_update.profile_pic=request.files['profile_pic']
        #ensure that that uploaded file is very secure
        profile_pic=secure_filename(name_to_update.profile_pic.filename)
        #create a unique name for the uploaded file
        name_to_update.profile_pic=str(uuid.uuid1())+ '_' + profile_pic
        #collect the uploaed file into a variable
        saver=request.files['profile_pic']
        saver.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
        #add the newly collected information to the database
        try:
            #save the uploaded file
            db.session.commit()
            #display a message that aknowledges that the record has been sucessfully collected
            flash('Record updated successfully')
            return render_template('dashboard.html',
                                   form=form,
                                   name_to_update=name_to_update)
        #if any issue was encountered, prevent the user from going further,
        #and prompt them to try again, also reload the same. 
        except:
            flash('Something went wrong, please check the information you are trying to enter and'
                  'try again')
            return render_template('dashboard.html',
                                   form=form,name_to_update=name_to_update)
    else:
        flash('not working')
        return render_template('dashboard.html', form=form, name_to_update=name_to_update)
    #return render_template('dashboard.html',form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out...never come back')
    return redirect(url_for('login'))
@app.route('/user_project', methods=['GET'])
@login_required 
def user_project():
    form=ProjectForm
    
    if form.validate_on_submit():
        flash('Your request have been collected sucessfully, you will get a reply in three days')
        return render_template('project_page.html', form=form)
    else:
        flash('please check the information you are submitting...something went wrong')
        return redirect(url_for('user_project'))
    

#defing the function that interacts with the web page collecting blog information
@app.route('/submit_blog_post', methods=['GET','POST'])
@login_required
def blog_post():
    title=None
    #author=None 
    form=BlogForm()
    #data=Posts()
    if form.validate_on_submit():
        poster=current_user.id
        title=form.title.data
        #author=form.author.data
        #filter_post=data.query.filter_by(Slug=form.slug).first()
        #if filter_post==None:
        user=Posts(Title=form.title.data, poster_id=poster, Slug=form.slug.data, Blog_content=form.content.data)
        db.session.add(user)
        db.session.commit()
        flash('Blog post have been uploaded sucessfully')
        #else:
            #flash('This blog post have been previously uploaded')
            #return render_template('Upload_blog.html', title=title, author=author, form=form)
        form.title.data=''
       # form.author.data=''
        form.slug.data=''
        form.content.data=''
        return render_template('Blog_post.html', title=title)
    else:
        return render_template('Upload_blog.html', title=title, form=form)

#editing blog post

@app.route('/edit_post/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    form=BlogForm()
    blog_info=Posts.query.get_or_404(id)
    if current_user.id==blog_info.poster.id or current_user.id==1:
        if form.validate_on_submit():
            flash('Blog post has been updated')
            blog_info.Blog_content=form.content.data
            blog_info.Title=form.title.data
            #blog_info.Author=form.author.data
            blog_info.Slug=form.slug.data
            db.session.add(blog_info)
            db.session.commit()
            #redirect to the page that contains all of the blog posts
            return redirect(url_for('Blog_posts_page'))
        form.content.data=blog_info.Blog_content
        form.title.data=blog_info.Title
        #form.author.data=blog_info.Author
        form.slug.data=blog_info.Slug
        
        return render_template ('edit_blog.html', form=form)
    else:
        flash('User Not Authorized!!! Only Author can access this page')
        return redirect(url_for('Blog_posts_page'))

@app.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    blog_info=Posts.query.get_or_404(id)
    author_id=blog_info.poster.id
    user_id=current_user.id
    blog_posts=Posts.query.order_by(Posts.date)
    if user_id==author_id or user_id==1:
        try:
            db.session.delete(blog_info)
            db.session.commit()
        except:
            flash('something went wrong, could not delete this post')
        blog_posts=Posts.query.order_by(Posts.date)
        return render_template('submited_posts.html',blog_posts=blog_posts)
    else:
        flash('User Not Authorized!!! Only Author can access this page')
        return render_template('submited_posts.html',blog_posts=blog_posts)
    
    
#updating the database with new information.    
@app.route('/user/update/<int:id>', methods=['GET','POST'])
@login_required
def update_user(id):
    form=UserForm()
    #collect an instance of the database using an id that is passed with the url
    name_to_update=db_model.query.get_or_404(id)
    #if the user submits a new form, update the content of the existing record with the new
    #information
    #if request.method=='POST':
    if form.validate_on_submit():
        name_to_update.name=form.name.data
        name_to_update.email=form.email.data
        name_to_update.about_author=form.about_author.data
        name_to_update.age=form.age.data
        name_to_update.passion=form.passion.data
        name_to_update.username=form.username.data
        name_to_update.hash_password=form.password.data
        
        #add the newly collected information to the database
        try:
            db.session.commit()
            #display a message that aknowledges that the record has been sucessfully collected
            flash('Record updated successfully')
            return render_template('update_user.html',
                                   form=form,
                                   id=id,
                                   name_to_update=name_to_update)
        #if any issue was encountered, prevent the user from going further,
        #and prompt them to try again, also reload the same. 
        except:
            flash('Something went wrong, please check the information you are trying to enter and'
                  'try again')
            return render_template('update_user.html',
                                   form=form,
                                   id=id,
                                   name_to_update=name_to_update)
    flash('Can not update record')
    return render_template('update_user.html',
                               form=form,
                               id=id,
                               name_to_update=name_to_update)


@app.route('/user_information',methods=['GET','POST'])
def database():
    name=None 
    form=UserForm()
    if form.validate_on_submit():
        #checks if the user is not entering an email that has been previously collected into the database
        user=db_model.query.filter_by(email=form.email.data).first()
        #if the email is unique, accept and collect all the information submitted by the user.
        if user==None:
            hashed_password=generate_password_hash(form.password.data)
            user=db_model(name=form.name.data, username=form.username.data, age=form.age.data, about_author=form.about_author.data, email=form.email.data, 
                          passion=form.passion.data, hash_password=hashed_password)
            db.session.add(user)
            db.session.commit()
        #assign all the newly collected information to variables
        name=form.name.data
        form.passion.data=''
        form.username.data=''
        form.about_author.data=''
        form.name.data=''
        form.age.data=''
        form.email.data=''
        flash('Your data has been collected successfully')
        current_users=db_model.query.order_by(db_model.date)
        return render_template('database.html',
                           name=name,
                           our_users=current_users,
                           form=form)
    current_users=db_model.query.order_by(db_model.date)
    return render_template('database.html',
                           name=name,
                           our_users=current_users,
                           form=form)

#allows the user to customize web response by including the desired id to the url.
@app.route('/delete/<int:id>') 
@login_required
def delete_user(id):
    if current_user.id==id:
        name=None 
        form=UserForm()
        user_to_delete=db_model.query.get_or_404(id)
        current_users=db_model.query.order_by(db_model.date)
            #if form.validate_on_submit():
                #return render_template('database.html',
                              #  name=name,
                              #  our_users=current_users,
                               ## form=form)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User deleted successfully')
            return render_template('database.html',
                               name=name,
                               our_users=current_users,
                               form=form)
        except:
            flash('Some very unexpected happened...are you trying to hack us?...please do not do that')
            return render_template('database.html',name=name,
                                   our_users=current_users,
                                   form=form)
    else:
        flash('You are not authorized to delete this page')
        return redirect(url_for('dashboard'))
            
@app.route('/user')
def see():
    name='Welcome'
    stuff='Try out the web inteface and report your experience...'
    return render_template('index.html',
                           info=name, 
                           infob=stuff) 

#creating a page that will contain all the submited blog posts
@app.route('/Posts')
def Blog_posts_page():
    
    blog_posts=Posts.query.order_by(Posts.date)
    return render_template('submited_posts.html',blog_posts=blog_posts)

#creating a page that will show each blog post

@app.route('/Post/<int:id>')

def Blog_Post(id):
    
    post=Posts.query.get_or_404(id)
    #post=Posts.query.filter_by(id=id).first()
    
    return render_template('post.html',post=post)

#defining a function that allows you to pass variables into the base file of your application
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)

#define the function that will handle the search bar on the app
@app.route('/search', methods=['POST'])
def search():
    form=SearchForm()
    posts=Posts.query
    if form.validate_on_submit():
        post_searched=form.searched.data
        #query the database post by content
        posts=posts.filter(Posts.Blog_content.like('%' + post_searched + '%'))
        posts=posts.order_by(Posts.Title).all()
        return render_template('search.html', searched=post_searched, posts=posts)
    #return render_template('search.html',form=form, searched='good God')
#defining the functions that will handle the errors
@app.route('/greet/<string:name>')
def index(name):
    return render_template('new.html', info=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500



    
#define the database table for users and call it db_model
class db_model(db.Model, UserMixin):
    
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(200), nullable=False)
    username=db.Column(db.String(50), nullable=False, unique=True)
    about_author=db.Column(db.Text(), nullable=True)
    passion=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(150), nullable=False,unique=True)
    age=db.Column(db.Integer, nullable=False)
    profile_pic=db.Column(db.String(728), nullable=True)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    #defining the password class into the database
    hash_password=db.Column(db.String(200), nullable=False)
    #defining the relationship between the db_model table and the posts table
    #note to refrence the preceding variable, 'poster' should be used.
    posts=db.relationship('Posts', backref='poster')
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    #generate a hash for the password submitted by the user
    @password.setter
    def password(self, password):
        self.hash_password=generate_password_hash(password)
    #verify that the generated hash is indeed equal to the password send into the system.
    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)
    #create a function that ilustrate something directly back on the screen
    def __repr__(self):
        
        return '<name % >r'% self.name
    
#Defining a new table for blog posts that will be sent into app by users.   
class Posts(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title=db.Column(db.String(200), nullable=False)
    #Author=db.Column(db.String(200), nullable=False)
    Slug=db.Column(db.String(200), nullable=False,unique=True)
    Blog_content=db.Column(db.Text(), nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)
    
    #create a foreign key that will connect to the db_model table using the id
    poster_id=db.Column(db.Integer, db.ForeignKey('db_model.id'))

if __name__=='__main__':
    app.run()
    
    
    
'''fields that can be used with wtforms 

BooleanField',
 'DateField', 
 'DateTimeField', 
 'DateTimeLocalField', 
 'DecimalField', 'DecimalRangeField',
 'EmailField', 'Field', 'FieldList', 
 'FileField', 'Flags', 'FloatField', 
 'FormField', 'HiddenField', 'IntegerField', 
 'IntegerRangeField', 'Label', 'MonthField', '
 MultipleFileField', 'PasswordField', 
 'RadioField', 'SearchField', 'SelectField',
 'SelectFieldBase', 'SelectMultipleField',
 'StringField', 'SubmitField', 'TelField', 'TextAreaField', 'TimeField', 'URLField',
 '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', 
 '__package__', '__path__', '__spec__', '_unset_value', 'choices', 'core', 
 'datetime', 'form', 'list', 'numeric', 'simple'
 '''