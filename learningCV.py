import cv2
import numpy as np
import os, subprocess
import matplotlib.pyplot as plt
from tkinter import*
from PIL import Image, ImageTk

# Get all images
path = os.getcwd()+'\images\jpg'
myList = os.listdir(path)
list2 = []
for _, imgs in enumerate(myList):
    img = imgs.split(".")
    if img[1] == "jpg":
        list2.append(imgs)
        print(imgs)
# Images
directory = path+'\\'+list2[0]
posList = []
img = cv2.imread(directory)
resized_image = img
hm_img = np.zeros((0,0)) # homography image
image_counter = 0

# Windows
win = Tk()
win.geometry("1008x786")
label_1 = Label(win,text="This is a label")

def to_pil(img,label,x,y,w,h):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(w,h))
    # img = cv2.flip(img,1)
    image = Image.fromarray(img)
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.place(x=x, y=y)

# directory = os.getcwd()+'\images\jpg'+'\IMG_7595.jpg'

def resizeImage(image, scale):
    scale_percent = scale # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    
    # resize image
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def computeHomography(src_img, dst_img):
    buf = 0
    pts_src = np.array(posList)
    pts_dst = np.array([[buf, buf],[dst_img.shape[1]-buf, buf],[dst_img.shape[1]-buf, dst_img.shape[0]-buf],[buf, dst_img.shape[0]-buf]])
    print(pts_src)
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    # Warp source image to destination based on homography
    return cv2.warpPerspective(src_img, h, (dst_img.shape[1],dst_img.shape[0]))

# def click_event(event, x, y, flags, params):
#     global posList, resized_image
#     # checking for left mouse clicks
#     if event == cv2.EVENT_LBUTTONDOWN:
 
#         # displaying the coordinates
#         # on the Shell
#         # resized_image = resizeImage(img, 30)
#         if (len(posList)<4):
#             print(x, ' ', y)
#             cv2.circle(resized_image,(x,y),20,(255,0,0),-1)
#             posList.append([x,y])
#                 # font = cv2.FONT_HERSHEY_SIMPLEX
#                 # cv2.putText(img, str(x) + ',' +
#                 #             str(y), (x,y), font,
#                 #             1, (255, 0, 0), 2)
#             cv2.imshow('image', resized_image)
#         else:
#             print("You've hit 4 points")
#             print("Use right mouse if you want to remove")
 
#     # checking for right mouse clicks    
#     if event==cv2.EVENT_RBUTTONDOWN:
 
#         # displaying the coordinates
#         # on the Shell
#         print(x, ' ', y)
#         posList = []
#         resized_image = resizeImage(img, 30)
#         print("Points cleared")
#         cv2.imshow('image', resized_image)
    
def add_point(eventAddPoint):
    global posList, win, resized_image
    x = eventAddPoint.x 
    y = eventAddPoint.y
    if y >15:
        if(len(posList) < 4):
            print(x, y)
            cv2.circle(resized_image, (x,y), 10, (255, 255, 0), -1)
            to_pil(resized_image,label_1,0,30,1008,756)
            posList.append([x, y])
        else:
            print("List is full")
        


def generate_homography():
    global hm_img
    if len(posList) == 4:
        print("Generating Homography")
        img = cv2.imread(path+'\\'+list2[image_counter])
        src_img = cv2.resize(img,(1008,756))
        canvas_size = np.zeros((src_img.shape[0], src_img.shape[1]))
        hm_image = computeHomography(src_img,canvas_size)
        hm_img = hm_image
        cv2.imshow('Homography Computed', hm_img)
    else:
        print("Not enought points")

# def out_calculate_corners():
#     print("Detecting Corners")

def next_image():
    global image_counter, list2, label_1, path, l, posList, resized_image
    posList = []
    if image_counter < len(list2)-1:
        image_counter +=1
        print(list2[image_counter])
    else:
        image_counter = 0
        print(list2[image_counter])
    img = cv2.imread(path+'\\'+list2[image_counter])
    resized_image = cv2.resize(img,(1008,756))
    to_pil(img,label_1,0,30,1008,756)
    l.config(text="Image: "+list2[image_counter])
        
def prev_image():
    global image_counter, label_1, path, l, posList, resized_image
    posList = []
    if image_counter > 0:
        image_counter -=1
        print(list2[image_counter])
    else:
        image_counter = len(list2)-1
        print(list2[image_counter])
    img = cv2.imread(path+'\\'+list2[image_counter])
    resized_image = cv2.resize(img,(1008,756))
    to_pil(img,label_1,0,30,1008,756)
    l.config(text="Image: "+list2[image_counter])

