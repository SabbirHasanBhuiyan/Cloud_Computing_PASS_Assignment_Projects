# app1.py - User Authentication App
from flask import Flask, render_template_string, request, jsonify, session
import mysql.connector
from mysql.connector import Error
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Database Configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12781148',
    'user': 'sql12781148',
    'password': 'h9iJN2JMRZ',
    'port': 3306
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database tables"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create users table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            connection.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Authentication System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }

        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .tab {
            flex: 1;
            padding: 15px;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            font-size: 1.1rem;
        }

        .tab.active {
            background: #667eea;
            color: white;
        }

        .form-container {
            display: none;
        }

        .form-container.active {
            display: block;
        }

        .input-group {
            margin-bottom: 20px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
            margin-top: 10px;
        }

        button:hover {
            transform: translateY(-2px);
        }

        .message {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }

        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .loading {
            color: #667eea;
            margin-top: 15px;
            display: none;
        }

        .dashboard {
            display: none;
            text-align: center;
        }

        .welcome {
            color: #667eea;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }

        .logout-btn {
            background: #dc3545;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="authSection">
            <h1>🔐 Authentication</h1>

            <div class="tabs">
                <button class="tab active" onclick="showTab('login')">Login</button>
                <button class="tab" onclick="showTab('register')">Register</button>
            </div>

            <!-- Login Form -->
            <div id="loginForm" class="form-container active">
                <form id="loginFormData">
                    <div class="input-group">
                        <label for="loginUsername">Username</label>
                        <input type="text" id="loginUsername" required>
                    </div>
                    <div class="input-group">
                        <label for="loginPassword">Password</label>
                        <input type="password" id="loginPassword" required>
                    </div>
                    <button type="submit">Login</button>
                </form>
            </div>

            <!-- Register Form -->
            <div id="registerForm" class="form-container">
                <form id="registerFormData">
                    <div class="input-group">
                        <label for="registerUsername">Username</label>
                        <input type="text" id="registerUsername" required>
                    </div>
                    <div class="input-group">
                        <label for="registerEmail">Email</label>
                        <input type="email" id="registerEmail" required>
                    </div>
                    <div class="input-group">
                        <label for="registerPassword">Password</label>
                        <input type="password" id="registerPassword" required>
                    </div>
                    <div class="input-group">
                        <label for="confirmPassword">Confirm Password</label>
                        <input type="password" id="confirmPassword" required>
                    </div>
                    <button type="submit">Register</button>
                </form>
            </div>

            <div class="loading" id="loading">Processing...</div>
            <div class="message" id="message"></div>
        </div>

        <!-- Dashboard -->
        <div id="dashboard" class="dashboard">
            <div class="welcome" id="welcomeMessage"></div>
            <p>Welcome to your dashboard! You are successfully logged in.</p>
            <button class="logout-btn" onclick="logout()">Logout</button>
        </div>
    </div>

    <script>
        function showTab(tab) {
            // Hide all forms
            document.querySelectorAll('.form-container').forEach(form => {
                form.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(t => {
                t.classList.remove('active');
            });

            // Show selected form
            document.getElementById(tab + 'Form').classList.add('active');
            event.target.classList.add('active');

            // Clear messages
            hideMessage();
        }

        function showMessage(text, type) {
            const message = document.getElementById('message');
            message.textContent = text;
            message.className = `message ${type}`;
            message.style.display = 'block';
        }

        function hideMessage() {
            document.getElementById('message').style.display = 'none';
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        // Login Form Handler
        document.getElementById('loginFormData').addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            hideMessage();
            showLoading(true);

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({username, password})
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    document.getElementById('authSection').style.display = 'none';
                    document.getElementById('dashboard').style.display = 'block';
                    document.getElementById('welcomeMessage').textContent = `Hello, ${data.username}!`;
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Something went wrong. Please try again.', 'error');
            });
        });

        // Register Form Handler
        document.getElementById('registerFormData').addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            if (password !== confirmPassword) {
                showMessage('Passwords do not match!', 'error');
                return;
            }

            hideMessage();
            showLoading(true);

            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({username, email, password})
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    showMessage(data.message, 'success');
                    document.getElementById('registerFormData').reset();
                    setTimeout(() => showTab('login'), 2000);
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Something went wrong. Please try again.', 'error');
            });
        });

        function logout() {
            fetch('/logout', {method: 'POST'})
            .then(() => {
                document.getElementById('authSection').style.display = 'block';
                document.getElementById('dashboard').style.display = 'none';
                document.getElementById('loginFormData').reset();
                hideMessage();
            });
        }
    </script>
</body>
</html>
    ''')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'})

        if len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters'})

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'})

        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor()

        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Username already exists'})

        # Insert new user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        connection.commit()

        return jsonify({'success': True, 'message': 'Registration successful! Please login.'})

    except Error as e:
        return jsonify({'success': False, 'message': 'Registration failed'})
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'})

        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor()
        password_hash = hash_password(password)

        cursor.execute(
            "SELECT id, username FROM users WHERE username = %s AND password_hash = %s",
            (username, password_hash)
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({'success': True, 'username': user[1]})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})

    except Error as e:
        return jsonify({'success': False, 'message': 'Login failed'})
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
