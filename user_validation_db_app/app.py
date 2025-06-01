# app1.py - User Registration App
from flask import Flask, render_template_string, request, jsonify, session
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12782499',
    'user': 'sql12782499',
    'password': 'eBtLvErKkK',
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
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registration System</title>
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

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-size: 1rem;
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }

        button:hover {
            transform: translateY(-2px);
        }

        .message {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
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
            margin-top: 20px;
            display: none;
        }

        .switch-form {
            margin-top: 20px;
            color: #667eea;
            cursor: pointer;
            text-decoration: underline;
        }

        .switch-form:hover {
            color: #764ba2;
        }

        #loginForm {
            display: none;
        }

        .user-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: left;
        }

        .user-info h3 {
            color: #333;
            margin-bottom: 15px;
        }

        .user-detail {
            margin-bottom: 10px;
            color: #555;
        }

        .logout-btn {
            background: #dc3545;
            margin-top: 15px;
            padding: 10px 20px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Registration</h1>

        <!-- Registration Form -->
        <form id="registerForm">
            <div class="form-group">
                <label for="reg_username">Username</label>
                <input type="text" id="reg_username" name="username" required minlength="3">
            </div>

            <div class="form-group">
                <label for="reg_password">Password</label>
                <input type="password" id="reg_password" name="password" required minlength="6">
            </div>

            <div class="form-group">
                <label for="reg_email">Email</label>
                <input type="email" id="reg_email" name="email" required>
            </div>

            <div class="form-group">
                <label for="reg_fullname">Full Name</label>
                <input type="text" id="reg_fullname" name="full_name" required>
            </div>

            <button type="submit">Register</button>
            <div class="switch-form" onclick="switchToLogin()">Already have an account? Login here</div>
        </form>

        <!-- Login Form -->
        <form id="loginForm">
            <div class="form-group">
                <label for="login_username">Username</label>
                <input type="text" id="login_username" name="username" required>
            </div>

            <div class="form-group">
                <label for="login_password">Password</label>
                <input type="password" id="login_password" name="password" required>
            </div>

            <button type="submit">Login</button>
            <div class="switch-form" onclick="switchToRegister()">Don't have an account? Register here</div>
        </form>

        <!-- User Dashboard -->
        <div id="userDashboard" style="display: none;">
            <div class="user-info">
                <h3>Welcome!</h3>
                <div id="userDetails"></div>
                <button class="logout-btn" onclick="logout()">Logout</button>
            </div>
        </div>

        <div class="loading" id="loading">Processing...</div>
        <div class="message" id="message"></div>
    </div>

    <script>
        function switchToLogin() {
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('loginForm').style.display = 'block';
            document.querySelector('h1').textContent = 'User Login';
            clearMessage();
        }

        function switchToRegister() {
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('registerForm').style.display = 'block';
            document.querySelector('h1').textContent = 'User Registration';
            clearMessage();
        }

        function showMessage(text, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = text;
            messageDiv.className = `message ${type}`;
            messageDiv.style.display = 'block';
        }

        function clearMessage() {
            document.getElementById('message').style.display = 'none';
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

        function showDashboard(userData) {
            document.getElementById('registerForm').style.display = 'none';
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('userDashboard').style.display = 'block';
            document.querySelector('h1').textContent = 'Dashboard';

            const userDetails = document.getElementById('userDetails');
            userDetails.innerHTML = `
                <div class="user-detail"><strong>Username:</strong> ${userData.username}</div>
                <div class="user-detail"><strong>Email:</strong> ${userData.email}</div>
                <div class="user-detail"><strong>Full Name:</strong> ${userData.full_name}</div>
                <div class="user-detail"><strong>Member Since:</strong> ${new Date(userData.created_at).toLocaleDateString()}</div>
            `;
        }

        function logout() {
            fetch('/logout', { method: 'POST' })
            .then(() => {
                document.getElementById('userDashboard').style.display = 'none';
                document.getElementById('registerForm').style.display = 'block';
                document.querySelector('h1').textContent = 'User Registration';
                clearMessage();
            });
        }

        // Registration form handler
        document.getElementById('registerForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            showLoading(true);
            clearMessage();

            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    showMessage(data.message, 'success');
                    e.target.reset();
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Registration failed. Please try again.', 'error');
            });
        });

        // Login form handler
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            showLoading(true);
            clearMessage();

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    showDashboard(data.user);
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Login failed. Please try again.', 'error');
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        full_name = data.get('full_name', '').strip()

        # Validation
        if not all([username, password, email, full_name]):
            return jsonify({'success': False, 'message': 'All fields are required'})

        if len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters'})

        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'})

        # Hash password
        hashed_password = hash_password(password)

        # Database operations
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor()

        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Username already exists'})

        # Check if email exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Email already registered'})

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password, email, full_name, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (username, hashed_password.decode('utf-8'), email, full_name)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Registration successful! You can now login.'})

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'})

        # Database operations
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor(dictionary=True)

        # Get user data
        cursor.execute(
            "SELECT id, username, password, email, full_name, created_at FROM users WHERE username = %s AND is_active = TRUE",
            (username,)
        )
        user = cursor.fetchone()

        if not user or not verify_password(password, user['password']):
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid username or password'})

        # Store user session
        session['user_id'] = user['id']
        session['username'] = user['username']

        # Log the login
        cursor.execute(
            "INSERT INTO user_sessions (user_id, ip_address, user_agent) VALUES (%s, %s, %s)",
            (user['id'], request.remote_addr, request.headers.get('User-Agent', ''))
        )
        connection.commit()

        cursor.close()
        connection.close()

        # Return user data (excluding password)
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'created_at': user['created_at'].isoformat() if user['created_at'] else None
        }

        return jsonify({'success': True, 'message': 'Login successful!', 'user': user_data})

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed. Please try again.'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
