import pytesseract
import cv2
import numpy as np
from PIL import Image
image_path = "static/captcha9.png"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
kernel = np.ones((2, 2), np.uint8)
morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
resized = cv2.resize(morphed, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
processed_image = Image.fromarray(resized)
custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWYZ'
captcha_text = pytesseract.image_to_string(processed_image, config=custom_config)
print("Extracted Text:", captcha_text.strip())
print("Generated CAPTCHA Text:", captcha_text)





