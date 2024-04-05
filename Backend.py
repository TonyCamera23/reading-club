from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# SQLite configuration
db = sqlite3.connect('helix_database.db')
cursor = db.cursor()

# Create user_sign_up table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS user_sign_up (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  passcode TEXT NOT NULL,
                  confirm_passcode TEXT NOT NULL,
                  flincap_optimism_wallet_address TEXT NOT NULL)''')
db.commit()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    passcode = data.get('passcode')
    confirm_passcode = data.get('confirm_passcode')
    wallet_address = data.get('flincap_optimism_wallet_address')

    # Check if passwords match
    if passcode != confirm_passcode:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if email is already registered
    cursor.execute("SELECT * FROM user_sign_up WHERE email=?", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({'error': 'Email is already registered'}), 400

    # Insert new user into database
    try:
        cursor.execute("""INSERT INTO user_sign_up (email, passcode, confirm_passcode, flincap_optimism_wallet_address)
                          VALUES (?, ?, ?, ?)""", (email, passcode, confirm_passcode, wallet_address))
        db.commit()
        return jsonify({'message': 'Sign-up successful'}), 200
    except Exception as e:
        return jsonify({'error': 'Error while signing up'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    passcode = data.get('passcode')

    # Check if email and password match
    cursor.execute("SELECT * FROM user_sign_up WHERE email=? AND passcode=?", (email, passcode))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/transactions/earn', methods=['POST'])
def earn_tokens():
    # Handle earning tokens
    return jsonify({'message': 'Tokens earned'})

@app.route('/transactions/spend', methods=['POST'])
def spend_tokens():
    # Handle spending tokens
    return jsonify({'message': 'Tokens spent'})

if __name__ == '__main__':
    app.run(debug=True)
