from flask import Flask, render_template, request, redirect, url_for, make_response, abort
# from flask_mongoengine import MongoEngine, Document
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, Form, SelectField, SubmitField, BooleanField
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from wtforms.validators import Email, Length, InputRequired, EqualTo, Regexp, URL
# from wtforms.widgets import TextArea
# from werkzeug.security import generate_password_hash, check_password_hash
# from db_connect import MONGODB_URI, db
# from math import ceil
# from binascii import hexlify
# from forms import ContactForm, FilterForm, AccountForm, InvestorAccountForm, CommentForm, AddAdminForm, RemoveAdminForm, DeleteUserForm, DonateForm
# from credentials import mlab_host, mlab_api_key, google_api_key, google_client_id, google_client_secret, gmail_password, google_app_password, sendgrid_password, cloudinary_api_key, cloudinary_api_secret
# from webclasses import WebStartup, WebInvestor, pushStartup, updateStartup, pushInvestor, updateInvestor, parse_multi_form, WebUser
# from flask_uploads import UploadSet, configure_uploads, IMAGES
# from flask_mail import Mail, Message
# # from flask_oauth import OAuth
# from oauth_flask import OAuth

# import urllib
# import time

# try:
# 	from urllib import urlopen
# except:
	# from urllib.request import urlopen

# heroku push fails with first one; internal development server only works with first one and doesn't work with #2.

# from pygeocoder import Geocoder
# import pandas as pd
# import numpy as np
# import pymongo
# from pymongo import GEO2D, GEOSPHERE
# import functools
# from pymongo import MongoClient
# import io; io.StringIO()
# import random
# import string
import os
# import csv
# import re
# import json
# import datetime as dt
# from datetime import datetime, timedelta

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'db': 'incub8sf',
#     'host': db_uri,
#     'username': 'incub8sf',
#     'password': 'willw0ntwin'
# }

db = {"Startups":{"test":{"feature":"true"}}}

@app.errorhandler(404)
def page_not_found(e):
    title = 'Not Found'
    code = '404'
    message = "We can't seem to find the page you're looking for."
    return render_template('error.html', title = title, code = code, message = message), 404

@app.errorhandler(403)
def page_forbidden(e):
    title = 'Forbidden'
    code = '403'
    message = "You do not have access to this page."
    return render_template('error.html', title = title, code = code, message = message), 403

@app.errorhandler(500)
def internal_server_error(e):
    title = 'Internal Server Error'
    code = '500'
    message = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    return render_template('error.html', title = title, code = code, message = message), 500

@app.route('/')
def index():
	# current_features = ["sophiamartika", "incub8", "eaglerivercustomtshirts"]
	# features = list(db.Startups.find({"id": {"$in": current_features}}))
	# features = list(db.Startups.find({"feature": True}))
	# feature_indexes = []
	# for feature in features:
	# 	feature["index"] = features.index(feature)
	# 	if "location" in feature:
	# 		if "latitude" in feature["location"]:
	# 			feature["coordinates"] = [feature["location"]["latitude"], feature["location"]["longitude"]]
	# 			feature["location"] = feature["location"]["address"]
	# 	feature_indexes.append(features.index(feature))
	# feature_indexes.pop(0)
	return render_template('index.html')
	# return render_template('index.html', feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)

@app.route('/sorry')
def sorry():
    return render_template('under_construction.html')

# @app.route('/explore', methods=['GET', 'POST'])
# def startups():
# 	form = FilterForm()
# 	category = request.args.get('category', None)
# 	tag = request.args.get('tag', None)
# 	latitude = request.args.get('lat', None)
# 	longitude = request.args.get('long', None)
# 	country = request.args.get('country', None)
# 	query = request.args.get('query', None)
# 	exact_location = request.args.get('in', None)
# 	radius = request.args.get('radius', None)
# 	if request.method == 'POST':
# 		category = form.category.data or None
# 		query = form.query.data or None
# 		location = form.location.data or None
# 		if location:
# 			location_info = Geocoder(api_key=google_api_key).geocode(location)
# 			coordinates = list(location_info.coordinates)
# 			latitude = str(coordinates[0])
# 			longitude = str(coordinates[1])
# 		radius = form.radius.data or None
# 		if radius:
# 			radius = (float(radius)/0.62137119)*1000

# 	search_options = {}

# 	if category == "All":
# 		category = None

# 	if category == "None":
# 		category = None

# 	if category is not None:
# 		search_options["category"] = category
# 	if exact_location is not None:
# 		search_options["exact_location"] = exact_location
# 	if tag is not None:
# 		search_options["tag"] = tag
# 	if latitude is not None:
# 		search_options["latitude"] = float(latitude)
# 	if longitude is not None:
# 		search_options["longitude"] = float(longitude)
# 	if query is not None:
# 		search_options["query"] = query
# 	if country is not None:
# 		search_options["country"] = country

# 	print(search_options)

# 	if search_options:
# 		if "category" in search_options:
# 		    all_startups = db.Startups.find({'category': {'$regex': category, "$options": "-i"}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "tag" in search_options:
# 			 all_startups = db.Startups.find({}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "exact_location" in search_options:
# 			 all_startups = db.Startups.find({'location_str': {'$regex': exact_location, "$options": "-i"}}).sort('date', pymongo.DESCENDING).limit(25)
# 		    # all_startups = db.Startups.find({'tags': {'$elemMatch': {tag}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "country" in search_options:
# 		    all_startups = db.Startups.find({'location': {'country': {'$regex': search_options["country"], "$options": "-i"}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "latitude" in search_options and "longitude" in search_options:
# 			if radius is None:
# 				radius = 10000
# 			all_startups = db.Startups.find({'coordinates':{"$near": [ search_options["longitude"] , search_options["latitude"] ]}}).limit(25)
# 			# all_startups = db.Startups.find({"geometry":  {"$nearSphere": {"$geometry": {"type" : "Point","coordinates" : [ search_options["longitude"], search_options["latitude"] ]}, "$maxDistance": radius}}})
# 		if "query" in search_options:
# 		    all_startups = db.Startups.find({'name': {'$regex': query, "$options": "-i"}}).sort('date', pymongo.DESCENDING).limit(25)
# 	else:
# 		all_startups = db.Startups.find({}).sort('date', pymongo.DESCENDING).limit(25)
# 	return render_template('pinterest_startups.html', form = form, startups=all_startups, logged_in=current_user.is_authenticated, api_key = google_api_key, categories = categories_list)




