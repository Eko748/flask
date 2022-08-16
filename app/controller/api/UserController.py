import email
import imp
from importlib.metadata import files
from os import access
from app.model.auth.users import User
from app.model.gambar import Gambar
# from flask import Response, redirect, request, render_template, url_for, flash, session
from app import response, app, db, uploadconfig
from flask import request, render_template
from flask_jwt_extended import *
from werkzeug.utils import secure_filename
import uuid
import os
import datetime

def   upload():
    try:
        judul = request.form.get('judul')
        
        if 'file' not in request.files:
            return response.badRequest([], 'File tidak tersedia')
        
        file = request.files['file']
        
        if file.filename == '':
            return response.badRequest([], 'File tidak tersedia')
        if file and uploadconfig.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            renamefile = "Flask-"+str(uid)+filename
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))
            
            uploads = Gambar(judul=judul, pathname=renamefile)
            db.session.add(uploads)
            db.session.commit()
            
            return response.success(
                {
                    'judul':judul,
                    'pathname':renamefile
                },
                "Sukses mengupload file"
            )
        else:
            return response.badRequest([], 'File tidak diizinkan')
            
    except Exception as e:
        print(e)

def buatAdmin():
    try:
        active = 1
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        
        users = User(active=active, email=email, password=password, username=username)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        
        return response.success('', 'Sukses menambahkan Data Admin!')
    except Exception as e:
        print(e)
        

def singleObject(data):
    data = {
        'id': data.id,
        'name': data.name,
        'email': data.email,
        'level': data.level
    }
    
    return data

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return response.badRequest([], 'Email tidak terdaftar')
        
        if not user.checkPassword(password):
            return response.badRequest([], 'Kombinasi Password Salah!')
        
        data = singleObject(user)
        
        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)
        
        acces_token = create_access_token(data, fresh=True, expires_delta= expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)
        
        return response.success({
            "data" : data,
            "access_token" : acces_token,
            "refresh_token" : refresh_token,
        }, "Sukses Login!")
        
    except Exception as e:
        print(e)
        
def signin():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return response.badRequest([], 'Email tidak terdaftar')
        
        if not user.checkPassword(password):
            return response.badRequest([], 'Kombinasi Password Salah!')
        
        data = singleObject(user)
        
        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)
        
        acces_token = create_access_token(data, fresh=True, expires_delta= expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)
        
        return response.success({
            "data" : data,
            "access_token" : acces_token,
            "refresh_token" : refresh_token,
        }, "Sukses Login!")
        
    except Exception as e:
        print(e)