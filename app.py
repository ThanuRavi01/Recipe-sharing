from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# PostgreSQL database configuration
DB_HOST = 'localhost'
DB_NAME = 'foody_bliss'
DB_USER = 'Thanu_KJC'
DB_PASSWORD = 'KJC@24'

# Connect to PostgreSQL database
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn
# Route for index page (dashboard)
@app.route('/')
def index():
    # Render the index page
    return render_template('index.html')


# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Insert data into database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO registration (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to login page after registration
        return redirect(url_for('login'))

    # Render registration form
    return render_template('register.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check if username and password exist in database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM registration WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            # User found, redirect to dashboard
            return redirect(url_for('index'))
        else:
            # User not found, render login page with error message
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)

    # Render login form
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
