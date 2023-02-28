# cv_homography_creator
 
This Python script allows the user to select four points on an image, and computes the homography for that image using OpenCV. The homography is then displayed in a separate window.

The script opens a window where the user can load a folder containing JPEG images. The images are loaded from the folder and displayed in the window.

To select points, the user clicks on the displayed image. The selected points are then used to compute the homography.

##The script uses the following libraries:

* cv2
* numpy
* os
* subprocess
* matplotlib
* tkinter
* PIL

To run the script, simply execute it in a Python environment.

Note: The code is currently set up to work with images in a folder called 'images' located in the same directory as the script. If you wish to use a different folder, simply modify the path variable to point to the folder you wish to use. There is also a write up on how to use this program in greater detail called Homography_guide_OPENCV.pdf. 
