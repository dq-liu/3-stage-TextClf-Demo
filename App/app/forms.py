from flask_wtf import Form
from wtforms import RadioField, SubmitField, SelectField, TextAreaField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Optional


def only_if(form, field):
	if form.good.data == 'N':
		raise ValidationError('You can only answer this question if the previous answer was Yes!')

class GoalsForm(Form):
	good = RadioField('If you only had 10 minutes to review a patient’s past clinical notes to prepare for a goals of care conversation, is this a note you would want to read?', choices=[('Y','Yes'),('N','No')], validators=[DataRequired()])
	impt = RadioField('Is this note an extremely important note?', choices=[('Y','Yes'),('N','No')], validators=[Optional(), only_if])
	send = SubmitField(label='Send')

class login(Form):
    names = RadioField('names', choices=[('casarett','Dr. Casarett'),('childers','Dr. Childers'),('griffith','Dr. Griffith'),('kim','Dr. Kim'),('lowe','Dr. Lowe'),('mumm','Dr. Mumm'),('test','Test Account')], validators=[DataRequired()])
    submit = SubmitField(label='Submit')
    