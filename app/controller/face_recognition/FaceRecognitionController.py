import os
import numpy as np
import cv2
from PIL import Image
from app import mycursor, mydb
from flask import Response, redirect, request, render_template, url_for, flash, session
from app.face_recognition import face_recognition, generate_dataset

def person():
    mycursor.execute("select prs_nbr, prs_name, prs_skill, prs_active, prs_added from prs_mstr")
    data = mycursor.fetchall()
    return render_template('admin/pages/face_recognition/person.html', data=data)

def add_person():
    mycursor.execute("select ifnull(max(prs_nbr) + 1, 101) from prs_mstr")
    row = mycursor.fetchone()
    nbr = row[0]
    # print(int(nbr))
    if 'loggedin' in session:
        return render_template('admin/pages/face_recognition/add_person.html', newnbr=int(nbr)) 
    flash('Harap Login dulu','danger')
    return redirect(url_for('logins'))

def add_person_submit():
    prsnbr = request.form.get('txtnbr')
    prsname = request.form.get('txtname')
    prsskill = request.form.get('optskill')
 
    mycursor.execute("""INSERT INTO `prs_mstr` (`prs_nbr`, `prs_name`, `prs_skill`) VALUES
                    ('{}', '{}', '{}')""".format(prsnbr, prsname, prsskill))
    mydb.commit()
 
    return redirect(url_for('video_feed_dataset_pages', prs=prsnbr))

def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_feed_dataset(nbr):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_feed_dataset_page(prs):
    return render_template('admin/pages/face_recognition/gendataset.html', prs=prs)

def frame_page():
    return render_template('admin/pages/face_recognition/frame_page.html')

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
 
    return redirect('/frame-page')