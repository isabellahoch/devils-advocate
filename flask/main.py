from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask import request
import os
import json
from forms import SubscribeForm
from flask_compress import Compress
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'application/json']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

app.config['SECRET_KEY'] = os.urandom(24)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore

# grab credentials from json file
cred = credentials.Certificate("firebase-private-key.json")


firebase_admin.initialize_app(cred, {
  'projectId': "uhs-devils-advocate",
  'databaseURL': 'https://uhs-devils-advocate.firebaseio.com'
})

import pyrebase # allows us to work with firebase in python more easily!

config = {
  "apiKey": "AIzaSyARCliKyACLYhK_1qlK8a3IUSvQ4Do_3Jc",
  "authDomain": "uhs-devils-advocate.firebaseapp.com",
  "databaseURL": "https://uhs-devils-advocate.firebaseio.com",
  "storageBucket": "uhs-devils-advocate.appspot.com",
}

# temporarily exposing apiKey so that next editors have access to it, in future will transition to using more secure environment variables instead

firebase = pyrebase.initialize_app(config)
dbp = firebase.database()

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

# adding an admin section for editors-in-chief to be able to edit and manage articles!
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from forms import LoginForm
from creds import ACCESS_CODE
login = LoginManager(app)
login.login_view = 'login'

from flask_sqlalchemy import SQLAlchemy

sql_db = SQLAlchemy()

sql_db.init_app(app)

