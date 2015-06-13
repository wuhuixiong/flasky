#coding=utf-8
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from wtforms.fields.simple import PasswordField
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
import os, os.path

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['DEBUG']=True
app.config['SECRET_KEY'] = 'aXdfe0BefafY4Qar6gqA9z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'huixiongwu@gmail.com'
app.config['MAIL_PASSWORD'] = 'stone46364488'

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)



            
@app.route('/', methods=['GET','POST'])
def index( ):
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known',False))
        


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role',lazy = 'dynamic')
    def __repr_(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    #password = PasswordField('PASSWORD:', validators=[Required()])
    submit = SubmitField('OK')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, mail=mail)
manager.add_command("shell", Shell(make_context=make_shell_context))



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=80)
    manager.run()