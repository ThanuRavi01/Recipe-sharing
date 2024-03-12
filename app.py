from flask import Flask, render_template, request
import psycopg2

# Define database connection parameters
DB_NAME = 'Foody_biss'
DB_USER = 'Thanu_kjc'
DB_PASSWORD = 'KJC@24'
DB_HOST = 'local_pgdb'
DB_PORT = '5432'

# Define a function to connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                # Execute a query to fetch data
                cursor.execute("SELECT * FROM your_table")
                # Fetch all rows
                rows = cursor.fetchall()
                # Close cursor and connection
                cursor.close()
                conn.close()
                # Render template with fetched data
                return render_template('register.html', rows=rows)
            except Exception as e:
                return f"Error fetching data: {e}"
        else:
            return "Failed to connect to the database."

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
