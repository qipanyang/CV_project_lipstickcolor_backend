import json
import numpy as np  
import cv2 
import rgb2lab
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color

jsonfile = open("realData.json","rb")
fileJson = json.load(jsonfile)
all = fileJson["brands"]
def bgr2h(p):
    R = p[2]/255.0
    G = p[1]/255.0
    B = p[0]/255.0
    large = max(R,G,B)
    small = min(R,G,B) 
    h = 0
    if R == large:
        h = (G-B)/(large-small)
    if G == large:
        h = 2 + (B-R)/(large-small)
    if B == large:
        h = 4 + (R-G)/(large-small)
    h*=60
    if h<0:
        h+=360
    return h
def dis(H,p):
    h = bgr2h(p)
    dif = abs(H-h)
    if dif > 180:
        dif = 360-dif
    return dif

def find_color(ave):
    print("average", ave)
    ave_rgb = sRGBColor(ave[2], ave[1], ave[0], 1)
    ave_lab = convert_color(ave_rgb, LabColor)
    res = []
    dist_d = {}
    # for brand in all:
    for o in range(len(all)):
        brand = all[o]
        brandname = brand["name"]
        series = brand["series"]
        l_series = len(series)
        res_sery = ""
        min_dis = 180
        
        for sery_id in range(l_series):
        # for sery_id in range(1,2):
            sery = series[sery_id]
            lipsticks = sery["lipsticks"]
            l_lipsticks = len(lipsticks)
            for colorid in range(l_lipsticks):
                color = lipsticks[colorid]["color"]
                r = int(color[1:3],16)  
                g = int(color[3:5],16)  
                b = int(color[5:7],16)
                current_rgb = sRGBColor(r, g, b, 1)
                current_lab = convert_color(current_rgb, LabColor)
                d = delta_e_cie2000(ave_lab, current_lab)
                # d = dis(H, (b,g,r))
                # print(bgr2h((b,g,r)))
                # if d<min_dis:
                #     res_color = lipsticks[colorid]
                #     res_sery = sery["name"]
                #     min_dis = d
                dist_d[str(o)+"_"+str(sery_id)+"_"+str(colorid)] = d
    sort_d = sorted(dist_d.items(), key=lambda x: x[1])
    for i in range(5):
        brand_id, sery_id, colorid = sort_d[i][0].split("_")
        print(brand_id, sery_id, colorid)
        series = all[int(brand_id)]["series"]
        res_color = series[int(sery_id)]["lipsticks"][int(colorid)]
        res_color["brand"] = all[int(brand_id)]["name"]
        res_color["series"] = series[int(sery_id)]["name"]
        res.append(res_color)
        # print((brandname, res_sery, res_color))
    return res

       

# pic_path = "shine14.jpg"
# img = cv2.imread(pic_path)
# # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# # print(imgHSV.shape)
# m = img.shape[0]
# n = img.shape[1]
# s = 0
# for i in range(m):
#     for j in range(n):
#         hh=bgr2h(img[i][j])
#         if hh<180:
#             hh+=360
#         s+=hh
# s /= m*n
# if s > 360:
#     s-=360
# print(img[15][15])
# print("s", s)
# find_color(img[10][10]) # H in opencv is in (0, 180)