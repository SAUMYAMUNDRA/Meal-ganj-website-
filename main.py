from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Function to load orders from JSON file
def load_orders():
    try:
        with open("orders.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save orders to JSON file
def save_orders(orders):
    with open("orders.json", "w") as f:
        json.dump(orders, f)
# Function to load users from JSON file
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

# Function to save users to JSON file
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)
@app.route('/')
def hello():
    signedin = False
    if 'username' in session:
        signedin = True
    return render_template('index.html',signedin = signedin)
@app.route('/testaments')
def hellor():
    
    return render_template('testaments.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' in session:
        if request.method == 'POST':
            Date = request.form['date']
            mealType = request.form['mealType']
            order_data = {'username': session['username'], 'date': Date, 'meal_type':mealType}
            orders = load_orders()
            orders.append(order_data)
            save_orders(orders)            
            return render_template('order.html',meal = mealType, date=Date)
    else:
        return redirect('/login')
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        current_username = session['username']
        orders = load_orders()
        user_orders = [order for order in orders if order['username'] == current_username]
        return render_template('dashboard.html', orders=user_orders)
    else:
        return redirect('/login')



# Login route





@app.route('/login', methods=['GET', 'POST'])
def login():
    if not 'username' in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            users = load_users()
            if username in users and users[username]['password'] == password:
                session['username'] = username
                return redirect('/')
            else:
                return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')
    else:
        return redirect('/dashboard')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', error="Username already exists")
        else:
            users[username] = {'password': password}
            save_users(users)
            return redirect(url_for('login'))
    return render_template('register.html')

# Protected route
@app.route('/protected')
def protected():
    if 'username' in session:
        return render_template('protected.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3456)
