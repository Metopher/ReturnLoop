from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for the new home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the "Get a Ride" page
@app.route('/get_ride')
def get_ride():
    return render_template('get_ride.html')

# Route for the pooling page
@app.route('/pooling')
def pooling():
    return render_template('pooling.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)