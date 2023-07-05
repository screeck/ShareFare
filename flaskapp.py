from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Flask(__name__, static_folder='templates/static')
app.secret_key = 'jsnbfdbglsirvledjeoantoa2t472fn38f'


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

    # Check if the email already exists in the database
    cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()[0]

    if result > 0:
        # Email already exists, return an error message
        cursor.close()
        conn.close()
        return "Registration failed. An account with this email already exists."

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
        result = cursor.fetchone()
        logger.info(f"result: {result}")
        # Close the database connection


        if result is not None:
            # Authentication successful, retrieve the first name
            cursor.execute(
                "SELECT first_name FROM users WHERE email = %s",
                (email,)
            )
            first_name = cursor.fetchone()[0]

            # Set the session variable
            session['first_name'] = first_name

            cursor.close()
            conn.close()

            return redirect(url_for('main', firstName=first_name))
        else:
            # Authentication failed, return an error message
            return "Authentication failed. Please check your email and password."

    return render_template('login.html')


@app.route('/main')
def main():
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

    # Retrieve the product data from the database
    cursor.execute("SELECT p.id, p.title, p.date, pi.image_url FROM products p LEFT JOIN product_images pi ON p.id = pi.product_id")
    products = []
    product = None
    for row in cursor.fetchall():
        if product is None or product[0] != row[0]:
            # Create a new product object
            if product is not None:
                products.append(product)
            product = [row[0], row[1], row[2], []]  # [id, title, date, images]
        if row[3]:
            # Append the image URL to the product's images list
            product[3].append(row[3])

    if product is not None:
        products.append(product)

    # Close the database connection
    cursor.close()
    conn.close()

    first_name = session.get('first_name')
    return render_template('main.html', first_name=first_name, products=products)



@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect the user to the index page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
