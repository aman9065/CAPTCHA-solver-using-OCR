# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import bcrypt
import random
import string
import os
from captcha.image import ImageCaptcha
from PIL import Image
import pytesseract
from PIL import ImageFilter,ImageDraw,ImageFont

from captcha.image import ImageCaptcha

class CleanImageCaptcha(ImageCaptcha):
    def create_noise_dots(self, image, color):
        pass  

    def create_noise_curve(self, image, color):
        pass 

image = CleanImageCaptcha(width=160, height=60, font_sizes=[50])


# Flask app and configuration
app = Flask(__name__)
app.secret_key = "Aman123@56zw"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'helloaman'
mysql = MySQL(app)

# WTForms
class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Signup')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def home():
    return redirect(url_for('generate_captcha'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO captcha (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash("Signup successful. Please login.", "success")
        return redirect(url_for('generate_captcha'))

    return render_template('signup.html', form=form)

@app.route('/generate')
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))  # Use correct attribute: digits
    width, height = 160, 50
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Use a font available on your system — update this if needed
    font_path = "C:/Windows/Fonts/arial.ttf"  # For Windows
    font = ImageFont.truetype(font_path, 36)

    x = 10
    for char in captcha_text:
        draw.text((x, 5), char, font=font, fill='black')
        x += 30

    
    os.makedirs("static", exist_ok=True)

    image_path = "static/captcha9.png"  
    image.save(image_path)

    session['captcha'] = captcha_text
    print("Generated CAPTCHA Text:", captcha_text)
    return render_template("index.html")









@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user_input = request.form.get('captcha')

        if user_input != session.get('captcha'):
            flash("Incorrect CAPTCHA", "danger")
            return redirect(url_for('generate_captcha'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM captcha WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            db_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid password.", "danger")
        else:
            flash("User not found.", "danger")
        return redirect(url_for('generate_captcha'))

    return render_template('success.html', form=form)

@app.route('/success')
def success():
    return('success.html')

@app.route('/refresh')
def refresh():
    return redirect(url_for('generate_captcha'))

if __name__ == '__main__':
    app.run(debug=True, port=7000)
  