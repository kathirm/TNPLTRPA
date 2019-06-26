from cv2 import imread
from cv2 import imshow
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle
# load the photograph
pixels = imread('/tmp/R.Sarathipriyan.1.jpg')
# load the pre-trained model
classifier = CascadeClassifier('/tmp/haarcascade_frontalface_default.xml')
# perform face detection
bboxes = classifier.detectMultiScale(pixels)
# print bounding box for each detected face
for box in bboxes:
    

    x, y, width, height = box
    x2, y2 = x + width, y + height

    rectangle(pixels, (x, y), (x2, y2), (0,0,255), 1)

imshow('face detection', pixels)
waitKey(0)
destroyAllWindows()
