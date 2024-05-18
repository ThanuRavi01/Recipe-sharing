from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_HOST = 'host.docker.internal'  
DB_NAME = 'Foodie-biss'
DB_USER = 'postgres'
DB_PASSWORD = 'Thanu_2003'
DB_PORT = '5433'

def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e.pgcode} - {e.pgerror}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                            (username, email, hashed_password))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login'))
            except psycopg2.Error as e:
                print("Error while inserting data:", e)
                conn.rollback()
                cur.close()
                conn.close()
                error = "An error occurred while registering. Please try again. Username might already exist"
                return render_template('register.html', error=error)
        else:
            error = "Database connection error. Please try again later."
            return render_template('register.html', error=error)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT password FROM users WHERE username = %s", (username,))
                result = cur.fetchone()
                cur.close()
                conn.close()
                if result and check_password_hash(result[0], password):
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    error = "Invalid username or password. Please try again."
                    return render_template('login.html', error=error)
            except psycopg2.Error as e:
                print("Error while fetching data:", e)
                conn.close()
                error = "An error occurred while logging in. Please try again."
                return render_template('login.html', error=error)
        else:
            error = "Database connection error. Please try again later."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Route to handle search query
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']

        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Example query to retrieve data based on search term
        cur.execute("SELECT recipe_name,ingredients, instructions FROM recipes WHERE recipe_name ILIKE %s", ('%' + search_term + '%',))
        recipes = cur.fetchall()

        cur.close()
        conn.close()

        # Render the HTML page with the retrieved data
        return render_template('recipe.html', recipes=recipes, search_term=search_term)
    
    # Render recipe form
    return render_template('recipe.html')

@app.route('/submit_feedback', methods=['GET','POST'])
def submit_feedback():
    if request.method == 'POST':
         recipe_name = request.form['recipe_name']
         rating = int(request.form['rating'])
         feedback = request.form['feedback']

         # Connect to the database
         conn = connect_db()
         cur = conn.cursor()

         # Insert feedback into database
         cur.execute("INSERT INTO feedbacks (recipe_name, rating, feedback) VALUES (%s, %s, %s)", (recipe_name, rating, feedback))
         conn.commit()

         cur.close()
         conn.close()

          # Flash the success message
         flash("Feedback submitted successfully!", "success")
         # Redirect to the index page
         return redirect(url_for('search'))
    
    # Render registration form
    return render_template('feedback.html')        
            

@app.route('/submit_recipe', methods=['GET','POST'])
def submit_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        # Get the current datetime
        current_date = datetime.datetime.now()

        # Convert the datetime to a string in the desired format
        current_date_str = current_date.strftime('%Y-%m-%d %H:%M:%S')

        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Insert recipe into database
        cur.execute("INSERT INTO recipes (recipe_name, ingredients, instructions, created_at) VALUES (%s, %s, %s, %s)", (recipe_name, ingredients, instructions, current_date_str))
        conn.commit()

        cur.close()
        conn.close()

       # Flash the success message
        flash("Recipe submitted successfully!", "success")
        # Redirect to the index page
        return redirect(url_for('search'))
    
    # Render registration form
    return render_template('addrecipe.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        # Get form data
        Name = request.form['Name']
        Contactemail = request.form['Contact_email']
        Message = request.form['Message']

        # Insert contact us data into database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO contactus(name,contact_email,message) VALUES (%s, %s, %s)",(Name, Contactemail, Message))
                conn.commit()
                cur.close()
                conn.close()                
                 # Flash the success message
                flash("Thank you for contacting us! We will get back to you soon.", "success")
                # Redirect to the index page
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                # Log the full traceback of the exception for debugging purposes
                app.logger.error("Error submitting contact us form: %s", e, exc_info=True)
                # Flash error message and render contact us form
                flash("An error occurred during contact us submission. Please try again.", "error")
                return render_template('contactus.html')
        else:
            # Render contact us form with error message
            return render_template('contactus.html', error="Unable to connect to the database. Please try again later.")
    
    # Render contact us form
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)