# @app.route('/favorites', methods=['GET', 'POST'])
# @login_required
# @investor_required
# def favorite_startups():
# 	this_investor_info = WebInvestor(current_user.email).get_info()
# 	all_startups = []
# 	startup_ids = []
# 	if "saved" in this_investor_info:
# 		for this_startup in this_investor_info["saved"]:
# 			new_startup = WebStartup(this_startup["id"]).get_info()
# 			all_startups.append(new_startup)
# 			startup_ids.append(this_startup["id"])
# 	else:
# 		print("what a loser")
# 	form = FilterForm()
# 	category = request.args.get('category', None)
# 	tag = request.args.get('tag', None)
# 	query = request.args.get('query', None)
# 	exact_location = request.args.get('in', None)
# 	if request.method == 'POST':
# 		category = form.category.data or None
# 		query = form.query.data or None
# 	search_options = {}
# 	if category == "All":
# 		category = None
# 	if category == "None":
# 		category = None
# 	if category is not None:
# 		search_options["category"] = category
# 	if exact_location is not None:
# 		search_options["exact_location"] = exact_location
# 	if tag is not None:
# 		search_options["tag"] = tag
# 	if query is not None:
# 		search_options["query"] = query
# 	print(search_options)
# 	if search_options:
# 		if "category" in search_options:
# 		    all_startups = db.Startups.find({'category': {'$regex': category, "$options": "-i"}},{{ 'id': { '$in': startup_ids}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "tag" in search_options:
# 			 all_startups = db.Startups.find({{ 'id': { '$in': startup_ids}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "exact_location" in search_options:
# 			 all_startups = db.Startups.find({'location': {'$regex': exact_location, "$options": "-i"}},{{ 'id': { '$in': startup_ids}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		    # all_startups = db.Startups.find({'tags': {'$elemMatch': {tag}}}).sort('date', pymongo.DESCENDING).limit(25)
# 		if "query" in search_options:
# 		    all_startups = db.Startups.find({'name': {'$regex': query, "$options": "-i"}},{{ 'id': { '$in': startup_ids}}}).sort('date', pymongo.DESCENDING).limit(25)
# 	else:
# 		all_startups = db.Startups.find({ 'id': { '$in': startup_ids}}).sort('date', pymongo.DESCENDING).limit(25)
# 	return render_template('pinterest_startups.html', form = form, startups=all_startups, logged_in=current_user.is_authenticated, api_key = google_api_key, categories = categories_list)

# @app.route('/submission')
# def submision():
#     return redirect(url_for('cac_submission'))

# our_founders = [{"key":"isabella", "email":'ihochschild@gmail.com'}, {"key":"aarushi", "email":'aarushi03@hotmail.com'}, {"key":"sriya", "email":'sriyaaluru@gmail.com'}] 

# @app.route('/about')
# def about():
# 	info = {}
# 	for founder in our_founders:
# 		founder_info = WebUser(founder["email"]).get_info()
# 		info[founder["key"]] = founder_info
# 	return render_template('about.html', info = info, logged_in=current_user.is_authenticated)

# @app.route('/2018-congressional-app-challenge-submission')
# def cac_submission():
#     return render_template('submission.html', logged_in=current_user.is_authenticated)

# @app.route('/demo-video')
# def demo_video():
#     return render_template('demo_video.html', logged_in=current_user.is_authenticated)

# @app.route('/extended-family')
# def extended_family():
#     return render_template('extended_family.html', logged_in=current_user.is_authenticated)

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     form = ContactForm()
#     if request.method == 'POST':
#     	if form.validate():
#         	contact_us(form.subject.data, form.name.data, form.email.data, form.message.data)
#         	if current_user.is_authenticated:
#         		return redirect(url_for('dashboard', if_message = True, message="Your message was sent."))
#         	else:
#         		return render_template('contact.html', post = 'yup', form = form, logged_in=current_user.is_authenticated)
#     form.name.data = ""
#     form.email.data = ""
#     form.subject.data = ""
#     form.message.data = ""
#     return render_template('contact.html', form = form, logged_in=current_user.is_authenticated)

# @app.route('/swipe')
# def swipe():
# 	filters = {}
# 	total_startup_n = db.Startups.find(filters).count()
# 	startup_ids = db.Startups.find(filters, {'id':1}).sort("name", pymongo.DESCENDING)
# 	all_startups = list(db.Startups.find({ "id": { "$ne": "incub8" }}))
# 	new_startups = []
# 	last_startup = WebStartup('incub8').get_info()
# 	for this_startup in all_startups:
# 		new_startup = this_startup
# 		if "location" in this_startup:
# 			if "latitude" in this_startup["location"]:
# 				new_startup["coordinates"] = [this_startup["location"]["latitude"], this_startup["location"]["longitude"]]
# 				new_startup["location"] = this_startup["location"]["address"]
# 		new_startups.append(new_startup)
# 	all_startups = new_startups
# 	if_investor = False
# 	investor_email = None
# 	if current_user.is_authenticated:
# 		if current_user.role == "investor":
# 			# investor_info = WebInvestor(current_user.email).get_info()
# 			# if investor_info:
# 			# 	investor_email = investor_info["email"]
# 			# 	if_investor = True
# 			investor_email = current_user.email
# 			if_investor = True
# 	return render_template('swipe.html', investor_email = investor_email, if_investor = if_investor, api_key = mlab_api_key, last_startup = last_startup, startups=all_startups, n_total=total_startup_n, logged_in=current_user.is_authenticated)

