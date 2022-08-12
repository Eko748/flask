from re import S
from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="belajarflask_db"
)
mycursor = mydb.cursor()


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'cbn'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='belajarflask_db'
mysql = MySQL(app)

jwt = JWTManager(app)

from app.model import user, dosen, mahasiswa, gambar
from app import routes