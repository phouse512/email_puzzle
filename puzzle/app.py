#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_required, login_user, current_user, logout_user
from flask import render_template, request, jsonify, make_response, Response, flash, redirect, session, url_for, g
from puzzle.models import Base, User, Challenge, Timer
from puzzle import config
from forms import LoginForm, ChallengeForm

from sqlalchemy import desc, and_
from sqlalchemy.orm import load_only

import time
import math

app = Flask(__name__)
app.config.from_object(config)

lm = LoginManager()
lm.init_app(app)

db = SQLAlchemy(app)
db.Model = Base

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
	return db.session.query(User).get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('home'))

	form = LoginForm() if request.method == 'POST' else LoginForm(request.args)
	if form.validate_on_submit():

		user = db.session.query(User).filter_by(username=form.username.data).filter_by(email=form.email.data).first()

		if user is None:
			flash('User does not exist, please register.')
			return redirect(url_for('welcome'))

		login_user(user)
		flash(('Logged in successfully.'))
		return redirect(url_for('home'))
	return render_template('login.html', form=form)
	
@app.route('/welcome', methods=['GET'])
def welcome():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('home'))
	return render_template('welcome.html')

@app.route('/home')
@login_required
def home():
	allChallenges = db.session.query(Challenge).filter_by(active=True)
	userChallenges = db.session.query(Timer).filter_by(user_id=g.user.id)
	score = db.session.query(User).filter_by(id=g.user.id).first()
	finished = []
	unfinished = []

	for timer in userChallenges:
		current = db.session.query(Challenge).filter_by(active=True).filter_by(id=timer.challenge_id).first()
		if timer.end_time:
			finished.append(current)
		else:
			unfinished.append(current)

	subset = finished + unfinished
	left = []

	for c in allChallenges:
		if c not in subset:
			left.append(c)

	leaders = db.session.query(User).order_by(User.score.desc()).limit(5)

	return render_template('home.html', finished=finished, unfinished=unfinished, left=left, user=score, leaders=leaders)


@app.route('/challenge/<challenge_id>', methods=['GET', 'POST'])
@login_required
def challenge(challenge_id):
	valid = db.session.query(Challenge).filter_by(active=True).filter_by(id=challenge_id).first()
	if not valid:
		flash(('Not an active challenge, sorry!'))
		return redirect(url_for('home'))

	timer = db.session.query(Timer).filter_by(user_id=g.user.id).filter_by(challenge_id=challenge_id).first()
	if not timer:
		newTimer = Timer(time.time(), challenge_id, g.user.id)
		db.session.add(newTimer)
		db.session.commit()
	else:
		if timer.end_time:
			flash(("You've already completed that challenge!"))
			return redirect(url_for('home'))

	form = ChallengeForm() if request.method == 'POST' else ChallengeForm(request.args)
	
	if form.validate_on_submit():
		if form.answer.data == valid.answer:
			end = time.time()
			timer.end_time = end

			user = db.session.query(User).filter_by(id=g.user.id).first()
			score = math.ceil(5 * valid.weight * (4000000 / (end - timer.start_time)))
			user.score = score + user.score

			db.session.commit()
			flash(('Your answer was correct! You received a score of ' + str(score) ))
			return redirect(url_for('home'))
		else:
			flash(('Ooh sorry...wrong answer, try again!'))
			return redirect(url_for('challenge', challenge_id=challenge_id))
	return render_template('challenge.html', form=form, challenge=valid)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('home'))

	form = LoginForm() if request.method == 'POST' else LoginForm(request.args)
	if form.validate_on_submit():

		user = db.session.query(User).filter_by(username=form.username.data).first()
		if user:
			flash(('Username already in use, please try again :('))
			return redirect(url_for('signup'))
		else:
			new_user = User(username=form.username.data, email=form.email.data)
			db.session.add(new_user)
			db.session.commit()
		flash(("Successfully registered! Please now login below!"))
		return redirect(url_for('login'))
	elif(form.errors):
		flash((form.errors))
	return render_template('signup.html', form=form)

# Example of ajax route that returns JSON
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)