class User(sql_db.Model):
    """An admin user capable of viewing reports.

    :param str email: UHS email address of user

    """
    __tablename__ = 'user'

    email = sql_db.Column(sql_db.String, primary_key=True)
    authenticated = sql_db.Column(sql_db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    sql_db.create_all()
    alert = request.args.get('alert')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        next_url = request.args.get("next")
        if form.password.data != ACCESS_CODE:
            alert='Invalid access code. Please try again or contact UHS administration for help.'
            return redirect(url_for('login', alert=alert))
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(email=form.email.data)
            sql_db.session.add(user)
            sql_db.session.commit()
            login_user(user, remember=True)
        else:
            login_user(user, remember=True)
        if next_url:
            return redirect(next_url)
        return redirect(url_for('index'))
    if alert:
        return render_template('login.html', form=form, data = get_info(), if_alert = True, alert = alert)
    return render_template('login.html', form=form, data = get_info())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@cache.cached(timeout=50, key_prefix='all_info')
def get_info():
    info = {}
    ref = db.reference('/sections')
    snapshot = ref.get()
    info["sections"] = {}
    for (key,val) in snapshot.items():
         info["sections"][key] = val
    info["archive"] = [{"name": "March 2021", "id": "march-2021"},{"name":"October 2020","id":"october-2020"},{"name":"September 2020","id":"september-2020"},{"name":"February 2020","id":"february-2020"},{"name":"November 2019","id":"november-2019"}]
    return info

def get_senior_wills_info():
    sh = gc.open("Senior Wills! (Responses)")
    wk = sh.sheet1
    senior_wills_info_old = wk.get_all_values().pop(0).pop(0)
    senior_wills_info_old = wk.get_all_records()
    senior_wills_info = {}
    count = 0
    for this_will in senior_wills_info_old:
        # put this code in a try catch block in case editors formatted the data incorrectly/unexpectedly in the database
        try:
            will_id = this_will["name"].lower().replace(" ","-")
            senior_wills_info[will_id] = {}
            senior_wills_info[will_id]["index"] = count
            senior_wills_info[will_id]["cause_of_death"] = this_will["senior will - cause of death (optional, but encouraged)"]
            senior_wills_info[will_id]["id"] = will_id
            senior_wills_info[will_id]["name"] = this_will["name"]
            senior_wills_info[will_id]["email"] = this_will["Email Address"]
            if this_will["freshmen"]:
                senior_wills_info[will_id]["freshmen"] = this_will["freshmen"].split("\n")
            if this_will["sophomores"]:
                senior_wills_info[will_id]["sophomores"] = this_will["sophomores"].split("\n")
            if this_will["juniors"]:
                senior_wills_info[will_id]["juniors"] = this_will["juniors"].split("\n")
            if this_will["faculty"]:
                senior_wills_info[will_id]["faculty"] = this_will["faculty"].split("\n")
            count = count + 1
        except Exception as e:
            print(e)
    return senior_wills_info

def get_article_info(article_id):
    article = db.reference('/articles').child(article_id).get()
    article["authors"] = get_author_info(article["authors"])
    article["comments"] = get_comments(article_id)
    article["all_comments"] = db.reference('/comments').get()
    article["author"] = article["authors"][0]
    if "img" in article:
        if "drive.google.com/open" in article["img"]:
            article["img"] = "https://drive.google.com/uc?export=view&id="+article["img"].split("le.com/open?id=")[1]
    return article

def get_comments(article_id):
    comment_info = db.reference('/comments').child(article_id).get()
    if comment_info:
        return comment_info
    return []

def get_author_info(author_list):
    authors = []
    for author_id in author_list:
        author_info = db.reference('/authors').child(author_id).get()
        if author_info:
            if "img" in author_info:
                author_info["img"] = author_info["img"]
            else:
                author_info["img"] = "/static/img/authors/"+author_info["name"]+".png"
        else:
            author_info = {}
            author_info["img"] = "/static/img/authors/anonymous.png"
            author_info["name"] = author_id.title().replace("-"," ")
            author_info["id"] = author_id
        authors.append(author_info)
    return authors

def get_featured_articles():
    snapshot = db.reference('/articles').order_by_child('featured').equal_to(True).get()
    if snapshot:
        features = []
        for key, val in snapshot.items():
            article = val
            article["authors"] = get_author_info(article["authors"])
            article["author"] = article["authors"][0]
            if "img" in article:
                if "drive.google.com/open" in article["img"]:
                    article["img"] = "https://drive.google.com/uc?export=view&id="+article["img"].split("le.com/open?id=")[1]
            features.append(article)
        return features
    else:
        return None

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

latest_edition = "march-2021"

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
@login_required
@cache.cached(timeout=50)
def index():
    info = {}
    info["features"] = get_featured_articles()
    return render_template('index.html', if_notification = False, notification = {"message":"The SENIOR WILLS are out in the latest edition!", "link":"/latest"}, info = info, data = get_info())

@app.route('/authors')
@login_required
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
        if author["role"] == "Editor in Chief":
            info["sections"]["EICs"]["editors"].append(author)
        else:
            try:
                info["sections"][author["role"].split(" Editor")[0]]["editors"].append(author)
            except Exception as e:
                print(e)
    return render_template('authors.html', info = info, all_authors = all_authors, data = get_info())

@app.route('/articles')
@login_required
def articles():
    ref = db.reference('/articles')
    snapshot = ref.get()
    all_articles = []
    for key, val in snapshot.items():
         all_articles.append(val)
    return render_template('index.html', data = get_info())

@app.route('/latest')
@login_required
def latest():
    return redirect(url_for("get_edition", edition_id = latest_edition))

@app.route('/authors/<author_id>')
@login_required
def get_author(author_id):
    author_info = db.reference('/authors').child(author_id).get()
    snapshot = db.reference('/articles').order_by_child('author').equal_to(author_id).get()
    if snapshot:
        author_info["articles"] = []
        for key, val in snapshot.items():
            author_info["articles"].append(val)
    return render_template('author.html', author = author_info, data = get_info())

@app.route('/sections/<section_id>')
@login_required
def get_section(section_id):
    section_info = {}
    snapshot = db.reference('/sections').child(section_id).get()
    for key, val in snapshot.items():
        section_info[key] = val
    snapshot = db.reference('/articles').order_by_child('section').equal_to(section_id).get()
    if snapshot:
        section_info["articles"] = []
        for key, val in snapshot.items():
            article_info = val
            if article_info["edition"] == latest_edition:
                if "img" in article_info:
                    if "drive.google.com/open" in article_info["img"]:
                        article_info["img"] = "https://drive.google.com/uc?export=view&id="+article_info["img"].split("le.com/open?id=")[1]
                article_info["authors"] = get_author_info(article_info["authors"])
                section_info["articles"].append(article_info)
    return render_template('column.html', info = section_info, data = get_info())

@app.route('/articles/<article_id>')
@login_required
def get_article(article_id):
    article_info = get_article_info(article_id)
    article_info["features"] = get_featured_articles()
    if current_user.is_authenticated:
        user_email = current_user.get_id()
    else:
        user_email = "test@sfuhs.org"
    return render_template('article_comments.html', info = article_info, data = get_info(), current_user = user_email)

@app.route('/archive/<archive_id>')
@login_required
def get_archive(archive_id):
    if archive_id == "september-2020":
        return redirect(url_for('get_edition',edition_id = archive_id))
    archive_info = db.reference('/archive').child(archive_id).get()
    return render_template('archive.html', info = archive_info, data = get_info())

@app.route('/editions/<edition_id>')
@login_required
def get_edition(edition_id):
    if(edition_id == "february-2020"):
        return redirect(url_for("get_archive", archive_id = edition_id))
    elif(edition_id == "2020-senior-wills"):
        return redirect(url_for("senior_wills_2020"))
    edition_info = {"title":edition_id.replace("-"," ").title(),"id":edition_id,"date":edition_id.replace("-"," ").title()}
    edition_info["sections"] = {}
    for section in get_info()["sections"].values():
        if section["name"]=="A&E":
            section["name"] = "Arts & Entertainment"
        elif section["name"]=="Backpage":
            section["name"] = "Back Page"
        edition_info["sections"][section["id"]] = {"title":section["name"],"articles":[]}
    edition_info["features"] = []
    snapshot = db.reference('/articles').order_by_child('edition').equal_to(edition_id).get()
    if snapshot:
        edition_info["articles"] = []
        for key, val in snapshot.items():
            this_article_info = val
            this_article_info["author_info"] = db.reference('/authors').child(this_article_info["author"]).get()
            if this_article_info["author_info"]:
                this_article_info["author"] = this_article_info["author_info"]
            else:
                if this_article_info["author"]:
                    this_article_info["author"] = {"name":this_article_info["author"].replace("-"," ").title(),"role":"Contributing Writer","id":this_article_info["author"]}
                else:
                    this_article_info["author"] = {"name":"Anonymous","role":"Contributing Writer","id":"anonymous"}
            edition_info["sections"][this_article_info["section"]]["articles"].append(this_article_info)
            if "featured" in this_article_info:
                if this_article_info["featured"] == True:
                    this_article_info["index"] = len(edition_info["features"])
                    edition_info["features"].append(this_article_info)
    return render_template('edition.html', info = edition_info, data = get_info())

@app.route('/2020-senior-wills')
@login_required
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

# quick update to add senior wills for this year!

import gspread
gc = gspread.service_account(filename='service_account.json')

@app.route('/2021-senior-wills')
def senior_wills_2021():
    senior_wills_info = get_senior_wills_info()
    return render_template('senior_wills.html', info = senior_wills_info, data = get_info())

@app.route('/formatted-senior-wills')
def senior_wills_2021_formatted():
    senior_wills_info = get_senior_wills_info()
    return render_template('formatted_senior_wills.html', info = senior_wills_info, data = get_info())

@app.route('/2021-senior-wills/<senior_will_id>')
def get_senior_will(senior_will_id):
    senior_will_info = get_senior_wills_info()
    senior_will_info = senior_will_info[senior_will_id]
    return render_template('senior_will.html', info = senior_will_info, data = get_info())

@app.route('/youtube')
@login_required
def youtube():
    return render_template('youtube.html', data = get_info())

@app.route('/contribute')
@login_required
def contribute():
    return render_template('contribute.html', data = get_info())

@app.route('/staff')
@login_required
def staff():
    test_ref = db.reference('/authors')
    snapshot = test_ref.get()
    all_authors = []
    for key, val in snapshot.items():
        if not val["role"] == "Contributing Writer":
            all_authors.append(val)
    info = {}
    info["sections"] = {}
    for section in get_info()["sections"].values():
        if section["name"]=="A&E":
            section["name"] = "Arts & Entertainment"
        elif section["name"]=="Backpage":
            section["name"] = "Back Page"
        info["sections"][section["name"]] = {"title":section["name"],"editors":[]}
    info["EICs"] = {"title":"Editors in Chief","editors":[]}
    info["tech"] = {"title":"Technical Support","editors":[]}
    for author in all_authors:
        if "img" not in author:
            author["img"] = "/static/img/authors/"+author["name"]+".png"
        if author["role"] == "Editor in Chief":
            info["EICs"]["editors"].append(author)
        elif author["role"] == "Technical Support":
            info["tech"]["editors"].append(author)
        elif author["role"] == "Digital Editor":
            info["tech"]["editors"].append(author)
        else:
            info["sections"][author["role"].split(" Editor")[0]]["editors"].append(author)
    return render_template('staff.html', info = info, authors = all_authors, data = get_info())

@app.route('/about')
@login_required
def about():
    return render_template('about.html', data = get_info())

@app.route('/about/privacy')
@login_required
def privacy_policy():
    return render_template('privacy.html', data = get_info())

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', data = get_info())

@app.route('/crossword')
@login_required
def crossword():
    crossword_info = db.reference('/info').child("crossword").get()
    return render_template('crossword.html', crossword = crossword_info, data = get_info())

from werkzeug.datastructures import MultiDict

@app.route('/subscribe', methods=['GET','POST'])
@login_required
def subscribe():
    form = SubscribeForm(formdata=MultiDict({'email': current_user.email}))
    if request.method == 'POST':
        subscriber_info = {}
        subscriber_info["name"] = form.name.data
        subscriber_info["email"] = form.email.data
        subscriber_info["name"] = form.name.data
        subscriber_info["affiliation"] = form.affiliation.data
        ref = db.reference('subscribers')
        ref.set(subscriber_info)
        return render_template('subscribe.html', confirmation = True, form = form, data = get_info())
    return render_template('subscribe.html', form = form, data = get_info())

@app.route('/sorry')
@login_required
def sorry():
    return render_template('under_construction.html', data = get_info())

@app.route('/internal_search/<query>')
def internal_search(query):
    snapshot = db.reference("/articles").order_by_child("title").start_at(query.title()).end_at(query.title()+"\uf8ff").get()
    if snapshot:
        articles = []
        for key, val in snapshot.items():
            article = val
            article["authors"] = get_author_info(article["authors"])
            article["author"] = article["authors"][0]
            if "img" in article:
                if "drive.google.com/open" in article["img"]:
                    article["img"] = "https://drive.google.com/uc?export=view&id="+article["img"].split("le.com/open?id=")[1]
            articles.append(article)
            if_articles = True
    else:
        articles = None
        if_articles = False
    return render_template('internal_search.html', info = articles, if_articles = if_articles)

@app.route('/search')
@login_required
def search():
    snapshot = db.reference('/articles').get()
    articles = []
    if snapshot:
        for key, val in snapshot.items():
            article = val
            article["authors"] = get_author_info(article["authors"])
            article["author"] = article["authors"][0]
            if "img" in article:
                if "drive.google.com/open" in article["img"]:
                    article["img"] = "https://drive.google.com/uc?export=view&id="+article["img"].split("le.com/open?id=")[1]
            articles.append(article)
    return render_template('search.html', data = get_info(), info = articles)

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
    sql_db.init_app(app)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
