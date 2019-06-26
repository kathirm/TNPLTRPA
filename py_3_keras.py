import cv2
 
img = cv2.imread("/tmp/R.Sarathipriyan.1.jpg", cv2.IMREAD_COLOR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 1.5)
gray = cv2.Canny(gray, 0, 50)
   
cv2.imshow("img", img)
cv2.waitKey();
