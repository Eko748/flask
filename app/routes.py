from functools import wraps
from app.model.auth.users import User
from app.model.auth.roles import Role
from flask_jwt_extended import *
from app import app, response, db
from flask import request, render_template, redirect, url_for, g, session
from app.controller.auth import LoginController
from app.controller.face_recognition import FaceRecognitionController
from app.controller.api import DosenController, UserController
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required
from flask_babelex import Babel
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


# babel = Babel(app)

@app.before_request
def user_logged_in():
    id = session.get('username')
    if id == None:
        g.user = None
    else:
        g.user='set'

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('logins'))
        return FaceRecognitionController.person()
    return wrapped_view

# To Do List
@app.route('/')
def wellcome():
    return 'Halo'

@app.route('/hai')
@roles_required
def emp():
    return 'hai employee'

@app.route('/api/roles')
def roles():
    query = Role.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Role.name_role.like(f'%{search}%'),
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['name_role']:
            col_name = 'name_role'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Role, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [roles.to_dict() for roles in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Role.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/user')
def ajax():
    return render_template('ajax_table.html', title='Ajax Table')

@app.route('/api/data')
def data():
    query = User.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['username', 'email']:
            col_name = 'username'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [users.to_dict() for users in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


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
