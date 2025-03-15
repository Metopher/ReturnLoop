import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',      # Replace with your MySQL host
    'user': 'root',           # Replace with your MySQL username
    'password': '',           # Replace with your MySQL password
    'database': 'accounts'     # Replace with your database name
}

# Function to insert data into the table
def insert_data(name, mail):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to insert data
        query = "INSERT INTO users (name, mail) VALUES (%s, %s)"
        values = (name, mail)

        # Execute the query
        cursor.execute(query, values)

        # Commit the transaction
        conn.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Input data from the user
name = input("Enter your name: ")
mail = input("Enter your email: ")

# Insert data into the table
insert_data(name, mail)