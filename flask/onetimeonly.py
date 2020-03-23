import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from authors import author_info
from data import all_articles

cred = credentials.Certificate("firebase-private-key.json")

firebase_admin.initialize_app(cred, {
  'projectId': "uhs-devils-advocate",
  'databaseURL': 'https://uhs-devils-advocate.firebaseio.com'
})

ref = db.reference("/")

# users_ref = ref.child('authors')
# users_ref.set(author_info)

# users_ref = ref.child('archive')
# users_ref.set(archive)

users_ref = ref.child('articles')
users_ref.set(all_articles)