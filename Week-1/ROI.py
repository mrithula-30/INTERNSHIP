import cv2

image_path='/home/sensen/Downloads/car.webp'
image=cv2.imread(image_path)
if image is None:
    print("could not load the image ")
    exit()

roi=cv2.selectROI("Select ROI",image,showCrosshair=True,fromCenter=False)
x,y,w,h=roi
print(f"ROI Coordinates: x={x}, y={y},width={w},height={h}")
roi_image = image.copy()
cv2.rectangle(roi_image,(x, y),(x+w, y+h),(0, 255, 0),2)
cv2.imshow("Selected ROI", roi_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

