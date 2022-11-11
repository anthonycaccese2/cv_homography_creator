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
# 
image_label = Label(win,text=" No Images")
image_label.place(relx=0.5, rely=0.5, anchor=CENTER)
# image dimension in the window 
image_dimension_x = 1008 
image_dimension_y = 756 
# image_scale  
image_scale_x = img.shape[1]/image_dimension_x
image_scale_y = img.shape[0]/image_dimension_y
print(image_scale_x, image_scale_y)


def refresh_list():
    global list2, image_counter, l
    myList = os.listdir(path)
    if len(list2) > 0: 
        list2 = []
        for _, imgs in enumerate(myList):
            img = imgs.split(".")
            if img[1] == "jpg":
                list2.append(imgs)
        l.config(text="Image: {0}; Unprocessed: {1}".format( list2[image_counter], str(len(list2))))
    else:
        list2 = []
        for _, imgs in enumerate(myList):
            img = imgs.split(".")
            if img[1] == "jpg":
                list2.append(imgs)
        image_counter = len(list2)-1 # reset to first image
        next_image()
    print("Image list refreshed")

def to_pil(img,label,x,y,w,h):
    global canvas, image_container
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(w,h))
    # img = cv2.flip(img,1)
    image = Image.fromarray(img)
    pic = ImageTk.PhotoImage(image)
    print(pic)
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

def computeHomography(src_img, dst_img,pts_list):
    buf = 0
    pts_src = np.array(pts_list)
    pts_dst = np.array([[buf, buf],[dst_img.shape[1]-buf, buf],[dst_img.shape[1]-buf, dst_img.shape[0]-buf],[buf, dst_img.shape[0]-buf]])
    print(pts_src)
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    # Warp source image to destination based on homography
    return cv2.warpPerspective(src_img, h, (dst_img.shape[1],dst_img.shape[0]))

    
def add_point(event):
    global posList, win, resized_image
    x = event.x 
    y = event.y
    if y >15:
        if(len(posList) < 4 and len(list2) > 0):
            print(x, y)
            cv2.circle(resized_image, (x,y), 10, (255, 255, 0), -1)
            to_pil(resized_image,image_label,0,30,image_dimension_x,image_dimension_y)
            posList.append([x, y])
        else:
            print("List is full")
        
def remove_points(event):
    global posList
    posList = []
    display_current_img()
    print("Points cleared")

def display_current_img():
    global img, resized_image, image_counter, path, image_label, image_dimension_x, image_dimension_y
    img = cv2.imread(path+'\\'+list2[image_counter])
    resized_image = cv2.resize(img,(image_dimension_x,image_dimension_y))
    to_pil(img,image_label,0,30,image_dimension_x,image_dimension_y)

def generate_homography():
    global hm_img
    if len(posList) == 4:
        print("Generating Homography")
        img = cv2.imread(path+'\\'+list2[image_counter])
        # src_img = cv2.resize(img,(image_dimension_x,image_dimension_y))
        canvas_size = np.zeros((img.shape[0], img.shape[1]))
        scaled_list = []
        for point in posList: # apply scale so no resolution is lost
            scaled_list.append([point[0]*image_scale_x,point[1]*image_scale_y])
        hm_image = computeHomography(img,canvas_size,scaled_list)
        hm_img = hm_image # save homography
        resized_hm_img = cv2.resize(hm_img,(image_dimension_x,image_dimension_y)) # resize to window
        cv2.imshow('Homography Computed', resized_hm_img)
    else:
        print("Not enought points")

# def out_calculate_corners():
#     print("Detecting Corners")

def next_image():
    global image_counter, list2, image_label, path, l, posList, resized_image
    posList = []
    if len(list2) > 0:
        if image_counter < len(list2)-1:
            image_counter +=1
            print(list2[image_counter])
        else:
            image_counter = 0
            print(list2[image_counter])
        display_current_img()
        # img = cv2.imread(path+'\\'+list2[image_counter])
        # resized_image = cv2.resize(img,(image_dimension_x,image_dimension_y))
        # to_pil(img,image_label,0,30,image_dimension_x,image_dimension_y)
        l.config(text="Image: {0}; Unprocessed: {1}".format( list2[image_counter], str(len(list2))))
    else:
        l.config(text="List empty: Add images to /images/jpg, click refresh")
        
def prev_image():
    global image_counter, image_label, path, l, posList, resized_image
    posList = []
    if len(list2) > 0:
        if image_counter > 0:
            image_counter -=1
            print(list2[image_counter])
        else:
            image_counter = len(list2)-1
            print(list2[image_counter])
        display_current_img()
        # img = cv2.imread(path+'\\'+list2[image_counter])
        # resized_image = cv2.resize(img,(image_dimension_x,image_dimension_y))
        # to_pil(img,image_label,0,30,image_dimension_x,image_dimension_y)
        l.config(text="Image: {0}; Unprocessed: {1}".format( list2[image_counter], str(len(list2))))
    else:
        l.config(text="List empty: Add images to /images/jpg, click refresh")

def save_homography(): # doesn't work
    global hm_img, list2, image_counter, resized_image, img, posList
    print(hm_img.shape[0])
    if hm_img.shape[0] == 0:
        print("Homography not generated")
        if len(posList) == 4:
            generate_homography()
            save_homography()
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
            # grey = cv2.rectangle(hm_img, (0,0), (image_dimension_x,image_dimension_y), (100,100,100), -1)
            # to_pil(grey,image_label,0,30,image_dimension_x,image_dimension_y)
            image_label.config(image='')
            l.config(text="All homographys have been computed")
            list2 = []
            resized_image = None
        else:
            list2.pop(image_counter)
            img = cv2.imread(path+'\\'+list2[image_counter])
            resized_image = cv2.resize(img,(image_dimension_x,image_dimension_y))
            to_pil(img,image_label,0,30,image_dimension_x,image_dimension_y)
            l.config(text="Image: {0}; Unprocessed: {1}".format( list2[image_counter], str(len(list2))))
        posList = []
        hm_img = np.zeros((0,0)) #clear homography


prev_btn = Button(win, text=" < ", command=prev_image, bg='white')
prev_btn.pack(side="left", fill="none", expand="no", padx="10", pady="0")

next_btn = Button(win, text=" > ", command=next_image, bg='white')
next_btn.pack(side="right", fill="none", expand="no", padx="10", pady="0")

homography_btn = Button(win, text="Generate Homography", command=generate_homography, bg='white')
homography_btn.pack(side="bottom", fill="none", expand="no", padx="10", pady="10")


# Create label for title
l = Label(win, text = "Image: {0}; Unprocessed: {1}".format( list2[image_counter], str(len(list2))))
l.config(font =("Courier", 14))
l.pack()

save_btn = Button(win, text="Save", command=save_homography, bg='white')
save_btn.place(relx=0.01, rely=0.005, anchor=NW)

refresh_btn = Button(win, text="Refresh", command=refresh_list, bg='white')
refresh_btn.place(relx=0.99, rely=0.005, anchor=NE)

win.bind("<Button 1>", add_point)
win.bind("<BackSpace>", remove_points)

display_current_img()

win.mainloop()