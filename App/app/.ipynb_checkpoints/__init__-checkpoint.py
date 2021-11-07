from flask import Flask
#from config import Config
app=Flask(__name__)
#app.config.from_object(Config)
#app.debug=True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['DEBUG'] = True

from app import routes