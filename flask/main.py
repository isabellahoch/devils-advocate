from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from credentials import FIREBASE_API_KEY
from flask import request
import os
import json

app = Flask(__name__)

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