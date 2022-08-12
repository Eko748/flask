import datetime
import os
from PIL import Image
from app.model.user import User
import numpy as np
import cv2
from flask_jwt_extended import *
from app.face_recognition import face_recognition, generate_dataset
from app import app, response, mycursor, mydb
from flask import Response, redirect, request, render_template, url_for, flash, session
from flask import jsonify
from app.controller.login import LoginController
from app.controller import DosenController
from app.controller import UserController
from flask_jwt_extended import current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, LoginManager

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
@app.route('/')
def wellcome():
    return 'Halo'

@app.route('/menu')
def menus():
    return LoginController.menu()

@app.route('/registrasi', methods=('GET','POST'))
def regis():
    return LoginController.registrasi()
 
@app.route('/login', methods=('GET', 'POST'))
def logins():
    return LoginController.login()

@app.route('/logout')
def logouts():
    return LoginController.logout()

@app.route('/person')
def home():
    mycursor.execute("select prs_nbr, prs_name, prs_skill, prs_active, prs_added from prs_mstr")
    data = mycursor.fetchall()
 
    return render_template('index.html', data=data)

# @app.route('/', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         #cek data username
#         # cursor = mydb.cursor()
#         mycursor.execute('SELECT * FROM user WHERE email=%s',(email, ))
#         akun = mycursor.fetchone()
#         if akun is None:
#             flash('Login Gagal, Cek Username Anda','danger')
#         elif not check_password_hash(akun[3], password):
#             flash('Login gagal, Cek Password Anda', 'danger')
#         else:
#             # session['loggedin'] = True
#             session['name'] = akun[1]
#             session['level'] = akun[4]
#             return redirect(url_for('index'))
#     return render_template('login.html')

# @app.route('/', methods=('GET', 'POST'))
# def signins():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         user = User.query.filter_by(email=email).first()
        
#         if not user:
#             return response.emailInvalid()
        
#         if not user.checkPassword(password):
#             return response.passwordInvalid()
        
#         # data = DosenController.singleObject(user)
        
#         expires = datetime.timedelta(days=7)
#         expires_refresh = datetime.timedelta(days=7)
        
#         # acces_token = create_access_token(fresh=True, expires_delta= expires)
#         # refresh_token = create_refresh_token(expires_delta=expires_refresh)
#         # acces_token = request
        
#         return redirect('/person')
#     else:
#         return render_template('login.html')


@app.route('/train_classifier/<nbr>')
def train_classifier(nbr):
    dataset_dir = "D:/Face/flask/dataset"
 
    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    faces = []
    ids = []
 
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
 
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)
 
    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
 
    return redirect('/')
 
@app.route('/addprsn')
def addprsn():
    mycursor.execute("select ifnull(max(prs_nbr) + 1, 101) from prs_mstr")
    row = mycursor.fetchone()
    nbr = row[0]
    # print(int(nbr))
    if 'loggedin' in session:
        return render_template('addprsn.html', newnbr=int(nbr)) 
    flash('Harap Login dulu','danger')
    return redirect(url_for('logins'))

@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    prsnbr = request.form.get('txtnbr')
    prsname = request.form.get('txtname')
    prsskill = request.form.get('optskill')
 
    mycursor.execute("""INSERT INTO `prs_mstr` (`prs_nbr`, `prs_name`, `prs_skill`) VALUES
                    ('{}', '{}', '{}')""".format(prsnbr, prsname, prsskill))
    mydb.commit()
 
    # return redirect(url_for('home'))
    return redirect(url_for('vfdataset_page', prs=prsnbr))
 
@app.route('/vfdataset_page/<prs>')
def vfdataset_page(prs):
    return render_template('gendataset.html', prs=prs)
 
@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/fr_page')
def fr_page():
    return render_template('fr_page.html')




# -------------------------------- API Routes -------------------------------- #

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses')

@app.route('/api/dosen', methods=['GET', 'POST'])
@jwt_required()
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()
    
# buat rute paging
@app.route('/api/dosen/page', methods=['GET'])
def pagination():
    return DosenController.paginate()
    
@app.route('/api/file-upload', methods=['POST'])
def uploads():
    return UserController.upload()
    
@app.route('/api/createadmin', methods=['POST'])
def admins():
    return UserController.buatAdmin()

@app.route('/api/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)
    
@app.route('/api/login', methods=['POST'])
def apilogins():
    return UserController.login()
