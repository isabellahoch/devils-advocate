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

# db = firestore.client()



import flask_login


from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(user_email):
    user = find_user_by_email(user_email)
    if not user:
        return None
    return user

login.login_view = 'login'

users = [
    {'email':'isabella.hochschi_21@sfuhs.org', 'password': 'killerskill!', 'is_admin': True},
    {'email':'uhsstudentit@gmmail.com', 'password': 'killerskill!', 'is_admin': True}
]

def find_user_by_id(user_id):
    for _user in users:
        if _user['id'] == user_id:
            return _user
    return None

def find_user_by_username(username):
    for _user in users:
        if _user['username'] == username:
            return _user
    return None

def find_user_by_email(email):
    for _user in users:
        if _user['email'] == email:
            return _user
    return None

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
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class LoginUser(UserMixin):
#     def __init__(self, id):
#         self.id = id

#     @property
#     def username(self):
#         user = self.get_user()
#         return user['username']

#     @property
#     def is_admin(self):
#         user = self.get_user()
#         return user['is_admin']

#     def get_user(self):
#         return find_user_by_id(self.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if (current_user.is_authenticated):
        return redirect(url_for('dashboard', current_user=current_user, data = get_info()))
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        if form.errors:
            print(form.errors)
        user = find_user_by_email(email)
        if user:
            if user['password'] == password:
                user_obj = User(user)
                login_user(user_obj, remember=True)
                print(current_user.is_authenticated)
                next = request.args.get("next")
                return redirect(next or url_for('dashboard'))
    # if current_user.is_authenticated:
    #   return redirect(url_for('dashboard', form=form, logged_in=current_user.is_authenticated, data = get_info()))
    # if request.method == 'POST':
    #   if form.validate():
    #       check_user = User.get(email=form.email.data).first()
    #       if check_user:
    #           if check_password_hash(check_user['password'], form.password.data):
    #               login_user(check_user)
 #                    session.permanent = True
    #               return redirect(next or url_for('dashboard', form=form, logged_in=current_user.is_authenticated, data = get_info()))
    return render_template('login.html', form=form, data = get_info())

@app.route('/register', methods=['GET', 'POST'])
def registration():
    role = request.args.get('role', default=None, type=None)
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            print('looks like the form validated')
            # existing_user = User.objects(email=form.email.data).first()
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.email.data,hashpass).save()
                login_user(hey)
                return redirect(url_for('dashboard', form=form, logged_in=current_user.is_authenticated, data = get_info()))
        else:
            print(form.errors)
    return render_template('registration.html', form=form, next=next, data = get_info())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def get_info():
    info = {}
    # snapshot = db.reference('/authors').get()
    # info["authors"] = []
    # for key, val in snapshot.items():
    #     if not val["role"] == "Contributing Writer":
    #         info["authors"].append(val)
    info["sections"] = ["Arts & Entertainment","Current Events","Food","Op-Ed","Sports","Back Page"]
    info["archive"] = [{"name":"February 2020","id":"february-2020"},{"name":"November 2019","id":"november-2019"}]
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
    notif = {"message":"The SENIOR WILLS ARE out now!", "link":"/senior-wills"}
    info = {}
    info["features"] = [{"title":"Sorrel: UHS's Michelin-Starred Neighbor","id":"sorrel"}, {"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies"},{"title": "Lukas Bacho '20's Guide to College Etiquette","id":"lukas_coletiquette"}]
    info["articles"] = [{"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies","author":{"name":"Eve Leupold","img":"https://previews.dropbox.com/p/thumb/AAtSmlmLIMt_5Rw4jAaAu_bQcWxfEJNqwYsRy8grIObRuOgNLLFCrZ-_V8Ck3YxZ7DmNP9MrjeAIKq4S5vIFXw8BlS9354PnNjQP2_tI2wAThcQ8P_CVwIlgendC_6yp9SrMZmSxtKwIbRvL4Gd4jJ4bRtHtxRXb676981DDagTcbzfohDjTbZNDGlH874BSB6RbmEGJzXtHsPHXRQup-60Usa8MaYXSUxBHy-za6pP-d_VT1XqmV754rx2rrOOePzcEDwMkdv8qH1p5g7RC5wXx-xHF6dTckG_na8UVC7QRRNRtoPLqx4jLzNmyug8tbViDlXIUiGeg5YWYrskS3_KJL1fDqlGf5KYuTT8Z35Ov6Q/p.jpeg?size=2048x1536&size_mode=3"}}]
    return render_template('index.html', notification = notif, info = info, data = get_info())
    # archive_info = db.reference('/archive').child("february-2020").get()
    # return render_template('archive.html', info = archive_info, data = get_info())
	# return render_template('index.html', feature_no = feature_indexes, features = features, logged_in=current_user.is_authenticated)

@app.route('/authors')
def authors():
    test_ref = db.reference('/authors')
    print(test_ref.get())
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
    print(info)
    return render_template('authors.html', info = info, all_authors = all_authors, data = get_info())

@app.route('/articles')
def articles():
    ref = db.reference('/articles')
    print(ref.get())
    snapshot = ref.get()
    all_articles = []
    for key, val in snapshot.items():
         all_articles.append(val)
    return render_template('index.html', data = get_info())

@app.route('/latest')
def latest():
    return redirect(url_for("get_edition", edition_id = "february-2020"))

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

@app.route('/sections/<section_id>')
def get_section(section_id):
	section_info = {"title":section_id,"id":section_id}
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
    edition_info = {"title":edition_id,"id":edition_id,"date":edition_id.replace("-"," ").title()}
    edition_info["features"] = [{"title":"Sorrel: UHS's Michelin-Starred Neighbor","id":"sorrel"}, {"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies"},{"title": "Lukas Bacho '20's Guide to College Etiquette","id":"lukas_coletiquette"}]
    edition_info["articles"] = [{"title":"Eve Leupold '20 Breaks Down Her Favorite Holiday Movies","id":"eve_movies","author":{"name":"Eve Leupold","img":"https://previews.dropbox.com/p/thumb/AAtSmlmLIMt_5Rw4jAaAu_bQcWxfEJNqwYsRy8grIObRuOgNLLFCrZ-_V8Ck3YxZ7DmNP9MrjeAIKq4S5vIFXw8BlS9354PnNjQP2_tI2wAThcQ8P_CVwIlgendC_6yp9SrMZmSxtKwIbRvL4Gd4jJ4bRtHtxRXb676981DDagTcbzfohDjTbZNDGlH874BSB6RbmEGJzXtHsPHXRQup-60Usa8MaYXSUxBHy-za6pP-d_VT1XqmV754rx2rrOOePzcEDwMkdv8qH1p5g7RC5wXx-xHF6dTckG_na8UVC7QRRNRtoPLqx4jLzNmyug8tbViDlXIUiGeg5YWYrskS3_KJL1fDqlGf5KYuTT8Z35Ov6Q/p.jpeg?size=2048x1536&size_mode=3"}}]
    return render_template('issue.html', info = edition_info, data = get_info())

@app.route('/testinggg')
def issue():
    return render_template('issue.html', data = get_info())

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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user = current_user, data = get_info())

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