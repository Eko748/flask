from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import mysql
from werkzeug.security import check_password_hash, generate_password_hash

def menu():
    if 'loggedin' in session:
        return render_template('menu.html')
    flash('Harap Login dulu','danger')
    return redirect(url_for('logins'))

#registrasi
def registrasi():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        level = request.form['level']

        #cek username atau email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s OR email=%s',(username, email, ))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s)', (username, email, generate_password_hash(password), level))
            mysql.connection.commit()
            flash('Registrasi Berhasil','success')
        else :
            flash('Username atau email sudah ada','danger')
    return render_template('registrasi.html')

#login
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        #cek data username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email=%s',(email, ))
        akun = cursor.fetchone()
        if akun is None:
            flash('Login Gagal, Cek Username Anda','danger')
        elif not check_password_hash(akun[3], password):
            flash('Login gagal, Cek Password Anda', 'danger')
        else:
            session['loggedin'] = True
            session['username'] = akun[1]
            session['level'] = akun[4]
            return redirect(url_for('addprsn', session))
    return render_template('login.html', session)

#logout
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('level', None)
    return redirect(url_for('logins'))