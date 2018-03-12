import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import re
import datetime as dt
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, MinMaxScaler
# from sklearn.feature_selection import chi2, SelectKBest
# from sklearn.decomposition import TruncatedSVD
# from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.linear_model import LogisticRegression
# from imblearn.under_sampling import RandomUnderSampler
import nltk
from nltk.tokenize import word_tokenize
from tamagombti import *
import time
import pickle

start = time.time()
print "start"
#CONFIG
app = flask.Flask(__name__)
app.config['DEBUG'] = True

# #Initialize database
# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
#
# db = SQLAlchemy(app)

#Unpickle
with open('extra','r') as f:
    E = pickle.load(f)
f.close()
with open('sense','r') as f:
    S = pickle.load(f)
f.close()
with open('think','r') as f:
    T = pickle.load(f)
f.close()
with open('judge','r') as f:
    J = pickle.load(f)
f.close()

#Initialize new user
def typerologie(M, label):
    numb, proba = newguy.perform_magic(M)
    number = numb[0]
    result1 = label[number]
    result2 = proba[0][number] / sum(proba[0])
    return number, result1, str(round((result2*100),2))+'%'
mailey=[]

end = time.time()
duration = end-start
print "Time elapsed: "+ str(round(duration/60))+' min and '+str(round(duration%60))+' sec'

# App rounting
@app.route('/')
def index():
    global newguy
    newguy = NewBerd()
    global usecount
    usecount = len(newguy.wordlist)
    assert newguy.wordlist == []
    return flask.render_template('default.html', c=usecount)

@app.route('/1',  methods=['POST', 'GET'])
def addword():
    if request.method == 'POST' and len(request.form['entry']) != 0:
        newguy.preprocess(request.form['entry'])
        usecount=len(newguy.wordlist)
        return flask.render_template('default.html', c=usecount)

@app.route('/2', methods=['POST', 'GET'])
def predefined():
    if request.method == 'POST': #Luckily the webpage serves as a natural filter
        choice = int(request.form['number'])
        giraffe = pd.read_csv('mbti_1.csv')
        wordlist = giraffe.iloc[choice, 1].split('|||')
        for line in wordlist:
            newguy.preprocess(line)
        usecount=len(newguy.wordlist)
        return flask.render_template('default.html', c=usecount)

@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/result')
def result():
    assert len(newguy.wordlist) > 30
    E_r, E_result, E_proba = typerologie(E, label=['Introverted','Extraverted'])
    S_r, S_result, S_proba = typerologie(S, label=['iNtuitive','Sensing'])
    T_r, T_result, T_proba = typerologie(T, label=['Feeling','Thinking'])
    J_r, J_result, J_proba = typerologie(J, label=['Perceiving','Judging'])
    typer = ['I','E'][E_r]+['N','S'][S_r]+['F','T'][T_r]+['P','J'][J_r]
    return flask.render_template('result.html', typer=typer, e1=E_result, e2=E_proba, s1=S_result, s2=S_proba,
                                    t1=T_result, t2=T_proba, j1=J_result, j2=J_proba, wordy=newguy.wordlist)
#
# @app.route('/addemail')
# def addemail():
#     if request.method == 'POST':
#         mailey.append(request.form['email'])
#         return flask.render_template('addemail.html')
#
# @app.route('/danoob-secret-stash')
# def secret():
# 	return flask.render_template('emailcollect.html', mailey = mailey)

# Run application
if __name__ == "__main__":
    app.run(use_reloader=False)
