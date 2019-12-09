import dlib         
import numpy as np  
import cv2       
import os
import requests
import time
import json
from functools import cmp_to_key
import rgb2color
import cb
import math


def create_entry(facial_part, name_str, num):
    node_list = []
    for i in range(num):
        head_str = name_str + str(i)
        s = facial_part[head_str]
        node_list.append((s["x"], s["y"]))
	# new_entry = {"label": name_str, "line_color": None, "fill_color": None, 
	# "points": node_list, "shape_type": shape_type, "flags": {}}
    return(node_list)
def find_inside(outline):
    def foo(p1, p2):
        if p1[0]<p2[0]:
            return -1
        elif p1[0]>p2[0]:
            return 1
        else:
            if p1[1]<p2[1]:
                return -1
            else:
                return 1
        
    outline=sorted(outline, key=cmp_to_key(foo))
    # print(outline)
    l = len(outline)
    res = []
    i = 0
    while i < l-1:
        if outline[i+1][0] != outline[i][0]:
            i+=1
            continue
        current = -1
        m = -1
        while i<l-1 and outline[i+1][0] == outline[i][0]:
            if outline[i+1][1] - outline[i][1] > m and outline[i+1][1] - outline[i][1] > 10:
                current = i
                m = outline[i+1][1] - outline[i][1]
            i+=1
        i+=1
        if current != -1:
            for j in range(outline[current][1]+5, outline[current+1][1]-4):
                res.append((outline[current][0], j))
    return res



detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/dlib/shape_predictor_68_face_landmarks.dat')

http_url = 'https://api-us.faceplusplus.com/facepp/v1/face/thousandlandmark'
key = "_p0g9vLzw1mzabxwpGDikJU2aQTx-Ug2"
secret = "3J8m84Hm2f-GElMQnNEx0bgT5sfUAuE-"
data = {'api_key':key, 'api_secret':secret, 'return_landmark':'all'}
def cropface(img_path):
    img = cv2.imread(img_path)
    img = cb.white_balance(img)
    faces = detector(img, 1)
    u, v, d = img.shape
    print("faces in all:", len(faces), '\n')
    # cv2.namedWindow("res",0);
    # cv2.resizeWindow("res", 1280, 960);
    res = {}
    for num, face in enumerate(faces):              
        res["face"+str(num)] = {}      
        pos_start = (face.left(), face.top())
        pos_end = (min(face.right(), img.shape[1]), min(face.bottom(), img.shape[0]))
        height = pos_end[1]-face.top()
        width = pos_end[0]-face.left()
        img_blank = np.zeros((height, width, 3), np.uint8)
        x = face.top()
        y = face.left()
        print(img.shape)
        print(pos_start, pos_end)
        for i in range(height):
            for j in range(width):
                img_blank[i][j] = img[x+i][y+j]
        print("get face", num, "blank")
        
        face_path = "face/"+str(num)+".jpg"
        cv2.imwrite(face_path, img_blank)
        files = {'image_file': open(face_path, 'rb')}
        r = requests.post(http_url, data = data, files=files)

        savefile = "face/"+str(num)+".json"
        sfile = open(savefile, 'w')
        sfile.write(r.text)
        sfile.close()

        jfile = open(savefile, "rb")
        fileJson = json.load(jfile)
        face = fileJson["face"]
        landmark = face["landmark"]
        mouth = landmark["mouth"]
        n_lower_lip = create_entry(mouth, "lower_lip_", 64)
        n_upper_lip = create_entry(mouth, "upper_lip_", 64)
        for point in n_lower_lip:
    	    cv2.circle(img_blank, point, 1, (255,0,0), 0)
        for point in n_upper_lip:
            cv2.circle(img_blank, point, 1, (0,255,0), 0)
        send_face_path = "face/send"+str(num)+".jpg"
        cv2.imwrite(send_face_path, img_blank)

        inside_lower_lip = find_inside(n_lower_lip)
        inside_upper_lip = find_inside(n_upper_lip)

        s = 0
        c = 0
        ab = 0
        ar = 0
        ag = 0
        for point in inside_lower_lip:
            # print(img_blank[point[1]][point[0]])
            # hh=rgb2color.bgr2h(img_blank[point[1]][point[0]])#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if hh<180:
            #     hh+=360
            # print(hh)
            # s+=hh
            b,g,r = img_blank[point[1]][point[0]]
            ab += b**2
            ar += r**2
            ag += g**2 
            c+=1
        for point in inside_upper_lip:
            # print(img_blank[point[1]][point[0]])
            # hh=rgb2color.bgr2h(img_blank[point[1]][point[0]])
            # if hh<180:
            #     hh+=360
            # print(hh)
            # s+=hh
            b,g,r = img_blank[point[1]][point[0]]
            ab += b**2
            ar += r**2
            ag += g**2
            c+=1
        print("c", c)
        ave_brg = (math.sqrt(ab/c), math.sqrt(ag/c), math.sqrt(ar/c))
        # s = s/c
        # if s>360:
        #     s-=360
        nearest = rgb2color.find_color(ave_brg)
        for id, color in enumerate(nearest):
            res["face"+str(num)]["color"+str(id)] = color

            
    return res, len(faces)