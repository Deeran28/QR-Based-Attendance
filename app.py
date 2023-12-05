from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import io
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3 
import cv2
import pyzbar.pyzbar as pyzbar
import time
from datetime import date, datetime
import tkinter as tk
from tkinter import Frame, ttk, messagebox
from tkinter import *
from playsound import playsound

app = Flask(__name__)
app.secret_key = 'upload@123'

conn = sqlite3.connect('userdata.db', check_same_thread=False)
cursor = conn.cursor()

def create_database():
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uplods (
            id INTEGER PRIMARY KEY,
            filename BLOB,
            date_uploaded DATE
        )
    ''')
    conn.commit()
    conn.close()

create_database()
from datetime import datetime

app.static_folder = 'static'
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Login successful!"
    return render_template("new.html")

@app.route("/upload", methods=["GET", "POST"])
def uplod():
    if request.method == "POST":
        return "Signup successful!"
    return render_template("upload_file.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        return "Signup successful!"
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, id_number, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    return render_template('user_manage.html', employee_data=rows)

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    name = request.form.get('name')
    id = request.form.get('id')
    email = request.form.get('email')

    cursor.execute('SELECT * FROM users WHERE name = ? OR id_number = ? OR email = ?', (name, id, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Data already exists in the database."

    qr_data = f"{name} {id} {email}"
    print(qr_data)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_path = f'static/qrcodes/{name,id,email}.png'
    img.save(img_path)


    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'deeransp28@gmail.com'
    smtp_password = 'ndqbxjuupdzjsfqj'

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = 'QR Code'

    text = MIMEText('Hi,\nToday you Signup for Qr code\nHere is your QR code Attached below Please Verify.\nThanks&Regards\nDeeran')
    msg.attach(text)

    image = open(img_path, 'rb').read()
    image_attachment = MIMEImage(image, name='qr_code.png')
    msg.attach(image_attachment)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, msg.as_string())
        server.quit()
        print("QR code sent successfully!")
    except Exception as e:
        print(f"Error sending QR code: {str(e)}")
    
    cursor.execute('INSERT INTO users (name, id_number, email, qrcode) VALUES (?, ?, ?, ?)', (name, id, email, image))
    conn.commit()

    print("QR code sent successfully and data saved to the database.")
    return render_template('qr_generated.html', img_path=img_path)

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    try:
        # Get the ID from the request
        employee_id = request.form.get('id_number')
        
        # Perform the deletion in your database
        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (employee_id,))
        conn.commit()
        conn.close()
        
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False)
    
@app.route('/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file:
            # Check if a file with the same name already exists in the database
            cursor.execute("SELECT id FROM files WHERE filename = ?", (uploaded_file.filename,))
            existing_file = cursor.fetchone()

            if existing_file:
                # Flash a message indicating the file already exists
                return "Data already exists in the database."
            else:
                # Read the file as binary data
                file_data = uploaded_file.read()

                # Get the current date and time
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insert the file and current date into the database
                cursor.execute("INSERT INTO files (filename, filedata, upload_date) VALUES (?, ?, ?)",
                               (uploaded_file.filename, file_data, current_date))
                conn.commit()

                # Flash a success message
                return "File Uploaded Successfully."

    return render_template('upload_file.html')

@app.route('/view_attendance_files')
def view_attendance_files():
    # Fetch the list of uploaded files from the database
    cursor.execute("SELECT id, filename, upload_date FROM files")
    files = cursor.fetchall()
    return render_template('View_File.html')

@app.route('/download_file/<int:file_id>')
def download_file(file_id):
    # Fetch the file data from the database by ID
    cursor.execute("SELECT filename, filedata FROM files WHERE id = ?", (file_id,))
    file_record = cursor.fetchone()

    if file_record:
        filename, filedata = file_record
        # Create a response object with the file data
        response = io.BytesIO(filedata)
        response.seek(0)

        return send_file(response, attachment_filename=filename, as_attachment=True)
    else:
        # Handle the case where the file ID doesn't exist
        flash('File not found', 'danger')
        return redirect(url_for('view_attendance_files'))

if __name__ == '__main__':
    app.run(debug=True)
