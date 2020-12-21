import os
from forms import  AddForm , DelForm , AddTheme
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app._static_folder = '/images'

# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db) #to connect the app with db

#Create table projects

class Project(db.Model):

    __tablename__ = 'projects'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)

    theme = db.relationship('Thematic',backref='project',uselist=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.theme:
            return f"Project name: {self.name} has the following thematic: {self.theme.name}"
        else:
            return f"Project name: {self.name} and has not been assigned to a thematic"

#Create table Thematic

class Thematic(db.Model):

    __tablename__ = 'themes'

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.Text)
    # We use puppies.id because __tablename__='puppies'
    project_id = db.Column(db.Integer,db.ForeignKey('projects.id'))

    def __init__(self,name,project_id):
        self.name = name
        self.project_id = project_id

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

@app.route('/theme', methods=['GET', 'POST'])
def add_theme():
    form=AddTheme()

    if form.validate_on_submit():
        name=form.name.data
        id=form.id.data

        new_theme=Thematic(name,id)
        db.session.add(new_theme)
        db.session.commit()

        return redirect(url_for('list_projects'))
    return render_template('add_theme.html', form=form)

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
