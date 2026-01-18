from flask import Flask, request, redirect, render_template, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "major_project_secret"

# Fixed authority users
AUTH_USERS = {
    "auth@example.com": "auth123",
    "auth2@example.com": "auth456"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Database connection
def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn


# Login page
@app.route('/')
def login_page():
    return render_template('institution/login.html')

# Signup page
@app.route('/signup')
def signup_page():
    return render_template('institution/signup.html')


# Handle login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Authority login (fixed users)
    if role == "authority":
        from app import AUTH_USERS
        if email in AUTH_USERS and AUTH_USERS[email] == password:
            session['role'] = 'authority'
            session['email'] = email
            return redirect('/authority_dashboard')
        else:
            return "Invalid Authority Credentials"

    # Institution login (DB)
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=? AND role=?",
        (email, password, role)
    ).fetchone()
    conn.close()

    if user:
        session['role'] = 'institution'
        session['user_id'] = user['id']
        return redirect('/institution_dashboard')

    return "Invalid login credentials"


# Handle signup / registration
@app.route('/register', methods=['POST'])
def register():
    # Fixed role for this form
    role = 'institution'

    # Form fields from signup.html
    inst_name = request.form['institution_name']
    email = request.form['email']
    password = request.form['password']
    institute_type = request.form['institute_type']
    institute_id = request.form['institute_id']
    aff_uni = request.form.get('affiliated_university', '')
    est_year = request.form['established_year']
    state = request.form['state']
    district = request.form['district']
    city = request.form['city']
    pincode = request.form['pincode']
    category = request.form['category']
    phone = request.form['phone']
    authorized_person = request.form['authorized_person']
    designation = request.form['designation']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert into users table
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (inst_name, email, password, role)
        )
        user_id = cursor.lastrowid  # get generated user id

        # Insert into institutions table
        cursor.execute("""
            INSERT INTO institutions (
                user_id, institution_name, institute_type, institute_id, affiliating_university,
                year_of_establishment, state, district, city, pin_code,
                category, official_email, phone, authorized_person, designation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, inst_name, institute_type, institute_id, aff_uni,
            est_year, state, district, city, pincode,
            category, email, phone, authorized_person, designation
        ))

        conn.commit()

    except sqlite3.IntegrityError as e:
        return f"Error: {e}"

    finally:
        conn.close()

    return redirect('/institution_dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')

    conn = get_db_connection()
    inst = conn.execute(
        "SELECT * FROM institutions WHERE user_id=?",
        (session['user_id'],)
    ).fetchone()
    conn.close()

    return render_template('institution/profile.html', inst=inst)


# Dashboards
@app.route('/institution_dashboard')
def institution_dashboard():
    # For simplicity, assume last registered institution is logged in
    # Later you can use session to store logged-in user
    conn = get_db_connection()
    inst = conn.execute("SELECT * FROM institutions ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()

    return render_template('institution/dashboard.html', institution=inst)

@app.route('/authority_dashboard')
def authority_dashboard():
    return render_template('authority/dashboard.html')

# Run Flask
if __name__ == '__main__':
    app.run()
