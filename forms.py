from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField



class AddForm(FlaskForm):

    name = StringField('Name of Project:')
    submit = SubmitField('Add Project')

class DelForm(FlaskForm):

    id = IntegerField('Id Number of Project to Remove:')
    submit = SubmitField('Remove Project')

class AddTheme(FlaskForm):
    name = StringField('Which is the thematic of the project')
    id = IntegerField ('Project ID')
    submit = SubmitField ('Add Thematic')
