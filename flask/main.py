from flask import Flask, render_template, request, redirect, url_for, make_response, abort
# from credentials import FIREBASE_API_KEY
from flask import request
import os
import json
from forms import RegForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)


import firebase_admin
# from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
# cred = credentials.ApplicationDefault()

# added this below might be wrong teehee :()
cred = credentials.Certificate("firebase-private-key.json")


firebase_admin.initialize_app(cred, {
  'projectId': "uhs-devils-advocate",
  'databaseURL': 'https://uhs-devils-advocate.firebaseio.com'
})

import pyrebase

config = {
  "apiKey": "AIzaSyARCliKyACLYhK_1qlK8a3IUSvQ4Do_3Jc",
  "authDomain": "uhs-devils-advocate.firebaseapp.com",
  "databaseURL": "https://uhs-devils-advocate.firebaseio.com",
  "storageBucket": "uhs-devils-advocate.appspot.com",
}

firebase = pyrebase.initialize_app(config)
dbp = firebase.database()

# db = firestore.client()

from forms import LoginForm

from werkzeug.security import generate_password_hash, check_password_hash

import google.auth

try:
    credentials, project = google.auth.default(
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
except: 
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private-key.json'

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'firebase-private-key.json')

scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

def get_info():
    info = {}
    # snapshot = db.reference('/authors').get()
    # info["authors"] = []
    # for key, val in snapshot.items():
    #     if not val["role"] == "Contributing Writer":
    #         info["authors"].append(val)
    ref = db.reference('/sections')
    snapshot = ref.get()
    info["sections"] = {}
    for (key,val) in snapshot.items():
         info["sections"][key] = val
    # info["sections"] = ["Arts & Entertainment","Current Events","Food","Op-Ed","Sports","Back Page"]
    info["archive"] = [{"name":"February 2020","id":"february-2020"},{"name":"November 2019","id":"november-2019"}]
    return info

def matches_query(will, query):
    if "freshmen" in will:
        for x in will["freshmen"]:
            if query in x.lower():
                return True
    if "sophomores" in will:
        for x in will["sophomores"]:
            if query in x.lower():
                return True
    if "juniors" in will:
        for x in will["juniors"]:
            if query in x.lower():
                return True
    if "faculty" in will:
        for x in will["faculty"]:
            if query in x.lower():
                return True
    if "miscellaneous" in will:
        for x in will["miscellaneous"]:
            if query in x.lower():
                return True
    return False


@app.errorhandler(404)
def page_not_found(e):
    title = 'Not Found'
    code = '404'
    message = "We can't seem to find the page you're looking for."
    return render_template('error.html', title = title, code = code, message = message, data = get_info()), 404

@app.errorhandler(403)
def page_forbidden(e):
    title = 'Forbidden'
    code = '403'
    message = "You do not have access to this page."
    return render_template('error.html', title = title, code = code, message = message, data = get_info()), 403

@app.errorhandler(500)
def internal_server_error(e):
    title = 'Internal Server Error'
    code = '500'
    message = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
    return render_template('error.html', title = title, code = code, message = message, data = get_info()), 500

@app.route('/')
def index():
    # notif = {"message":"The SENIOR WILLS are out in the latest edition!", "link":"/latest"}
    info = {}
    info["features"] = [{"title":"Sorrel: UHS's Michelin-Starred Neighbor","id":"sorrel"}, {"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies"},{"title": "Lukas Bacho '20's Guide to College Etiquette","id":"lukas_coletiquette"}]
    info["articles"] = [{"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies","author":{"name":"Eve Leupold","img":"https://previews.dropbox.com/p/thumb/AAtSmlmLIMt_5Rw4jAaAu_bQcWxfEJNqwYsRy8grIObRuOgNLLFCrZ-_V8Ck3YxZ7DmNP9MrjeAIKq4S5vIFXw8BlS9354PnNjQP2_tI2wAThcQ8P_CVwIlgendC_6yp9SrMZmSxtKwIbRvL4Gd4jJ4bRtHtxRXb676981DDagTcbzfohDjTbZNDGlH874BSB6RbmEGJzXtHsPHXRQup-60Usa8MaYXSUxBHy-za6pP-d_VT1XqmV754rx2rrOOePzcEDwMkdv8qH1p5g7RC5wXx-xHF6dTckG_na8UVC7QRRNRtoPLqx4jLzNmyug8tbViDlXIUiGeg5YWYrskS3_KJL1fDqlGf5KYuTT8Z35Ov6Q/p.jpeg?size=2048x1536&size_mode=3"}}]
    return render_template('index.html', notification = False, info = info, data = get_info())
    # archive_info = db.reference('/archive').child("february-2020").get()
    # return render_template('archive.html', info = archive_info, data = get_info())
	# return render_template('index.html', feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)

@app.route('/authors')
def authors():
    test_ref = db.reference('/authors')
    snapshot = test_ref.get()
    all_authors = []
    for key, val in snapshot.items():
        if not val["role"] == "Contributing Writer":
            all_authors.append(val)
    info = {}
    info["sections"] = {}
    for section in get_info()["sections"]:
        info["sections"][section] = {"title":section,"editors":[]}
    info["sections"]["EICs"] = {"title":"Editors in Chief","editors":[]}
    for author in all_authors:
        print(author["role"])
        if author["role"] == "Editor in Chief":
            info["sections"]["EICs"]["editors"].append(author)
        else:
            info["sections"][author["role"].split(" Editor")[0]]["editors"].append(author)
    return render_template('authors.html', info = info, all_authors = all_authors, data = get_info())

