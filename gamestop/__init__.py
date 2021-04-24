from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# protect from modifying cookies, cross-site request forgery attacks
app.config['SECRET_KEY'] = 'd694936a4192c385995f1a67fd2af4aa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from gamestop import routes