def save_homography(): # doesn't work
    global hm_img, list2, image_counter, resized_image, img, posList
    print(hm_img.shape[0])
    if hm_img.shape[0] == 0:
        print("Homography not generated")
        if len(posList) == 4:
            generate_homography()
        else: 
            print("Not enough points")
    else:
        print("Saving")
        cv2.imwrite("images\outputs\Homography_"+list2[image_counter],hm_img)
        # remove this image from list or mark as finished 
        # next_image()
        if len(list2) <= 1:
            print("end of list no more images")
            # canvas_size = np.zeros((hm_img.shape[0], hm_img.shape[1]))
            # mat = cv2.Mat((1008,756))
            # to_pil(mat,label_1,0,30,1008,756)
        else:
            list2.pop(image_counter)
        posList = []
        img = cv2.imread(path+'\\'+list2[image_counter])
        resized_image = cv2.resize(img,(1008,756))
        to_pil(img,label_1,0,30,1008,756)
        l.config(text="Image: "+list2[image_counter])
        hm_img = np.zeros((0,0)) #clear homography

# Create label
l = Label(win, text = "Image: "+list2[image_counter])
l.config(font =("Courier", 14))
l.pack()

prev_btn = Button(win, text=" < ", command=prev_image)
prev_btn.pack(side="left", fill="none", expand="no", padx="10", pady="0")

next_btn = Button(win, text=" > ", command=next_image)
next_btn.pack(side="right", fill="none", expand="no", padx="10", pady="0")

homography_btn = Button(win, text="Generate Homography", command=generate_homography)
homography_btn.pack(side="bottom", fill="none", expand="no", padx="10", pady="10")

homography_btn = Button(win, text="Save", command=save_homography)
homography_btn.place(x=10, y=4)

win.bind("<Button 1>", add_point)

resized_image = cv2.resize(img,(1008,756))
to_pil(img,label_1,0,30,1008,756)

win.mainloop()

# driver function
# if __name__=="__main__":
#     # resize image
#     resized_image = resizeImage(img, 30)
#     # img = resized
#     quitState = False
#     # cv2.createButton("button6",generate_homography, None, cv2.QT_PUSH_BUTTON,1)
#     cv2.namedWindow('image')
#     cv2.createTrackbar('R','image',0,255,generate_homography)    
#     # cv2.createButton("homo", generate_homography, None, cv2.QT_PUSH_BUTTON, 1)
#     while(not quitState):
#         # displaying the image
#         cv2.imshow('image', resized_image)
        
#         # setting mouse handler for the image
#         # and calling the click_event() function
#         cv2.setMouseCallback('image', click_event)
#         alpha = 1.75 # Contrast control (1.0-3.0)
#         beta = 0 # Brightness control (0-100)
#         # adjusted = cv2.convertScaleAbs(resized_image, alpha=alpha, beta=beta)
#         adjusted = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
#         adjusted = cv2.convertScaleAbs(adjusted, alpha=alpha, beta=beta)
#         gray = cv2.cvtColor(adjusted,cv2.COLOR_BGR2GRAY)
        
#         # gray = np.float32(gray)
#         N_best_Corners = 4
#         qualityLevel = 0.05
#         min_Distance = 375 # x1, y1 x2, y2 -- sqrt(x2-x1^2)

#         corners = cv2.goodFeaturesToTrack(gray, N_best_Corners, qualityLevel, min_Distance) #corner detector
#         corners = np.int0(corners)
#         for corner in corners:
#             x, y = corner.ravel() # flattens an array [[[][]]] -> []
#             cv2.circle(resized_image, (x,y), 10, (255, 255, 0), -1)
#         #result is dilated for marking the corners, not important
#         # dst = cv2.dilate(dst,None)
#         # Threshold for an optimal value, it may vary depending on the image.
#         # resized_image[dst>0.01*dst.max()]=[0,0,255]
#         cv2.imshow('adjust',adjusted)
#         cv2.imshow('resized',resized_image)
#         cv2.imshow('dst',gray)

#         k = cv2.waitKey(0) # wait for a key to be pressed to exit
#         if k == 13:
#             print("comput homography")
#             if(len(posList) == 4):
#                 canvas_size = np.zeros((resized_image.shape[0], resized_image.shape[1]))
#                 resized_image = resizeImage(img, 30)
#                 hm_image = computeHomography(resized_image, canvas_size)
#                 cv2.imshow('computeHomography', hm_image)   
#             else: 
#                 print("Not enough points")     
#         elif k == 27:
#             quitState = True
#             cv2.destroyAllWindows()
#         else:
#             print("Thats not a command")
#             print(k)

#     cv2.destroyAllWindows()
    # close the window

