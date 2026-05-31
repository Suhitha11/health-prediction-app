from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import google.generativeai as genai
import re
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)

# ----------------------------
# LOAD ENV + GEMINI SETUP
# ----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ----------------------------
# CREATE TABLE
# ----------------------------
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_table()

# ----------------------------
# HOME PAGE
# ----------------------------
@app.route('/', methods=['GET', 'POST'])
def home():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    prediction = None

    if request.method == 'POST':

        fullname = request.form['fullname'].strip()
        dob = request.form['dob']
        email = request.form['email'].strip()
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        # ----------------------------
        # VALIDATION
        # ----------------------------
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            prediction = "❌ Invalid Email Address"
        elif dob > datetime.today().strftime('%Y-%m-%d'):
            prediction = "❌ Date of Birth cannot be in future"
        else:
            try:
                glucose = float(glucose)
                haemoglobin = float(haemoglobin)
                cholesterol = float(cholesterol)
            except ValueError:
                prediction = "❌ Blood values must be numeric"
            else:

                # ----------------------------
                # GEMINI PROMPT
                # ----------------------------
                prompt = f"""
                Analyze these blood test values:

                Glucose: {glucose}
                Haemoglobin: {haemoglobin}
                Cholesterol: {cholesterol}

                Give a short health risk assessment in one sentence.
                """

                response = model.generate_content(prompt)
                prediction = response.text

                # ----------------------------
                # SAVE TO DATABASE
                # ----------------------------
                cursor.execute('''
                INSERT INTO patients
                (fullname, dob, email, glucose, haemoglobin, cholesterol, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (fullname, dob, email, glucose, haemoglobin, cholesterol, prediction)
                )

                conn.commit()

    # ----------------------------
    # FETCH DATA
    # ----------------------------
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        patients=patients,
        prediction=prediction
    )

# ----------------------------
# EDIT PATIENT
# ----------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        prompt = f"""
        Analyze these blood test values:

        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        Give a short health risk assessment in one sentence.
        """

        response = model.generate_content(prompt)
        remarks = response.text

        cursor.execute('''
        UPDATE patients
        SET fullname=?,
            dob=?,
            email=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        ''',
        (fullname, dob, email, glucose, haemoglobin, cholesterol, remarks, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template('edit.html', patient=patient)

# ----------------------------
# DELETE PATIENT
# ----------------------------
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# ----------------------------
# RUN APP
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)