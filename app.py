from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import heapq  # For Dijkstra's Algorithm

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Function to get a new database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="users"
    )

# Graph Representation of Kochi (Distances in KM)
graph = {
    "Aluva": {"Edappally": 10, "Kakkanad": 14},
    "Edappally": {"Aluva": 10, "Kaloor": 6, "Kakkanad": 8},
    "Kaloor": {"Edappally": 6, "MG Road": 4},
    "MG Road": {"Kaloor": 4, "Fort Kochi": 11},
    "Fort Kochi": {"MG Road": 11, "Willingdon Island": 5},
    "Willingdon Island": {"Fort Kochi": 5, "Thevara": 6},
    "Thevara": {"Willingdon Island": 6, "Vyttila": 7},
    "Vyttila": {"Thevara": 7, "Kakkanad": 9, "Tripunithura": 6},
    "Kakkanad": {"Edappally": 8, "Aluva": 14, "Vyttila": 9},
    "Tripunithura": {"Vyttila": 6}
}

# Dijkstra's Algorithm to find the shortest distance
def dijkstra(graph, start, end):
    queue = [(0, start)]  # (distance, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            return current_distance  # Return total shortest distance

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return float('inf')  # No path found

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Get Ride Route (Shortest Distance Calculation)
@app.route('/get_ride', methods=['GET', 'POST'])
def get_ride():
    total_distance = None
    if request.method == 'POST':
        start = request.form.get('start_location')
        destination = request.form.get('destination')

        # Debugging Output
        print(f"Ride Request - Start: {start}, Destination: {destination}")

        # Check if locations exist in the graph
        if start not in graph or destination not in graph:
            flash("Invalid locations entered! Please choose valid areas in Kochi.", "danger")
            print("fail")
        else:
            total_distance = dijkstra(graph, start, destination)
            flash(f"Shortest distance from {start} to {destination} is {total_distance} km.", "success")
            print("success")

            # Store ride details in `districts` table if user is logged in
            if 'user' in session:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO district (area, destination, email) VALUES (%s, %s, %s)", 
                               (start, destination, session['user']))
                conn.commit()
                conn.close()

    return render_template('get_ride.html', total_distance=total_distance)

# Pooling Route
@app.route('/pooling', methods=['GET', 'POST'])
def pooling():
    if request.method == 'POST':
        pickup_location = request.form.get('location')
        destination = request.form.get('destination')
        date = request.form.get('date')

        # Debugging Output
        print(f"Pooling Request - Pickup: {pickup_location}, Destination: {destination}, Date: {date}")

        # Check if locations exist in the graph
        if pickup_location not in graph or destination not in graph:
            flash("Invalid locations entered! Please choose valid areas in Kochi.", "danger")
        else:
            # Store pooling request in the database if user is logged in
            if 'user' in session:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pooling_requests (pickup_location, destination, date, email) VALUES (%s, %s, %s, %s)", 
                               (pickup_location, destination, date, session['user']))
                conn.commit()
                conn.close()
                flash("Pooling request submitted successfully!", "success")
            else:
                flash("You must be logged in to submit a pooling request.", "warning")

    return render_template('pooling.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM idpass WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            conn.close()
            return redirect(url_for('login'))

        cursor.execute("INSERT INTO idpass (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        conn.close()

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM idpass WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = email
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed. Check your email or password.", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)