# @app.route('/test')
# def test():
# 	test_mail()
# 	return redirect(url_for('index'))


# # @app.route('/batch-operation')
# # @admin_required
# def one_time_only():
# 	# all_startups = list(db.Startups.find({}))
# 	# for this_startup in all_startups:
# 	# 	updates = {}
# 	# 	updates["location"] = {}
# 	# 	if "location" in this_startup:
# 	# 		if "coordinates" in this_startup:
# 	# 			print(this_startup["coordinates"])
# 	# 			try:
# 	# 				location_info = Geocoder(api_key=google_api_key).reverse_geocode(this_startup['coordinates'][0], this_startup['coordinates'][1])
# 	# 				print(location_info.coordinates)
# 	# 				updates['location']['latitude'] = this_startup['coordinates'][0]
# 	# 				updates['location']['longitude'] = this_startup['coordinates'][1]
# 	# 				updates['location']['address'] = location_info.formatted_address
# 	# 				updates['location']['country'] = location_info.country
# 	# 				print(this_startup["name"]+" was updated...")
# 	# 				db.Startups.find_one_and_update({"email": this_startup["email"]}, {"$set": updates})
# 	# 			except:
# 	# 				print(this_startup["name"]+" is a little bitch...")
# 	all_investors = list(db.Investors.find({}))
# 	for this_investor in all_investors:
# 		if "name" in this_investor:
# 			new_id = this_investor["name"].replace(" ", "").lower()
# 		else:
# 			new_id = this_investor["email"].split("@")[0].lower()
# 		starting_id = new_id
# 		while db.Investors.find({'id':new_id}).count() > 0:
# 			new_id = starting_id
# 			num_range = range(1, 999)
# 			new_id = new_id+str(random.choice(num_range))
# 		db.Investors.find_one_and_update({"email": this_investor["email"]}, {"$set": {"id":new_id}})
# 	# location_info = Geocoder(api_key=google_api_key).geocode("699 8th St, San Francisco, CA 94103")
# 	# print(location_info.coordinates)
# 	return redirect(url_for('index'))
	


# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
# 	role = request.args.get('role', default=None, type=None)
# 	if role == "investor":
# 		form = RegForm()
# 	elif role == "startup":
# 		form = SignUpForm()
# 	if request.method == 'POST':
# 		if form.validate():
# 			print('looks like the form validated')
# 			existing_user = User.objects(email=form.email.data).first()
# 			if existing_user is None:
# 				hashpass = generate_password_hash(form.password.data, method='sha256')
# 				hey = User(form.email.data,hashpass,form.name.data,role).save()
# 				login_user(hey)
# 				name = form.name.data
# 			if role == "investor":
# 				investor_dict = {}
# 				investor_dict['email'] = form.email.data
# 				investor_dict['name'] = form.name.data
# 				investor_dict['timestamp'] = datetime.now()
# 				new_id = investor_dict['name'].replace(" ", "").lower()
# 				while db.Startups.find({'id':new_id}).count() > 0:
# 					new_id = investor_dict['name'].replace(" ", "").lower()
# 					num_range = range(1, 999)
# 					new_id = new_id+str(random.choice(num_range))
# 				investor_dict["id"] = new_id
# 				db.Investors.insert(investor_dict)
# 				welcome_email(form.email.data, role)
# 				return redirect(url_for('dashboard', name=form.name.data))
# 			elif role == "startup":
# 				startup_dict = {}
# 				startup_dict['email'] = form.email.data
# 				startup_dict['name'] = form.name.data
# 				startup_dict['timestamp'] = datetime.now()
# 				startup_dict['description'] = form.description.data
# 				if form.location.data is None:
# 					if not form.city.data == "":
# 						startup_dict['location'] = form.city.data + ", " + form.state.data
# 					else:
# 						startup_dict['location'] = {'address': form.address.data}
# 				else:
# 					startup_dict['location'] = form.location.data
# 				startup_dict['image'] = form.image.data
# 				new_id = form.name.data.replace(" ", "").lower()
# 				while db.Startups.find({'id':new_id}).count() > 0:
# 					new_id = startup_dict['name'].replace(" ", "").lower()
# 					num_range = range(1, 999)
# 					new_id = new_id+str(random.choice(num_range))
# 				startup_dict["id"] = new_id
# 				startup_dict['category'] = form.category.data
# 				startup_dict['tags'] = form.tags.data.split(",")

# 				# watch out below

# 				if "demo" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				if "fake news" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				# hey delete above
				