@app.route('/articles')
def articles():
    ref = db.reference('/articles')
    snapshot = ref.get()
    all_articles = []
    for key, val in snapshot.items():
         all_articles.append(val)
    return render_template('index.html', data = get_info())

@app.route('/latest')
def latest():
    return redirect(url_for("get_edition", edition_id = "2020-senior-wills"))

@app.route('/authors/<author_id>')
def get_author(author_id):
    author_info = db.reference('/authors').child(author_id).get()
    snapshot = db.reference('/articles').order_by_child('author').equal_to(author_id).get()
    if snapshot:
        author_info["articles"] = []
        for key, val in snapshot.items():
            author_info["articles"].append(val)
    return render_template('author.html', author = author_info, data = get_info())

@app.route('/sections/<section_id>')
def get_section(section_id):
    # section_info = {"title":section_id,"id":section_id}
    section_info = {}
    snapshot = db.reference('/sections').child(section_id).get()
    for key, val in snapshot.items():
        section_info[key] = val
    snapshot = db.reference('/articles').order_by_child('section').equal_to(section_id).get()
    if snapshot:
        section_info["articles"] = []
        for key, val in snapshot.items():
            section_info["articles"].append(val)
    return render_template('column.html', info = section_info, data = get_info())

@app.route('/articles/<article_id>')
def get_article(article_id):
    article_info = db.reference('/articles').child(article_id).get()
    article_info["author"] = db.reference('/authors').child(article_info["author"]).get()
    return render_template('article.html', info = article_info, data = get_info())

@app.route('/archive/<archive_id>')
def get_archive(archive_id):
    archive_info = db.reference('/archive').child(archive_id).get()
    return render_template('archive.html', info = archive_info, data = get_info())

@app.route('/editions/<edition_id>')
def get_edition(edition_id):
    if(edition_id == "february-2020"):
        return redirect(url_for("get_archive", archive_id = edition_id))
    elif(edition_id == "2020-senior-wills"):
        return redirect(url_for("senior_wills_2020"))
    edition_info = {"title":edition_id,"id":edition_id,"date":edition_id.replace("-"," ").title()}
    edition_info["features"] = [{"title":"Sorrel: UHS's Michelin-Starred Neighbor","id":"sorrel"}, {"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies"},{"title": "Lukas Bacho '20's Guide to College Etiquette","id":"lukas_coletiquette"}]
    edition_info["articles"] = [{"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies","author":{"name":"Eve Leupold","img":"https://previews.dropbox.com/p/thumb/AAtSmlmLIMt_5Rw4jAaAu_bQcWxfEJNqwYsRy8grIObRuOgNLLFCrZ-_V8Ck3YxZ7DmNP9MrjeAIKq4S5vIFXw8BlS9354PnNjQP2_tI2wAThcQ8P_CVwIlgendC_6yp9SrMZmSxtKwIbRvL4Gd4jJ4bRtHtxRXb676981DDagTcbzfohDjTbZNDGlH874BSB6RbmEGJzXtHsPHXRQup-60Usa8MaYXSUxBHy-za6pP-d_VT1XqmV754rx2rrOOePzcEDwMkdv8qH1p5g7RC5wXx-xHF6dTckG_na8UVC7QRRNRtoPLqx4jLzNmyug8tbViDlXIUiGeg5YWYrskS3_KJL1fDqlGf5KYuTT8Z35Ov6Q/p.jpeg?size=2048x1536&size_mode=3"}}]
    return render_template('issue.html', info = edition_info, data = get_info())

@app.route('/2020-senior-wills')
def senior_wills_2020():
    query = request.args.get('query')
    senior_wills_info = db.reference('/archive').child("2020-senior-wills").child("senior-wills").order_by_key().get()
    if(query):
        query = query.lower()
        old_senior_wills_info = senior_wills_info
        senior_wills_info = {}
        for this_will in old_senior_wills_info:
            if(matches_query(old_senior_wills_info[this_will], query)):
                senior_wills_info[old_senior_wills_info[this_will]["id"]] = old_senior_wills_info[this_will]
    count = 0
    for this_will in senior_wills_info:
        senior_wills_info[this_will]["index"] = count
        count = count + 1
    return render_template('senior_wills.html', info = senior_wills_info, data = get_info())

@app.route('/2020-senior-wills/<senior_will_id>')
def get_senior_will(senior_will_id):
    senior_will_info = db.reference('/archive').child("2020-senior-wills").child("senior-wills").child(senior_will_id).get()
    return render_template('senior_will.html', info = senior_will_info, data = get_info())

@app.route('/youtube')
def youtube():
    return render_template('youtube.html', data = get_info())

@app.route('/about')
def about():
    test_ref = db.reference('/authors')
    snapshot = test_ref.get()
    all_authors = []
    for key, val in snapshot.items():
        if not val["role"] == "Contributing Writer":
            all_authors.append(val)
    info = {}
    info["sections"] = {}
    for section in get_info()["sections"]:
        info["sections"][section] = {"title":section,"editors":[]}
    info["sections"]["EICs"] = {"title":"Editors in Chief","editors":[]}
    for author in all_authors:
        if author["role"] == "Editor in Chief":
            info["sections"]["EICs"]["editors"].append(author)
        else:
            info["sections"][author["role"].split(" Editor")[0]]["editors"].append(author)
    return render_template('authors.html', info = info, authors = all_authors, data = get_info())

@app.route('/about/privacy')
def privacy_policy():
    return render_template('index.html', data = get_info())

@app.route('/crossword')
def crossword():
    return render_template('crossword.html', data = get_info())

@app.route('/sorry')
def sorry():
    return render_template('under_construction.html', data = get_info())

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







 



app.jinja_env.cache = {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)