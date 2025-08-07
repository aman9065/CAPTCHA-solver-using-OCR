 CAPTCHA Solver using OCR 🔐🧠

This is a Flask-based web application that reads and solves CAPTCHA images using OCR (Optical Character Recognition).  
It uses `pytesseract`, OpenCV, and image processing techniques to accurately extract and verify text from CAPTCHAs.  
It also includes login/signup functionality with password hashing and MySQL database.

---

 🚀 Features

- 🔍 CAPTCHA text extraction using Tesseract OCR
- 🖼️ Image preprocessing with OpenCV
- 🧾 Login and Signup with bcrypt password hashing
- 🗂️ Flask structure with templates and static folders
- ✅ CAPTCHA validation with user input

---

 🛠️ Tech Stack

- Python 3
- Flask
- OpenCV
- **Pytesseract**
- MySQL
- Bcrypt
- HTML + CSS

---

📁 Project Structure

📦 CAPTCHA-solver-using-OCR
├── app.py
├── test_captcha.py
├── templates/
│ ├── index.html
│ ├── Signup.html
│ └── success.html 
├── static/
│ ├── style.css
│ ├── SINGUP.css
│ └── captcha9.png (sample image)
└── README.md

 Reading Accuracy Analysis

Noise levels were increased from 10% to 90%, and OCR accuracy was tracked. Below is a summary:

| Noise Level | Accuracy         |
|-------------|------------------|
| 10%         | ~90%             |
| 25% + color | ~75-80%          |
| 50% + color | ~60-65%          |
| 75%         | ~45%             |
| 90%         | Failed (1–2 chars unreadable) |

 
 .
 