# 				try:
# 					# if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 					location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 					coordinates = list(location_info.coordinates)
# 					startup_dict['coordinates'] = coordinates
# 					startup_dict["location"] = {}
# 					startup_dict['location']['latitude'] = coordinates[0]
# 					startup_dict['location']['longitude'] = coordinates[1]
# 					startup_dict['location']['address'] = location_info.formatted_address
# 					startup_dict['location']['country'] = location_info.country
# 				except:
# 					print('oopsie')
# 					startup_dict["location"] = {'address':form.address.data}
# 				if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 					location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 					print(location_info)
# 					print(location_info.coordinates)
# 					coordinates = list(location_info.coordinates)
# 					startup_dict['coordinates'] = coordinates
# 					startup_dict['location']['latitude'] = coordinates[0]
# 					startup_dict['location']['longitude'] = coordinates[1]
# 					startup_dict['location']['address'] = location_info.formatted_address
# 					startup_dict['location']['country'] = location_info.country
# 				else:
# 					startup_dict["location"] = {'address':form.address.data}
# 				startup_dict['goals'] = {}
# 				if form.mentor_goal.data:
# 					startup_dict["goals"]["mentor"] = form.mentor_goal.data
# 				if form.funding_goal.data:
# 					startup_dict["goals"]["funding"] = form.funding_goal.data
# 				if form.awareness_goal.data:
# 					startup_dict["goals"]["awareness"] = form.awareness_goal.data
# 				if form.website.data:
# 					startup_dict['website'] = form.website.data
# 				if not db.Startups.find({'name':form.name.data}).count() > 0:
# 					db.Startups.insert(startup_dict)
# 				welcome_email(form.email.data, role)
# 				return redirect(url_for('dashboard'))
# 		elif form.errors == {'city': [u'Not a valid choice']}:
# 			existing_user = User.objects(email=form.email.data).first()
# 			if existing_user is None:
# 				hashpass = generate_password_hash(form.password.data, method='sha256')
# 				hey = User(form.email.data,hashpass,form.name.data,role).save()
# 				login_user(hey)
# 			if role == "investor":
# 				investor_dict = {}
# 				investor_dict['email'] = form.email.data
# 				investor_dict['timestamp'] = datetime.now()
# 				if form.name.data:
# 					investor_dict['name'] = form.name.data
# 					new_id = investor_dict['name'].replace(" ", "")
# 					while db.Startups.find({'id':new_id}).count() > 0:
# 						new_id = investor_dict['name'].replace(" ", "")
# 						num_range = range(1, 999)
# 						new_id = new_id+str(random.choice(num_range))
# 					investor_dict["id"] = new_id
# 				if not db.Investors.find({'name':form.name.data}).count() > 0:
# 					db.Investors.insert(investor_dict)
# 				welcome_email(form.email.data, role)
# 				return redirect(url_for('dashboard'))
# 			elif role == "startup":
# 				startup_dict = {}
# 				name = form.name.data
# 				startup_dict['email'] = form.email.data
# 				startup_dict['name'] = form.name.data
# 				startup_dict['timestamp'] = datetime.now()
# 				startup_dict['description'] = form.description.data
# 				startup_dict['tags'] = form.tags.data.split(",")

# 				# watch out below

# 				if "demo" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				if "fake news" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				# hey delete above
				
# 				if form.location.data == "":
# 					if not form.city.data == "":
# 						startup_dict['location'] = form.city.data + ", " + form.state.data
# 					else:
# 						startup_dict['location'] = form.state.data
# 				else:
# 					startup_dict['location'] = form.location.data
# 				try:
# 					# if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 					location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 					coordinates = list(location_info.coordinates)
# 					startup_dict['coordinates'] = coordinates
# 					startup_dict["location"] = {}
# 					startup_dict['location']['latitude'] = coordinates[0]
# 					startup_dict['location']['longitude'] = coordinates[1]
# 					startup_dict['location']['address'] = location_info.formatted_address
# 					startup_dict['location']['country'] = location_info.country
# 				except:
# 					print('oopsie')
# 				startup_dict['city'] = form.city.data
# 				startup_dict['state'] = form.state.data
# 				startup_dict['image'] = form.image.data
# 				startup_dict['category'] = form.category.data
# 				new_id = form.name.data.replace(" ", "").lower()
# 				while db.Startups.find({'id':new_id}).count() > 0:
# 					new_id = startup_dict['name'].replace(" ", "").lower()
# 					num_range = range(1, 999)
# 					new_id = new_id+str(random.choice(num_range))
# 				startup_dict["id"] = new_id
# 				startup_dict['tags'] = form.tags.data.split(",")

# 				# watch out below

# 				if "demo" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				if "fake news" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				# hey delete above
				
# 				startup_dict['goals'] = {}
# 				if form.mentor_goal.data:
# 					startup_dict["goals"]["mentor"] = form.mentor_goal.data
# 				if form.funding_goal.data:
# 					startup_dict["goals"]["funding"] = form.funding_goal.data
# 				if form.awareness_goal.data:
# 					startup_dict["goals"]["awareness"] = form.awareness_goal.data
# 				if form.website.data:
# 					startup_dict['website'] = form.website.data
# 				if not db.Startups.find({'name':form.name.data}).count() > 0:
# 					db.Startups.insert(startup_dict)
# 				welcome_email(form.email.data, role)
# 				return redirect(url_for('dashboard'))
# 		elif form.errors == {'city': [u'Not a valid choice'], 'state': [u'Not a valid choice']}:
# 			existing_user = User.objects(email=form.email.data).first()
# 			if existing_user is None:
# 				hashpass = generate_password_hash(form.password.data, method='sha256')
# 				hey = User(form.email.data,hashpass,form.name.data,role).save()
# 				login_user(hey)
# 			if role == "startup":
# 				startup_dict = {}
# 				name = form.name.data
# 				startup_dict['email'] = form.email.data
# 				startup_dict['name'] = form.name.data
# 				startup_dict['timestamp'] = datetime.now()
# 				startup_dict['description'] = form.description.data
# 				if form.location.data == "":
# 					if not form.city.data == "":
# 						startup_dict['location'] = form.city.data + ", " + form.state.data
# 					else:
# 						startup_dict['location'] = form.state.data
# 				else:
# 					startup_dict['location'] = form.location.data
# 				startup_dict['city'] = form.city.data
# 				startup_dict['state'] = form.state.data
# 				startup_dict['image'] = form.image.data
# 				startup_dict['category'] = form.category.data
# 				new_id = form.name.data.replace(" ", "").lower()
# 				while db.Startups.find({'id':new_id}).count() > 0:
# 					new_id = startup_dict['name'].replace(" ", "").lower()
# 					num_range = range(1, 999)
# 					new_id = new_id+str(random.choice(num_range))
# 				startup_dict["id"] = new_id
# 				startup_dict['tags'] = form.tags.data.split(",")

# 				# watch out below

# 				if "demo" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				if "fake news" in startup_dict['tags']:
# 					startup_dict['role'] = "demo"

# 				# hey delete above

# 				try:
# 					# if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 					location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 					coordinates = list(location_info.coordinates)
# 					startup_dict['coordinates'] = coordinates
# 					startup_dict["location"] = {}
# 					startup_dict['location']['latitude'] = coordinates[0]
# 					startup_dict['location']['longitude'] = coordinates[1]
# 					startup_dict['location']['address'] = location_info.formatted_address
# 					startup_dict['location']['country'] = location_info.country
# 				except:
# 					print('oopsie')
				
