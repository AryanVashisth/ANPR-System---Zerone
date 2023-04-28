import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
# Load the input image
image = cv2.imread('./test images/p5.jpg')

# Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 50, 200)

# Detect license plates
plate_cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
plates = plate_cascade.detectMultiScale(edged, scaleFactor=1.1, minNeighbors=5)

# Segment and recognize characters
for (x, y, w, h) in plates:
    plate = image[y:y + h, x:x + w]
    plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    plate_thresh = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    plate_chars = pytesseract.image_to_string(plate_thresh, config='--psm 11')

    # Print the recognized characters
    print("License plate: ", plate_chars.strip())
