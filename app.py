from argon2 import PasswordHasher, hash_password, verify_password
from flask import Flask, flash, render_template, request, redirect, session
import mysql.connector
import pymysql


app = Flask(__name__,template_folder='template')
app.secret_key = 'jw123'

def connect_to_database():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '12345',
        'database': 'child_vaccination'
    }
    return mysql.connector.connect(**db_config)


def register_user(username, password, phoneno, email):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        #hashed_password = hash_password(password)

        insert_query = "INSERT INTO register (username, password, phoneno, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (username, password, phoneno, email))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"User '{username}' registered successfully!")
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

def login_user(username, password):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        select_query = "SELECT password FROM register WHERE username = %s"
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result :
            stored_password = result[0]
            if password == stored_password:
                print("Login successful!")
                session['username'] = username
                return True
            else:
                print("Incorrect password.")
        else:
            print("User not found.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error during login: {e}")
        return False
    
def patient_details(childname, childage, gender, date, time, fathername, childdob, phoneno, address):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        #hashed_password = hash_password(password)

        insert_query = "INSERT INTO patient_details (childname, childage, gender, date, time, fathername, childdob, phoneno, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (childname, childage, gender, date, time, fathername, childdob, phoneno, address))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Patient Details stored successfully!")
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
        
default_username = "doctor"
default_password = "password"
 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phoneno = request.form['phoneno']
        email = request.form['email']
        
        # Register the user
        if register_user(username, password, phoneno, email):
            return redirect('/login')
        

    return render_template('register.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login_user(username, password):
            return redirect('/home')

    return render_template('login.html')
       
    
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        provided_username = request.form.get('username')
        provided_password = request.form.get('password')

      
        if provided_username == default_username and provided_password == default_password:
          
            return redirect('/view')
        else:
           
            return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html', username=default_username, password=default_password)
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        childname = request.form['childname']
        childage = request.form['childage']
        gender = request.form['gender']
        date=request.form['date']
        time = request.form['time']
        fathername = request.form['fathername']
        childdob = request.form['childdob']
        phoneno = request.form['phoneno']
        address = request.form['address']
        
        success = patient_details(childname, childage, gender, date, time, fathername, childdob, phoneno, address)

        if success:
            flash('Registered successfully!', 'success')
            return redirect('/home')
        else:
            flash('Error during registration. Please try again.', 'error')

    return render_template('home.html')


@app.route('/display_details',methods=["GET"])
def display_details():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        search_query = request.args.get('search_query', default='', type=str)
                
        select_query = (
            "SELECT * FROM patient_details "
            "WHERE date LIKE %s "
            "OR childname LIKE %s "
            
        )
        #select_query = "SELECT * FROM car_details"
        cursor.execute(select_query, (f'%{search_query}%', f'%{search_query}%'))
        
        
        patient_detail = cursor.fetchall()

        cursor.close()
        connection.close()
        
        print("Patient Details:", patient_detail)
        
        return render_template('display_details.html', patient_detail = patient_detail)
    
    except pymysql.Error as e:
        
        print(f"Error in fetching details: {e}")

        return render_template('error.html',error_message="Error fetching billing details")
    
@app.route('/view')
def view():
  
    return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)
