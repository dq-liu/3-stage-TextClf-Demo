import pandas as pd
import pickle
import numpy as np

def data_to_dict(noteid):
    db = pickle.load(open('db_5k/'+str(noteid)+'.p', 'rb'), encoding='latin-1')
    return db

def add_output(form):
	return {'good':form.good.data, 'impt':form.impt.data}

def reset(form):
	form.good.data = None
	form.impt.data = None