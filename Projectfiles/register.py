from flask import Flask, render_template, request,url_for,redirect
from pymongo import MongoClient

app = Flask(__name__, static_url_path='static')

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['test']  # Replace 'your_database' with your actual database name
collection = db['sampledata']  # Replace 'your_collection' with your actual collection name

@app.route('/register', methods=['POST'])
def register():
     if request.method == 'POST':
    # Get data from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Insert data into MongoDB
        user_data = {
            'username': username,
            'email': email,
            'password': password
            }
        collection.insert_one(user_data)

            # Optionally, you can redirect to another page after storing data
        return redirect(url_for('index.html')) # Render a success page
     
        # Render the registration form
     return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
