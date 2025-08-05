import pytesseract, cv2, numpy as np
from PIL import Image

image = cv2.imread("static/captcha9.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

kernel = np.ones((2, 2), np.uint8)
cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
cleaned = cv2.dilate(cleaned, kernel, iterations=1)

resized = cv2.resize(cleaned, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
processed_image = Image.fromarray(resized)

custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'
captcha_text = pytesseract.image_to_string(processed_image, config=custom_config).strip()

with open("static/captcha_text.txt", "r") as f:
    real_text = f.read().strip()

print("Generated CAPTCHA Text (Ground Truth):", real_text)
print("Extracted CAPTCHA Text (OCR Output):", captcha_text)
print("✅ CAPTCHA matched!" if captcha_text == real_text else "❌ CAPTCHA mismatch!")










