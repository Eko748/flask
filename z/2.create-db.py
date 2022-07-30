import mysql.connector

conn=mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = ''
)

myconn = conn.cursor()
myconn.execute(" CREATE DATABASE python")

print("nama db berhasil dibuat")
    