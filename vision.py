import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import numpy as np
from PIL import ImageGrab
import cv2

# Define the "Fight" button area (you'll calibrate these coordinates)
BATTLE_ROI = (500, 600, 700, 650) 

def check_battle():
    # Grab the screen at the specific ROI
    screen = np.array(ImageGrab.grab(bbox=BATTLE_ROI))
    # Convert to grayscale and threshold to make text pop for OCR
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    text = pytesseract.image_to_string(thresh, config='--psm 7').lower()
    return "fight" in text