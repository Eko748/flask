from flask import request
from app import app
from app.controller import DosenController

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosensDetail(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)

    