# 				if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 					location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 					print(location_info)
# 					print(location_info.coordinates)
# 					coordinates = location_info.coordinates.split("(")[1]
# 					coordinates = coordinates.split(")")[0]
# 					coordinates = coordinates.split(", ")
# 					startup_dict['coordinates'] = coordinates
# 					startup_dict['location']['latitude'] = coordinates[0]
# 					startup_dict['location']['longitude'] = coordinates[1]
# 					startup_dict['location']['address'] = location_info.formatted_address
# 					startup_dict['location']['country'] = location_info.country
# 				else:
# 					startup_dict["location"] = {'address':form.address.data}
# 				startup_dict['goals'] = {}	
# 				if form.mentor_goal.data:
# 					startup_dict["goals"]["mentor"] = form.mentor_goal.data
# 				if form.funding_goal.data:
# 					startup_dict["goals"]["funding"] = form.funding_goal.data
# 				if form.awareness_goal.data:
# 					startup_dict["goals"]["awareness"] = form.awareness_goal.data
# 				if form.website.data:
# 					startup_dict['website'] = form.website.data
# 				if not db.Startups.find({'name':form.name.data}).count() > 0:
# 					db.Startups.insert(startup_dict)
# 				welcome_email(form.email.data, role)
# 				return redirect(url_for('dashboard'))
# 		else:
# 			print(form.errors)
# 	if role == "investor":
# 		form = RegForm()
# 		return render_template('investor_signup.html', form=form)
# 	elif role == "startup":
# 		form = SignUpForm()
# 		data = cities_info
# 		return render_template('startup_signup.html', cities_info = data, form=form, api_key = google_api_key)
# 	return render_template('registration.html', form=form)

# @app.route('/invest', methods=['GET'])
# def invest():
# 	return render_template('invest.html', logged_in = current_user.is_authenticated)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard', name=current_user.email))
#     if request.method == 'POST':
#         if form.validate():
#             check_user = User.objects(email=form.email.data).first()
#             if check_user:
#                 if check_password_hash(check_user['password'], form.password.data):
#                     login_user(check_user)
#                     return redirect(url_for('dashboard'))
#         else:
#             print(form.errors)
#     return render_template('login.html', form=form)

