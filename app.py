from flask import Flask, render_template, redirect, url_for, request, session, flash
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# MongoDB connection using MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.hostel_management  
users_collection 


app.secret_key = "secret"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        user_exists = db.users.find_one({"email": email})
        if user_exists:
            flash('Email already exists!')
            return redirect(url_for('register'))

        # Insert the user into the MongoDB collection
        db.users.insert_one({
            'name': name,
            'email': email,
            'password': password,
            'role': role
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = db.users.find_one({"email": email, "password": password})
        
        if user:
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', role=session['role'])
    return redirect(url_for('login'))

# Hostel routes
@app.route('/hostel')
def hostel():
    return render_template('hostel.html')

@app.route('/hostel/view/<string:hostel_type>')
def view_hostel(hostel_type):
    # Fetch rooms based on hostel type from MongoDB
    rooms = db.hostel_booking.find({"hostel_type": hostel_type})
    
    return render_template('view_hostel.html', hostel_type=hostel_type, rooms=rooms)

@app.route('/hostel/book_manual', methods=['GET', 'POST'])
def book_room_manual():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        college_id = request.form['college_id']
        phone_number = request.form['phone_number']
        aadhaar_number = request.form['aadhaar_number']
        address = request.form['address']
        hostel_type = request.form['hostel_type']
        room_no = request.form['room_no']
        
        # Insert the booking details into the hostel_booking collection
        db.hostel_booking.insert_one({
            'name': name,
            'age': age,
            'college_id': college_id,
            'phone_number': phone_number,
            'aadhaar_number': aadhaar_number,
            'address': address,
            'hostel_type': hostel_type,
            'room_no': room_no,
            'is_booked': True
        })

        flash('Room booked successfully!')
        return redirect(url_for('view_hostel', hostel_type=hostel_type))

    return render_template('book_room_manual.html')

# Event routes
@app.route('/events')
def events():
    all_events = db.events.find()
    return render_template('events.html', events=all_events)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    if 'role' in session and session['role'] == 'Admin':
        if request.method == 'POST':
            name = request.form['name']
            date = request.form['date']
            place = request.form['place']
            description = request.form['description']
            
            db.events.insert_one({
                'name': name,
                'date': datetime.datetime.strptime(date, '%Y-%m-%d'),
                'place': place,
                'description': description
            })
            flash('Event added successfully!')
            return redirect(url_for('events'))
        return render_template('add_event.html')
    return redirect(url_for('login'))

# Contact routes
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/mess')
def mess():
    return render_template('mess.html')

@app.route('/study_hours')
def study_hours():
    return render_template('study_hours.html')

if __name__ == '__main__':
    app.run(debug=True)
