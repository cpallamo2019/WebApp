import os
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db) #to connect the app with db

#Create table

class Project(db.Model):

    __tablename__ = 'projects'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"Project name: {self.name}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data

        # Add new Puppy to database
        new_proj = Project(name)
        db.session.add(new_proj)
        db.session.commit()

        return redirect(url_for('list_projects'))

    return render_template('add.html',form=form)

@app.route('/list')
def list_projects():
    # Grab a list of puppies from database.
    projects = Project.query.all()
    return render_template('list.html', projects=projects)

@app.route('/delete', methods=['GET', 'POST'])
def del_project():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        project_id = Project.query.get(id)
        db.session.delete(project_id)
        db.session.commit()

        return redirect(url_for('list_projects'))
    return render_template('delete.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)
