from flask import Flask, render_template, request, redirect, url_for, make_response, abort
# from credentials import FIREBASE_API_KEY
from flask import request
import os
import json


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

# db = firestore.client()




from flask_login import LoginManager


from flask_login import current_user, login_user, UserMixin

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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

class User(UserMixin):
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('dashboard', form=form, logged_in=current_user.is_authenticated))
	if request.method == 'POST':
		if form.validate():
			check_user = User.objects(email=form.email.data).first()
			if check_user:
				if check_password_hash(check_user['password'], form.password.data):
					login_user(check_user)
					return redirect(next or url_for('dashboard', form=form, logged_in=current_user.is_authenticated))
	return render_template('login.html', form=form, next=next)


def get_info():
    snapshot = db.reference('/authors').get()
    info = {}
    info["authors"] = []
    for key, val in snapshot.items():
        info["authors"].append(val)
    return info


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
    notif = {"message":"The FEBRUARY issue is out now!", "link":"/february-2020"}
    return render_template('index.html', notification = notif, data = get_info())
	# return render_template('index.html', feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)

@app.route('/authors')
def authors():
    test_ref = db.reference('/authors')
    print(test_ref.get())
    snapshot = test_ref.get()
    all_authors = []
    for key, val in snapshot.items():
         all_authors.append(val)
    return render_template('authors.html', info = all_authors, data = get_info())

@app.route('/articles')
def articles():
    ref = db.reference('/articles')
    print(ref.get())
    snapshot = ref.get()
    all_articles = []
    for key, val in snapshot.items():
         all_articles.append(val)
    return render_template('index.html', data = get_info())

@app.route('/authors/<author_id>')
def get_author(author_id):
    author_info = db.reference('/authors').child(author_id).get()
    snapshot = db.reference('/articles').order_by_child('author').equal_to(author_id).get()
    if snapshot:
        author_info["articles"] = []
        print(snapshot)
        for key, val in snapshot.items():
            author_info["articles"].append(val)
    return render_template('author.html', author = author_info, data = get_info())

@app.route('/columns/<column_id>')
def get_column(column_id):
	column_info = {"title":column_id,"id":column_id}
	return render_template('column.html', info = column_info, data = get_info())

@app.route('/articles/<article_id>')
def get_article(article_id):
    article_info = db.reference('/articles').child(article_id).get()
    article_info["author"] = db.reference('/authors').child(article_info["author"]).get()
    return render_template('article.html', info = article_info, data = get_info())

@app.route('/editions/<edition_id>')
def get_edition(edition_id):
    edition_info = {"title":edition_id,"id":edition_id,"date":"March 2020"}
    edition_info["features"] = [{"title":"Sorrel: UHS's Michelin-Starred Neighbor","id":"sorrel"}, {"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies"},{"title": "Lukas Bacho '20's Guide to College Etiquette","id":"lukas_coletiquette"}]
    edition_info["articles"] = [{"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies","author":{"name":"Eve Leupold","img":"https://previews.dropbox.com/p/thumb/AAtSmlmLIMt_5Rw4jAaAu_bQcWxfEJNqwYsRy8grIObRuOgNLLFCrZ-_V8Ck3YxZ7DmNP9MrjeAIKq4S5vIFXw8BlS9354PnNjQP2_tI2wAThcQ8P_CVwIlgendC_6yp9SrMZmSxtKwIbRvL4Gd4jJ4bRtHtxRXb676981DDagTcbzfohDjTbZNDGlH874BSB6RbmEGJzXtHsPHXRQup-60Usa8MaYXSUxBHy-za6pP-d_VT1XqmV754rx2rrOOePzcEDwMkdv8qH1p5g7RC5wXx-xHF6dTckG_na8UVC7QRRNRtoPLqx4jLzNmyug8tbViDlXIUiGeg5YWYrskS3_KJL1fDqlGf5KYuTT8Z35Ov6Q/p.jpeg?size=2048x1536&size_mode=3"}}]
    return render_template('issue.html', info = edition_info, data = get_info())

@app.route('/testinggg')
def issue():
    return render_template('issue.html', data = get_info())

@app.route('/sorry')
def sorry():
    return render_template('under_construction.html', data = get_info())

@app.route('/dashboard')
def dashboard():
    return render_template('under_construction.html', data = get_info())

from forms import EditForm

@app.route('/editor', methods=['GET', 'POST'])
def editor():
    form = EditForm()
    if form.validate():
	    print("yay")
	    print(form.title.data)
	    print(form.body.data)
    return render_template('edit.html', form=form, data = get_info())

@app.route('/test')
def test():
    test_ref = db.collection(u'test')
    docs = test_ref.stream()
    all_tests = []
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        all_tests.append(doc.to_dict())
    return render_template('test.html', info = all_tests, data = get_info())





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