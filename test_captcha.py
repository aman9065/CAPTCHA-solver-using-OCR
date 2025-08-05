import pytesseract
import cv2
import numpy as np
from PIL import Image

# 1. Load image
image_path = "static/captcha9.png"
image = cv2.imread(image_path)

# 2. Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# 4. Adaptive thresholding (inverted binary)
thresh = cv2.adaptiveThreshold(
    blurred, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,  # You can try ADAPTIVE_THRESH_GAUSSIAN_C too
    cv2.THRESH_BINARY_INV,
    blockSize=11,
    C=2
)

# 5. Morphological operations to remove small dots/noise
kernel = np.ones((2, 2), np.uint8)
cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
cleaned = cv2.dilate(cleaned, kernel, iterations=1)

# 6. Resize to make characters more readable
resized = cv2.resize(cleaned, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

# 7. Convert for PIL
processed_image = Image.fromarray(resized)

# 8. OCR Config
custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz'

# 9. OCR Execution
captcha_text = pytesseract.image_to_string(processed_image, config=custom_config).strip()

# 10. Load actual text
with open("static/captcha_text.txt", "r") as f:
    real_text = f.read().strip()

# 11. Comparison
print("Generated CAPTCHA Text (Ground Truth):", real_text)
print("Extracted CAPTCHA Text (OCR Output):", captcha_text)

if captcha_text == real_text:
    print("✅ CAPTCHA matched!")
else:
    print("❌ CAPTCHA mismatch!")









