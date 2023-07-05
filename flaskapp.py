from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)

db_host = 'app-2b62167e-79b3-4a11-876c-ba8bc5ab7bb5-do-user-14289936-0.b.db.ondigitalocean.com'
db_port = '25060'
db_name = 'defaultdb'
db_user = 'doadmin'
db_password = 'AVNS_BlevRoe2edlQnO-TME1'


@app.route('/')
def home():
    return render_template('index.html')

# Route for displaying the registration form
@app.route('/register', methods=['GET'])
def display_registration_form():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    # Retrieve form data from the request
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password,
        sslmode='require'
    )
    cursor = conn.cursor()

    # Insert the user data into the database
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, email, password)
    )

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    # Redirect the user to a success page or perform any other necessary actions
    return "User registered successfully!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data from the request
        email = request.form['email']
        password = request.form['password']

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            sslmode='require'
        )
        cursor = conn.cursor()

        # Execute the database query to check user credentials
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        result = cursor.fetchone()[0]

        # Close the database connection
        cursor.close()
        conn.close()

        if result > 0:
            # Authentication successful, redirect to the main page
            return redirect('/main')
        else:
            # Authentication failed, return an error message
            return "Authentication failed. Please check your email and password."

    return render_template('login.html')

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
