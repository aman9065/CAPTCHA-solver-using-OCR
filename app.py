from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask import make_response

import bcrypt
import random
import string
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "Aman123@56zw"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project captcha'

mysql = MySQL(app)



def generate_captcha():
    import random, string, os
    from PIL import Image, ImageDraw, ImageFont
    from flask import session

    # 1. Generate random CAPTCHA text
    captcha_text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    # 2. Create white image
    width, height = 160, 50
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 36)

    # 3. Draw text on image
    x = 10
    for char in captcha_text:
        draw.text((x, 5), char, font=font, fill='black')
        x += 30

    # 4. Save image to static folder
    os.makedirs("static", exist_ok=True)
    image.save("static/captcha9.png")

    with open("static/captcha_text.txt", "w") as f:
        f.write(captcha_text)
    # 5. Store text in session
    session['captcha_text'] = captcha_text
    print("CAPTCHA Generated:", captcha_text)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/generate')
def generate():
    generate_captcha()
    return '', 204

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'first_name': request.form.get('first_name'),
            'middle_name': request.form.get('middle_name') or '',
            'last_name': request.form.get('last_name'),
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm': request.form.get('confirm_password')
        }

        if not all([data['first_name'], data['last_name'], data['username'], data['email'], data['password'], data['confirm']]):
            flash("Please fill all required fields.", "danger")
            return redirect(url_for('signup'))

        if data['password'] != data['confirm']:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_table WHERE username = %s OR email = %s", (data['username'], data['email']))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or Email already exists. Please choose another.", "danger")
            cursor.close()
            return redirect(url_for('signup'))

        
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("""
            INSERT INTO user_table (first_name, middle_name, last_name, username, email, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['first_name'], data['middle_name'], data['last_name'], data['username'], data['email'], hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash("Signup successful. Please login.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_input = request.form.get('captcha')  
        if user_input != session.get('captcha_text'):
            flash("Incorrect CAPTCHA", "danger")
            generate_captcha()
            return redirect(url_for('login'))
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_table WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            db_password = user[6]
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('success'))
            else:
                flash("Invalid username or password.", "danger")
        else:
            flash("User not found.", "danger")
        generate_captcha()
        return redirect(url_for('login'))
    generate_captcha()
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
@app.route('/success')
def success():
    if 'username' in session:
        return render_template('success.html')
    else:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=7000)






  