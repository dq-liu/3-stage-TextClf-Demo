from app import app
from flask import render_template, request, flash, redirect, url_for
from app.fun import *
from app.forms import GoalsForm, login
import jinja2


@app.route('/ajsjalaksneeeoeoa28474/<user>/<noteid>', methods=['GET', 'POST'])
def index(user, noteid):    
	import pandas as pd
	import numpy as np
	import pickle
	from time import gmtime, strftime
    
	user_output_noteid = 'data/' + user + '.p'
	user_output_adj = 'db_5k/' + str(noteid) + '.p'
    
	saveid = pickle.load(open(user_output_noteid, 'rb'), encoding='latin-1')

	form = GoalsForm(request.form)
	note = data_to_dict(noteid)
	note['num_reviewed'] = len(set(saveid))
    
	if note['good_'+user] != None:
		note['reviewStatusText0'] = 'You have reviewed this note!'
		if note['good_'+user] == 'Y':
			note['reviewStatusText1'] = 'Your previous answer: Yes.'
			if note['impt_'+user] == 'Y':
				note['reviewStatusText2'] = 'Your previous answer: Yes.'
			elif note['impt_'+user] == 'N':
				note['reviewStatusText2'] = 'Your previous answer: No.'
		elif note['good_'+user] == 'N':
			note['reviewStatusText1'] = 'Your previous answer: No.'

#		form = GoalsForm(data=[('good', note['good_'+user]), ('impt', note['impt_'+user])])
#		form.good.data = note['good_'+user]		# test for prepopulating
#		form.impt.data = note['impt_'+user]		# test for prepopulating

	if form.validate_on_submit():
		note['review'] += 1
		row = add_output(form)
#		saveid = pickle.load(open(user_output_noteid, 'rb'), encoding='latin-1')
		saveid.append(str(noteid))
		note['good_'+user] = row['good']
		note['impt_'+user] = row['impt']
		note.pop('num_reviewed')
		pickle.dump(saveid, open(user_output_noteid, 'wb'), protocol=2)
		pickle.dump(note, open(user_output_adj, 'wb'), protocol=2)
		return redirect(url_for('index', user=user, noteid = noteid))

	reset(form)
	return render_template('index.html', note = note, form = form, user = user, noteid = noteid)


@app.route('/', methods=['GET','POST'])
def home():
    form=login(request.form)
    if form.validate_on_submit():
        name = form.names.data
        if name == 'casarett':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8892/')
        elif name == 'childers':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8893/')
        elif name == 'griffith':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8894/')
        elif name == 'kim':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8895/')
        elif name == 'lowe':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8896/')
        elif name == 'mumm':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8897/')
        elif name == 'test':
            return redirect('http://pace-ql82pw3.dhe.duke.edu:8898/')
    return render_template('home.html', form=form)

@app.route('/alksjdnald')
def end():
    return render_template('end.html')