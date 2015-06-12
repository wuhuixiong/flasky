#coding=utf-8

from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.config['DEBUG']=True
            
@app.route('/')
def index( ):
    #return '<h1>Hello World!</h1>'
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s!</h1>'%name
    return render_template('user.html', name=name, comments=['a','b','c'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)