# @app.route('/logout', methods = ['GET'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# @app.route('/dashboard', methods = ['GET','POST'])
# @login_required
# def dashboard():
# 	action = None
# 	updates = {}
# 	if_update = False
# 	message = None
# 	if current_user.role == "startup":
# 	    form = AccountForm()
# 	    startup_info = WebStartup(current_user.email).get_info()
# 	    print(startup_info)
# 	    if request.method == 'POST':
# 	    	action = request.args.get('action')
# 	    	updates = {}
# 	    	if action == "bio":
# 	    		if form.bio.data:
# 	    			updates["description"] = form.bio.data
# 	    	elif action == "goals":
# 	    		updates["goals"] = {}
# 	    		if form.mentor_goal.data:
# 	    			updates["goals"]["mentor"] = form.mentor_goal.data
# 	    		if form.funding_goal.data:
# 	    			updates["goals"]["funding"] = form.funding_goal.data
# 	    		if form.awareness_goal.data:
# 	    			updates["goals"]["awareness"] = form.awareness_goal.data
# 	    	elif action == "password":
# 	    		if form.password.data and form.confirm_password.data:
# 	    			if form.password.data == form.confirm_password.data:
# 	    				hashpass = generate_password_hash(form.password.data, method='sha256')
# 	    				user = current_user
# 	    				user.password = hashpass
# 	    				db.Users.find_one_and_update({"email": current_user.email}, {"$set": {"password":hashpass}})
# 	    			else:
# 	    				print('uh nah')
# 	    	elif action == "social":
# 	    		updates["social"] = {}
# 	    		if form.facebook.data:
# 	    			updates["social"]["facebook"] = form.facebook.data
# 	    		if form.instagram.data:
# 	    			updates["social"]["instagram"] = form.instagram.data
# 	    		if form.twitter.data:
# 	    			updates["social"]["twitter"] = form.twitter.data
# 	    		if form.pinterest.data:
# 	    			updates["social"]["pinterest"] = form.pinterest.data
# 	    		if form.website.data:
# 	    			updates["website"] = form.website.data
# 	    	elif action == "image":
# 	    		if form.image.data:
# 	    			updates["image"] = form.image.data
# 	    		elif not form.image.data:
# 	    			updates["image"] = None
# 	    		if 'photo' in request.files:
# 	    			filename = photos.save(request.files['photo'])
# 	    			updates["pic"] = filename
# 	    			updates["image"] = "http://incub8.herokuapp.com/static/user/img/"+filename
# 	    			# new_pic = Cloud.CloudinaryImage(request.files['photo'])
# 	    			# new_pic = cloudinary.uploader.upload({
# 	    			# 	"file": request.files['photo'],
# 	    			# 	"public_id": startup_info["id"]+"_profile",
# 	    			# 	"tags": ['INCUB8', 'startup']
# 	    			# 	})
# 	    			cloudinary.uploader.upload(request.files['photo'], public_id = startup_info['id']+'_profile')
# 	    			img = cloudinary.CloudinaryImage(startup_info['id']+'_profile', format="png")
# 	    			print(img.url)
# 	    			updates["image"] = img.url
# 	    	elif action == "location":
# 	    		updates["location"] = {}
# 	    		# if Geocoder(api_key=google_api_key).geocode(form.address.data).valid_address:
# 	    		location_info = Geocoder(api_key=google_api_key).geocode(form.address.data)
# 	    		coordinates = []
# 	    		coordinates = list(location_info.coordinates)
# 	    		# coordinates = location_info.coordinates.split("(")[1]
# 	    		# coordinates = coordinates.split(")")[0]
# 	    		# coordinates = coordinates.split(", ")
# 	    		updates['coordinates'] = coordinates
# 	    		updates['location']['latitude'] = coordinates[0]
# 	    		updates['location']['longitude'] = coordinates[1]
# 	    		updates['location']['address'] = location_info.formatted_address
# 	    		updates['location']['country'] = location_info.country
# 	    	if updates:
# 	    		print(updates)
# 	    		if_update = True
# 	    		db.Startups.find_one_and_update({"email": current_user.email}, {"$set": updates})
# 	    startup_info = WebStartup(current_user.email).get_info()
# 	    if 'social' in startup_info:
# 	    	for x in startup_info['social']:
# 	    		form[x].data = startup_info['social'][x]
# 	    form.bio.data = startup_info['description']
# 	    if "image" in startup_info:
# 	    	form.image.data = startup_info['image']
# 	    if "location" in startup_info:
# 	    	if "address" in startup_info["location"]:
# 	    		form.location.data = startup_info['location']["address"]
# 	    return render_template('account_startup.html', update = if_update, message = message, info = startup_info, logged_in=current_user.is_authenticated, form = form, dashboard=True)
# 	elif current_user.role == "investor":
# 		form = InvestorAccountForm()
# 		investor_info = WebInvestor(current_user.email).get_info()
# 		if request.method == 'POST':
# 			action = request.args.get('action')
# 			updates = {}
# 			if action == "bio":
# 				if form.bio.data:
# 					updates["bio"] = form.bio.data
# 			elif action == "image":
# 				if form.image.data:
# 					updates["image"] = form.image.data
# 				if 'photo' in request.files:
# 					filename = photos.save(request.files['photo'])
# 					print(filename)
# 					updates["pic"] = filename
# 					updates["image"] = "http://incub8.herokuapp.com/static/user/img/"+filename
# 					# new_pic = Cloud.CloudinaryImage(request.files['photo'])
# 					try:
# 						cloudinary.uploader.upload(request.files['photo'])
# 						img = cloudinary.CloudinaryImage(investor_info['id']+'_profile', format="png")
# 						print(img.url)
# 						updates["image"] = img.url
# 					except:
# 						print("cloudinary error")
# 			if action == "password":
# 				print(current_user.password)
# 				if form.password.data and form.confirm_password.data:
# 					print("- - -")
# 					if form.password.data == form.confirm_password.data:
# 						print('uh yah')
# 						print(current_user.password)
# 						hashpass = generate_password_hash(form.password.data, method='sha256')
# 						user = current_user
# 						user.password = hashpass
# 						print(current_user.password)
# 						db.Users.find_one_and_update({"email": current_user.email}, {"$set": {"password":hashpass}})
# 					else:
# 						print('uh nah')
# 			if updates:
# 				if_update = True
# 				db.Investors.find_one_and_update({"email": current_user.email}, {"$set": updates})
# 		if "bio" in investor_info:
# 			form.bio.data = investor_info["bio"]
# 		elif "description" in investor_info:
# 			form.bio.data = investor_info["description"]
# 		if "bio" in investor_info:
# 			form.bio.data = investor_info["bio"]
# 		if "image" in investor_info:
# 			form.image.data = investor_info["image"]
# 		return render_template('account_investor.html', update = if_update, message = message, info = investor_info, form = form, logged_in=current_user.is_authenticated, dashboard=True)
# 	elif current_user.role == "admin":
# 		form = InvestorAccountForm()
# 		if request.method == 'POST':
# 			action = request.args.get('action')
# 			updates = {}
# 			if action == "password":
# 				if form.password.data and form.confirm_password.data:
# 					if form.password.data == form.confirm_password.data:
# 						hashpass = generate_password_hash(form.password.data, method='sha256')
# 						current_user.password = hashpass
# 						db.Users.find_one_and_update({"email": current_user.email}, {"$set": {"password":hashpass}})
# 			elif action == "bio":
# 				if form.bio.data:
# 					db.Internal.find_one_and_update({"email": current_user.email}, {"$set": {"bio":form.bio.data}})
# 			elif action == "image":
# 				if form.image.data:
# 					db.Internal.find_one_and_update({"email": current_user.email}, {"$set": {"image":form.image.data}})
# 		user_info = list(db.Internal.find({"email":current_user.email}))
# 		user_info = user_info[0]
# 		if "bio" in user_info:
# 			form.bio.data = user_info["bio"]
# 		if "image" in user_info:
# 			form.image.data = user_info["image"]
# 		admin_info = {}
# 		admin_info["startups"] = list(db.Startups.find({}))
# 		admin_info["investors"] = list(db.Investors.find({}))
# 		admin_info["users"] = list(db.Users.find({}))
# 		admin_info["stats"] = {}
# 		admin_info["stats"]["startup_no"] = db.Startups.find({}).count()
# 		admin_info["stats"]["investor_no"] = db.Investors.find({}).count()
# 		admin_info["stats"]["user_no"] = db.Users.find({}).count()
# 		user_info["name"] = "WILL WON'T WIN LOL"
# 		message = "HEY Y'ALL! GUESS WHAT? WILL WON'T WIN!!!!"
# 		all_users = list(db.Users.find({}))
# 		add_admin = AddAdminForm()
# 		remove_admin = RemoveAdminForm()
# 		delete_user = DeleteUserForm()
# 		return render_template('account_admin.html', delete_user = delete_user, add_admin = add_admin, remove_admin = remove_admin, all_users = all_users, update = if_update, message = message, admin_info = admin_info, info = user_info, form = form, logged_in=current_user.is_authenticated, dashboard=True)
# 	return render_template('dashboard.html', info = {"name":"N/A"}, logged_in=current_user.is_authenticated)


