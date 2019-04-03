import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import matplotlib.image as mpimg
ix,iy = -1,-1
ex,ey = -1,-1
drawing=False
red_lower=np.array([0,174,130]);red_higher = np.array([2,255,204])
brown_lower = [7,181,81] ; brown_higher = [13,255,124]
black_lower = np.array([0,0,0]); black_higher = np.array([180,255,12])
violet_lower = [163,212,52]; violet_higher = [183,232,132]
yellow_lower =[ 16,182,175]; yellow_higher = [36,202,255]
str =""
def adjust_gamma(image, gamma=1.6):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)
def draw_line(event,x,y,flags,param):
	global ix,iy,ex,ey,drawing
	if event == cv2.EVENT_LBUTTONDOWN:
		drawing=True
		ix,iy=x,y
		print(ix,iy)
	if event == cv2.EVENT_RBUTTONDOWN:
		if drawing== True:
			ex,ey=x,y
			cv2.line(img_hsv,(ix,iy),(x,y),(255,0,0),5)
			


def traverse(img_hsv):
	global str
	print(ex,ey)
	count = 0
	flag = 0
	accuracy =[0,0,0,0,0,0,0]
	for i in range(ix,ex):
		pixel=img_hsv[i,iy]
		print(red[i,iy])
		#print(pixel)
		if((red_lower[0]<=pixel[0]<=red_higher[0] or 176 <= pixel[0]<= 180 )and red_lower[1]<=pixel[1]<=red_higher[1] and red_lower[2]<= pixel[2]<=red_higher[2]):
			if(flag==1 and accuracy[1]<=1):
				continue
			# print("Red",end="")

			if count<2:
				str = str+"2"
				
			elif count ==2:
				str = str + "x100"
				
			count+=1
			flag=1
			acc=0
			accuracy[1]+=1
		elif(brown_lower[1]<=pixel[1]<=brown_higher[1] and brown_lower[0]<=pixel[0]<=brown_higher[0] and brown_lower[2]<=pixel[2]<=brown_higher[2]):
			if(flag==2 and accuracy[2]<=1):
				continue
			#print("brown",end="")
			if count<2:
				str = str+"1"
				count+=1
			elif count ==2:
				str = str + "x10"
				count+=1
			flag=2
			acc = 0
			accuracy[2]+=1
		elif(violet_lower[1]<=pixel[1]<=violet_higher[1] and violet_lower[0]<=pixel[0]<=violet_higher[0] and violet_lower[2]<=pixel[2]<=violet_higher[2]):
			if(flag==3 and accuracy[3]<=1):
				continue
			#print("violet",end="")
			if count<2:
				str = str+"7"
				
			elif count ==2:
				str = str + "x10^7"
			count+=1
			flag=3
			accuracy[3]+=1
		elif(black_lower[1]<=pixel[1]<=black_higher[1] and black_lower[0]<=pixel[0]<=black_higher[0] and black_lower[2]<=pixel[2]<=black_higher[2]):
			if(flag==4 and accuracy[4]<=1):
				continue
			#print("violet",end="")
			if count<2:
				str = str+"0"
				
			elif count ==2:
				str = str + ""
			count+=1
			flag=4
			
			accuracy[4]+=1
		elif(yellow_lower[1]<=pixel[1]<=yellow_higher[1] and yellow_lower[0]<=pixel[0]<=yellow_higher[0] and yellow_lower[2]<=pixel[2]<=yellow_higher[2]):
			if(flag==5 and accuracy[5]<=1):
				continue
			#print("violet",end="")
			if count<2:
				str = str+"4"
				
			elif count ==2:
				str = str + ""
			count+=1
			flag=5
			acc =0
			accuracy[5]+=1
		else:
			flag=-1
file_path = filedialog.askopenfilename()
img = cv2.imread(file_path)
# img=mpimg.imread('img.jfif')
kernel = np.ones((5,5), np.uint8)

image_erosion = cv2.erode(img, kernel, iterations=1)
adjusted = adjust_gamma(image_erosion)
img_hsv=cv2.cvtColor(image_erosion,cv2.COLOR_BGR2HSV)
print(img.shape)
img_hsv = cv2.resize(img_hsv,(960,640))
cv2.namedWindow('image')
black = cv2.inRange(img_hsv,black_lower,black_higher)
red = cv2.inRange(img_hsv,red_lower,red_higher)
red2 = cv2.inRange(img_hsv,np.array([176,174,130]),np.array([180,255,204]))
red = red + red2
red = cv2.GaussianBlur(red,(5,5),0)
cv2.imshow('red',red)
#cv2.imshow('img',adjusted)
cv2.setMouseCallback('image',draw_line)

while(1):
    cv2.imshow('image',img_hsv)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
    	break
traverse(img_hsv)
print(str)
# plt.imshow(image_erosion)
# plt.show()

cv2.destroyAllWindows()       