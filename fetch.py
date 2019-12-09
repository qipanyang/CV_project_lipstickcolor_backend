import cv2 as cv
import numpy as np
from google.cloud import storage
from firebase import firebase
import os
import urllib
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
firebase = firebase.FirebaseApplication("https://camera-798b0.firebaseio.com/")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Camera-c51eccc4dd96.json"

# cred = credentials.Certificate('Camera-c51eccc4dd96.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'camera-798b0.appspot.com'
# })
# bucket = storage.bucket()

def fetch_img(filename):
    print("start fetching")
    client = storage.Client()
    bucket = client.get_bucket('camera-798b0.appspot.com')
    pathWay = 'images/'+filename+'.jpg'
    imageBlob = bucket.blob(pathWay)
    url = imageBlob.public_url
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype = np.uint8)
    img = cv.imdecode(arr, -1)
    # trans_img = cv.transpose(img)
    # img = cv.flip(trans_img, 1)
    path = "face/original.jpg"
    cv.imwrite(path, img)
    print("finish fetching")

def send_imgs(num):
    client = storage.Client()
    bucket = client.get_bucket('camera-798b0.appspot.com')
    imageBlob = bucket.blob("/")
    for i in range(num):
        print("send", i)
        face_path = "face/send"+str(i)+".jpg"
        pathWay = "images/send"+str(i)+".jpg"
        print("sending to", pathWay)
        sendimageBlob = bucket.blob(pathWay)
        sendimageBlob.upload_from_filename(face_path)
        print("send sucessfully")
# send_imgs(1)
# fetch_img("22vxch16n_200x200")