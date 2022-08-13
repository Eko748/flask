from flask_jwt_extended import *
from app import app, response
from flask import request
from app.controller.auth import LoginController
from app.controller.face_recognition import FaceRecognitionController
from app.controller.api import DosenController, UserController
from flask_jwt_extended import current_user, get_jwt_identity
from flask_jwt_extended import jwt_required

# To Do List
@app.route('/')
def wellcome():
    return 'Halo'

# LoginController
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


# FaceRecognitionController
@app.route('/person')
def persons():
    return FaceRecognitionController.person()

@app.route('/train_classifier/<nbr>')
def train_classifiers(nbr):
    return FaceRecognitionController.train_classifier(nbr)
 
@app.route('/add-person')
def add_persons():
    return FaceRecognitionController.add_person()

@app.route('/add-person-submit', methods=['POST'])
def add_person_submits():
    return FaceRecognitionController.add_person_submit()

@app.route('/video-feed')
def video_feeds():
    return FaceRecognitionController.video_feed()

@app.route('/video-feed-dataset/<nbr>')
def video_feed_datasets(nbr):
    return FaceRecognitionController.video_feed_dataset(nbr)

@app.route('/vf-dataset-page/<prs>')
def video_feed_dataset_pages(prs):
    return FaceRecognitionController.video_feed_dataset_page(prs)

@app.route('/frame-page')
def frame_pages():
    return FaceRecognitionController.frame_page()




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
