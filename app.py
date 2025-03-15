from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="users"
)
cursor = connection.cursor()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Signup route (GET + POST)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        cursor.execute("SELECT * FROM idpass WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('login'))

        # Insert new user
        cursor.execute("INSERT INTO idpass (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        connection.commit()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route (GET + POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verify credentials
        cursor.execute("SELECT * FROM idpass WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = email  # Store session
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed. Check your email or password.", "danger")

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

# Other routes
@app.route('/get_ride')
def get_ride():
    return render_template('get_ride.html')

@app.route('/pooling')
def pooling():
    return render_template('pooling.html')

if __name__ == '__main__':
    app.run(debug=True)