# @app.route('/add-admin', methods=['GET','POST'])
# @login_required
# @admin_required
# def add_admin():
#     form = AddAdminForm()
#     if request.method == 'POST':
#         if form.email.data:
#         	if db.Investors.find({'email':form.email.data}).count() > 0:
#         		db.Investors.remove({'email':form.email.data})
#         	elif db.Startups.find({'email':form.email.data}).count() > 0:
#         		db.Startups.remove({'email':form.email.data})
#         	db.Users.update_one(
#             {"email": form.email.data},
#             {
#                 "$set": {
#                     "role":"admin"
#                 }
#             })
#     return redirect(url_for('dashboard'))

# @app.route('/delete', methods=['GET','POST'])
# @login_required
# @admin_required
# def delete_user():
#     form = DeleteUserForm()
#     if request.method == 'POST':
#         if form.email.data:
#         	existing_user = User.objects(email=form.email.data).first()
#         	existing_user.is_active = False
#         	if db.Investors.find({'email':form.email.data}).count() > 0:
#         		db.Investors.remove({'email':form.email.data})
#         	elif db.Startups.find({'email':form.email.data}).count() > 0:
#         		db.Startups.remove({'email':form.email.data})
#         	if db.Users.find({'email':form.email.data}).count() > 0:
#         		db.Users.remove({'email':form.email.data})
#     return redirect(url_for('dashboard'))

# @app.route('/remove-admin', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def remove_admin():
#     form = RemoveAdminForm()
#     if request.method == 'POST':
#         if form.email.data:
#             db.Users.update_one(
#             {"email": form.email.data},
#             {
#                 "$set": {
#                     "role":"old_admin"
#                 }
#             })
#     return redirect(url_for('dashboard'))

# @app.route('/dash')
# @login_required
# def get_dashboard(role):
# 	if role == 'startup':
# 		return render_template('startup_dashboard.html', logged_in=current_user.is_authenticated, name=current_user.email)
# 	elif role == 'investor':
# 		return render_template('investor_dashboard.html', logged_in=current_user.is_authenticated, name=current_user.email)
# 	return render_template('dashboard.html', logged_in=current_user.is_authenticated, name=current_user.email)

# @app.route('/startups/<startup_id>', methods = ['GET','POST'])
# def get_startup(startup_id):
# 	if_comment = request.args.get('comment', None)
# 	comment_form = CommentForm()
# 	if if_comment == "":
# 		if_comment = True
# 	if if_comment:
# 		if request.method == 'POST':
# 			new_comment = {
# 			"name": comment_form.name.data,
# 			"email": comment_form.email.data,
# 			"text": comment_form.text.data,
# 			"timestamp": datetime.now()
# 			}
# 			db.Startups.find_one_and_update({"id": startup_id}, {"$push": {"comments":new_comment}})
# 	this_startup_info = WebStartup(startup_id).get_info()
# 	if "social" in this_startup_info:
# 		if "twitter" in this_startup_info["social"]:
# 			this_startup_info["social"]["twitter_username"] = this_startup_info["social"]["twitter"].split('/')[-1]
# 		if "pinterest" in this_startup_info["social"]:
# 			this_startup_info["social"]["pinterest_username"] = this_startup_info["social"]["pinterest"].split('/')[-1]
# 	else:
# 		this_startup_info["social"] = {}
# 	new_comments = []
# 	if "comments" in this_startup_info:
# 		for this_comment in this_startup_info["comments"]:
# 			month = this_comment["timestamp"].strftime("%B")
# 			day = this_comment["timestamp"].strftime("%d")
# 			year = this_comment["timestamp"].strftime("%Y")
# 			hour = this_comment["timestamp"].strftime("%H")
# 			minute = this_comment["timestamp"].strftime("%M")
# 			new_date = month + " " + day + ", " + year
# 			new_time = hour+":"+minute
# 			this_comment["date"] = new_date
# 			this_comment["time"] = new_time
# 			new_comments.append(this_comment)
# 		this_startup_info["comments"] = new_comments
# 	comment_form.name.data = ""
# 	comment_form.email.data = ""
# 	comment_form.text.data = ""
# 	if current_user.is_authenticated:
# 		if current_user.role == "investor":
# 			comment_form.email.data = current_user.email
# 	comment_form = CommentForm()
# 	print(datetime.now())
# 	if_investor = False
# 	investor_email = None
# 	if current_user.is_authenticated:
# 		print(current_user.role)
# 		if current_user.role == "investor":
# 			investor_email = current_user.email
# 			if_investor = True
# 	return render_template('startup.html', if_investor = if_investor, investor_email = investor_email, api_key = mlab_api_key, info = this_startup_info, comment_form = comment_form, logged_in=current_user.is_authenticated)

# @app.route('/investors/<investor_id>')
# def get_investor(investor_id):
# 	this_investor_info = WebInvestor(investor_id).get_info()
# 	if not this_investor_info:
# 		return redirect(url_for('index'))
# 	if "timestamp" in this_investor_info:
# 		this_investor_info["date"] = this_investor_info["timestamp"]
# 	return render_template('investor.html', info = this_investor_info, logged_in=current_user.is_authenticated)

# @app.route('/privacy-policy')
# def privacy_policy():
# 	return render_template('privacy_policy.html')

# @app.route('/saved')
# @login_required
# @investor_required
# def get_saved_startups():
# 	this_investor_info = WebInvestor(current_user.email).get_info()
# 	all_startups = []
# 	if "saved" in this_investor_info:
# 		for this_startup in this_investor_info["saved"]:
# 			new_startup = WebStartup(this_startup["id"]).get_info()
# 			if new_startup is not None:
# 				if "location" in new_startup:
# 					if "latitude" in new_startup["location"]:
# 						new_startup["coordinates"] = [new_startup["location"]["latitude"], new_startup["location"]["longitude"]]
# 						new_startup["location"] = new_startup["location"]["address"]
# 				all_startups.append(new_startup)
# 	else:
# 		print("what a loser")
# 	return render_template('saved.html', info=all_startups, personal_info = this_investor_info, logged_in=current_user.is_authenticated)

# def search(query, attr, list_options):
#     for p in list_options:
#         if p[attr] == query:
#             return p

