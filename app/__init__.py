from re import S
from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import mysql.connector

secretKey = 'cbn'
host = 'localhost'
user = 'root'
database = 'belajarflask_db'

mydb = mysql.connector.connect(
    host= host,
    user= user,
    passwd="",
    database= database
)
mycursor = mydb.cursor()


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = secretKey
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = database
mysql = MySQL(app)

jwt = JWTManager(app)

from app.model import user, dosen, mahasiswa, gambar
from app import routes