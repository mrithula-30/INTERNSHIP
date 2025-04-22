import cv2
import numpy as np
point_count=0
point_coords=[]
def reset_image():
    global img
    img=cv2.imread('/home/sensen/Downloads/car.webp')
def ROIView(point_coords):
    cv2.namedWindow('ROI')
    mask=np.zeros_like(img)
    cv2.fillPoly(mask,[point_coords],color=(255,255,255))
    ROIimg=cv2.bitwise_and(img,mask)
    cv2.imshow('ROI',ROIimg)
def plotpoints(event,x,y,flags,param):
    global point_coords,point_count
    if event==cv2.EVENT_LBUTTONDOWN:
        point_count+=1
        point_coords.append((x,y))
        print(f"Point {point_count}: ({x},{y})")
        cv2.circle(img,(x,y),2,(255,255,255),-1)
        if point_count>1:
            for i in range(len(point_coords)-1):
                cv2.line(img,point_coords[i],point_coords[i+1],(255,255,255),2)
        if point_count>2:
            dist=(((x-point_coords[0][0])**2+(y-point_coords[0][1])**2)**0.5)
            if dist<10:
                reset_image()
                np_point_coords=np.array(point_coords[:-1],np.int32)
                np_point_coords=np_point_coords.reshape((-1,1,2))
                cv2.polylines(img,[np_point_coords],True,(255,255,255))
                ROIView(np_point_coords)
                point_coords.clear()
                point_count=0
img=cv2.imread('/home/sensen/Downloads/car.webp')
cv2.namedWindow('image')
cv2.setMouseCallback('image',plotpoints)
while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20)&0xFF==27:
        break
cv2.destroyAllWindows()