# @app.route('/edit-features', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_featured_startups():
# 	if request.method == 'POST':
# 		# print(request.form.getlist('checks[]'))
# 		results = parse_multi_form(request.form)
# 		# print(results)
# 		feature_ids = []
# 		if "checks" in results:
# 			for item in results["checks"].items():
# 				feature_ids.append(item[0])
# 		current_features = list(db.Startups.find({"feature": True}))
# 		for feature in current_features:
# 			print(feature["id"])
# 			db.Startups.find_one_and_update({"id": feature["id"]}, {"$set": {"feature":False}})
# 		for new_feature_id in feature_ids:
# 			db.Startups.find_one_and_update({"id": new_feature_id}, {"$set": {"feature":True}})
# 	# current_features = ["sophiamartika", "incub8", "eaglerivercustomtshirts"]
# 	# features = list(db.Startups.find({"id": {"$in": current_features}}))
# 	features = list(db.Startups.find({"feature": True}))
# 	feature_ids = list(db.Startups.find({"feature": True},{"id":1}))
# 	feature_indexes = []
# 	for feature in features:
# 		feature["index"] = features.index(feature)
# 		if "location" in feature:
# 			if "latitude" in feature["location"]:
# 				feature["coordinates"] = [feature["location"]["latitude"], feature["location"]["longitude"]]
# 				feature["location"] = feature["location"]["address"]
# 		feature_indexes.append(features.index(feature))
# 	if len(feature_indexes):
# 		feature_indexes.pop(0)
# 	all_startups = list(db.Startups.find({"feature": {"$ne": True}}))
# 	for this_startup in all_startups:
# 		this_startup["index"] = all_startups.index(this_startup)
# 		if this_startup["id"] in feature_ids:
# 			this_startup['feature'] = True
# 		else:
# 			this_startup['feature'] = False
# 	return render_template('edit_features.html', startups = all_startups, feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)


# # @app.route('/account', methods=['GET', 'POST'])
# # @login_required
# # def edit_account():
# # 	if current_user.role == "startup":
# # 	    form = AccountForm()
# # 	    startup_info = WebStartup(current_user.email).get_info()
# # 	    print(startup_info)
# # 	    if request.method == 'POST':
# # 	    	startup_info = WebStartup(current_user.email).get_info()
# # 	    if 'social' in startup_info:
# # 	    	for x in startup_info['social']:
# # 	    		form[x].data = startup_info['social'][x]
# # 	    form.bio.data = startup_info['description']
# # 	    return render_template('account_startup.html', info = startup_info, logged_in=current_user.is_authenticated, form = form)
# # 	return render_template('account.html', info = startup_info, logged_in=current_user.is_authenticated, form = form)

# @app.route('/awards')
# def awards():
#     return render_template('awards.html', logged_in=current_user.is_authenticated)

# @app.route('/investors')
# def investors():
# 	all_investors = list(db.Investors.find({'role': 'demo'}))
# 	all_investors = all_investors + list(db.Investors.find({'$and': [{'visibility': {'$ne':'hide'}}, {'role': {'$ne':'demo'}}]}))
# 	return render_template('investors.html', is_demo = True, investors = all_investors, logged_in=current_user.is_authenticated)

# @app.route('/help')
# def help():
#     return redirect(url_for('sorry'))

# @app.route('/home')
# def get_home():
#     return redirect(url_for('index'))

# @app.route('/index')
# def get_index():
#     return redirect(url_for('index'))

# @app.route('/successes')
# def success_stories():
#     return redirect(url_for('sorry'))

# @app.route('/unsubscribe')
# def unsubscribe():
#     return redirect(url_for('sorry'))

# @app.route('/checkout')
# def checkout():
# 	amount = 500
# 	formatted_amount = amount/100
# 	return render_template('check_out.html', amount=formatted_amount, key=stripe_keys['publishable_key'], logged_in=current_user.is_authenticated)

# @app.route('/donate', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def donate():
# 	amount = 2500
# 	formatted_amount = amount/100
# 	form = DonateForm()

# 	if request.method == 'POST':
# 		# Amount in cents
# 	    amount = int(form.amount.data)*100

# 	    customer = stripe.Customer.create(
# 	        email=form.email.data,
# 	        source=request.form['stripeToken']
# 	    )

# 	    charge = stripe.Charge.create(
# 	        customer=customer.id,
# 	        amount=amount,
# 	        currency='usd',
# 	        description='INCUB8 Charge'
# 	    )
# 	    message = "Thanks for donating!"
# 	else:
# 		message = None
# 	form.amount.data = str(amount/100)
# 	if current_user.is_authenticated:
# 		form.email.data = current_user.email
# 	if message is not None:
# 		form.amount.data = ""
# 		form.email.data = ""
# 		form.message.data = ""
# 	return render_template('donate.html', form = form, message = message, amount = amount, formatted_amount=formatted_amount, key=stripe_keys['publishable_key'], logged_in=current_user.is_authenticated)

# @app.route('/charge', methods=['POST'])
# def charge():
#     # Amount in cents
#     amount = 500

#     customer = stripe.Customer.create(
#         email='customer@example.com',
#         source=request.form['stripeToken']
#     )

#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount,
#         currency='usd',
#         description='Flask Charge'
#     )

#     formatted_amount = amount/100

#     return render_template('charge.html', amount=formatted_amount, logged_in=current_user.is_authenticated)

# @app.route('/routes', methods=['GET'])
# @admin_required
# def list_routes():
#     import urllib
#     output = []
#     for rule in app.url_map.iter_rules():

#         options = {}
#         for arg in rule.arguments:
#             options[arg] = "[{0}]".format(arg)

#         methods = ','.join(rule.methods)
#         url = url_for(rule.endpoint, **options)
#         line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
#         output.append(line)
    
#     for line in sorted(output):
#         print(line)
#     return redirect(url_for('index'))

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml """
    pages = []
    # All pages registed with flask apps
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append(rule.rule)

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    # return response
    return render_template('sitemap_template.xml', pages=pages)








if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)