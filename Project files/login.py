from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__, static_url_path='static')

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Replace 'your_database' with your actual database name
collection = db['your_collection']  # Replace 'your_collection' with your actual collection name

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password match a document in the database
        user = collection.find_one({'username': username, 'password': password})
        if user:
            # Successful login, redirect to a different page
            return redirect(url_for('index.html'))
        else:
            # Invalid credentials, render login page with error message
            return render_template('login.html', error='Invalid username or password')

    # Render the login form
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

