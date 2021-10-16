# The Devils' Advocate

The Devils' Advocate is the student-run newspaper of San Francisco University High School. As technical developer for the DA, I created a Flask-backed website to allow impactful student work to reach a greater audience as well as give editors a simpler way to aggregate and organize articles and newspaper information.

## How to Access
The DA website is currently hosted on Heroku. Please visit [da.sfuhs.org](http://da.sfuhs.org)—you can use the credentials *test@sfuhs.org* and *sfuhsda* to access.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
cd flask
python main.py
```

## Tech Stack
- Python 3.8: used for backend development
- [Flask](http://flask.pocoo.org/): employed for templating
- Firebase: used for database, with the help of pyrebase Python API wrapper
- Flask-WTF & WTForms: enabled creation of forms and easy access to form data
- Firebase-Admin: used to create admin portal to allow easy editing of website and access to certain permissions for specific editors
- Heroku: used to host web app

## License
[MIT](https://choosealicense.com/licenses/mit/)
