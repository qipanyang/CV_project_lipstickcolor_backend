import pyrebase
import time
import cropface
import fetch
config = {
    "apiKey": "AIzaSyAZ3cTlTuVh6M3k8JXVa2Z52ouIz-fsY1g",
    "authDomain": "camera-798b0.firebaseio.com/",
    "databaseURL": "https://camera-798b0.firebaseio.com/",
    "projectId": "camera-798b0",
    "storageBucket": "camera-798b0.appspot.com",
    "appId": "1:1000635454383:ios:c6a67c463f9d1e70ae555a"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
def stream_handler(message):
    print("something is changed")
    print(message)
    time.sleep(3)
    fetch.fetch_img(message["data"])
    dic, num_face = cropface.cropface("face/original.jpg")
    fetch.send_imgs(num_face)
    db.child('selected').update(dic)

my_stream =db.child('change').stream(stream_handler)

while True:
    data = input("[{}] Type exit to disconnect: ".format('?'))
    if data.strip().lower() == 'exit':
        print('Stop Stream Handler')
        if my_stream: my_stream.close()
        break
