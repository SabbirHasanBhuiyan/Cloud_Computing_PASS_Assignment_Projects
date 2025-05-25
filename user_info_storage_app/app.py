# app2.py - User Validation and Management App
from flask import Flask, render_template_string, request, jsonify, session
import mysql.connector
from mysql.connector import Error
import bcrypt
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
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
    <title>User Validation System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
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
            max-width: 800px;
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

        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #2c3e50;
            box-shadow: 0 0 0 3px rgba(44, 62, 80, 0.1);
        }

        button {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
            margin: 5px;
        }

        button:hover {
            transform: translateY(-2px);
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 0.9rem;
        }

        .btn-success {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        }

        .btn-danger {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        }

        .btn-info {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
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

        .info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }

        .loading {
            color: #2c3e50;
            margin-top: 20px;
            display: none;
        }

        .tabs {
            display: flex;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
        }

        .tab {
            padding: 12px 24px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            color: #666;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .tab.active {
            color: #2c3e50;
            border-bottom-color: #2c3e50;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .users-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 0.9rem;
        }

        .users-table th,
        .users-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        .users-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }

        .status-active {
            color: #27ae60;
            font-weight: bold;
        }

        .status-inactive {
            color: #e74c3c;
            font-weight: bold;
        }

        .user-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2c3e50;
        }

        .stat-label {
            color: #666;
            margin-top: 5px;
        }

        .login-form {
            max-width: 400px;
            margin: 0 auto;
        }

        .validation-result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }

        .validation-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
        }

        .validation-error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Validation System</h1>

        <div class="tabs">
            <div class="tab active" onclick="showTab('login')">Login</div>
            <div class="tab" onclick="showTab('validate')">Validate User</div>
            <div class="tab" onclick="showTab('manage')">Manage Users</div>
            <div class="tab" onclick="showTab('stats')">Statistics</div>
        </div>

        <!-- Login Tab -->
        <div id="login" class="tab-content active">
            <div class="login-form">
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
                </form>
            </div>
        </div>

        <!-- Validate User Tab -->
        <div id="validate" class="tab-content">
            <form id="validateForm">
                <div class="form-group">
                    <label for="val_username">Username to Validate</label>
                    <input type="text" id="val_username" name="username" required>
                </div>

                <div class="form-group">
                    <label for="val_password">Password</label>
                    <input type="password" id="val_password" name="password" required>
                </div>

                <button type="submit" class="btn-info">Validate User</button>
            </form>

            <div id="validationResult" class="validation-result">
                <!-- Validation results will appear here -->
            </div>
        </div>

        <!-- Manage Users Tab -->
        <div id="manage" class="tab-content">
            <button onclick="loadUsers()" class="btn-info">Refresh Users</button>

            <div id="usersContainer">
                <!-- Users will be loaded here -->
            </div>
        </div>

        <!-- Statistics Tab -->
        <div id="stats" class="tab-content">
            <button onclick="loadStats()" class="btn-info">Load Statistics</button>

            <div id="statsContainer">
                <!-- Stats will be loaded here -->
            </div>
        </div>

        <div class="loading" id="loading">Processing...</div>
        <div class="message" id="message"></div>
    </div>

    <script>
        let currentUser = null;

        function showTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });

            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });

            // Show selected tab content
            document.getElementById(tabName).classList.add('active');

            // Add active class to clicked tab
            event.target.classList.add('active');

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
            document.getElementById('validationResult').style.display = 'none';
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }

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
                    currentUser = data.user;
                    showMessage(`Welcome, ${data.user.full_name}!`, 'success');
                    e.target.reset();
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Login failed. Please try again.', 'error');
            });
        });

        // Validate form handler
        document.getElementById('validateForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            showLoading(true);
            clearMessage();

            fetch('/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                const resultDiv = document.getElementById('validationResult');

                if (data.success) {
                    resultDiv.className = 'validation-result validation-success';
                    resultDiv.innerHTML = `
                        <h3>✓ User Validation Successful</h3>
                        <p><strong>Username:</strong> ${data.user.username}</p>
                        <p><strong>Full Name:</strong> ${data.user.full_name}</p>
                        <p><strong>Email:</strong> ${data.user.email}</p>
                        <p><strong>Account Status:</strong> <span class="status-active">Active</span></p>
                        <p><strong>Member Since:</strong> ${new Date(data.user.created_at).toLocaleDateString()}</p>
                    `;
                } else {
                    resultDiv.className = 'validation-result validation-error';
                    resultDiv.innerHTML = `
                        <h3>✗ User Validation Failed</h3>
                        <p>${data.message}</p>
                    `;
                }

                resultDiv.style.display = 'block';
                e.target.reset();
            })
            .catch(err => {
                showLoading(false);
                showMessage('Validation failed. Please try again.', 'error');
            });
        });

        function loadUsers() {
            showLoading(true);

            fetch('/users')
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                const container = document.getElementById('usersContainer');

                if (data.success) {
                    let html = `
                        <table class="users-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Full Name</th>
                                    <th>Status</th>
                                    <th>Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;

                    data.users.forEach(user => {
                        html += `
                            <tr>
                                <td>${user.id}</td>
                                <td>${user.username}</td>
                                <td>${user.email}</td>
                                <td>${user.full_name}</td>
                                <td><span class="${user.is_active ? 'status-active' : 'status-inactive'}">
                                    ${user.is_active ? 'Active' : 'Inactive'}
                                </span></td>
                                <td>${new Date(user.created_at).toLocaleDateString()}</td>
                                <td>
                                    <button class="btn-small ${user.is_active ? 'btn-danger' : 'btn-success'}"
                                            onclick="toggleUserStatus(${user.id}, ${user.is_active})">
                                        ${user.is_active ? 'Deactivate' : 'Activate'}
                                    </button>
                                </td>
                            </tr>
                        `;
                    });

                    html += '</tbody></table>';
                    container.innerHTML = html;
                } else {
                    container.innerHTML = '<p>Failed to load users.</p>';
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Failed to load users.', 'error');
            });
        }

        function loadStats() {
            showLoading(true);

            fetch('/stats')
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                const container = document.getElementById('statsContainer');

                if (data.success) {
                    container.innerHTML = `
                        <div class="user-stats">
                            <div class="stat-card">
                                <div class="stat-number">${data.stats.total_users}</div>
                                <div class="stat-label">Total Users</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">${data.stats.active_users}</div>
                                <div class="stat-label">Active Users</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">${data.stats.inactive_users}</div>
                                <div class="stat-label">Inactive Users</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number">${data.stats.recent_logins}</div>
                                <div class="stat-label">Recent Logins (24h)</div>
                            </div>
                        </div>
                    `;
                } else {
                    container.innerHTML = '<p>Failed to load statistics.</p>';
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Failed to load statistics.', 'error');
            });
        }

        function toggleUserStatus(userId, currentStatus) {
            showLoading(true);

            fetch('/toggle-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({user_id: userId, is_active: !currentStatus})
            })
            .then(response => response.json())
            .then(data => {
                showLoading(false);
                if (data.success) {
                    showMessage(data.message, 'success');
                    loadUsers(); // Refresh the users list
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(err => {
                showLoading(false);
                showMessage('Failed to update user status.', 'error');
            });
        }
    </script>
</body>
</html>
    ''')

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

@app.route('/validate', methods=['POST'])
def validate_user():
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
            "SELECT id, username, password, email, full_name, created_at, is_active FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'User not found'})

        if not user['is_active']:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'User account is deactivated'})

        if not verify_password(password, user['password']):
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid password'})

        cursor.close()
        connection.close()

        # Return user data (excluding password)
        user_data = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'created_at': user['created_at'].isoformat() if user['created_at'] else None,
            'is_active': user['is_active']
        }

        return jsonify({'success': True, 'message': 'User validation successful!', 'user': user_data})

    except Exception as e:
        print(f"Validation error: {e}")
        return jsonify({'success': False, 'message': 'Validation failed. Please try again.'})

@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, username, email, full_name, created_at, is_active FROM users ORDER BY created_at DESC"
        )
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        # Convert datetime objects to strings
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()

        return jsonify({'success': True, 'users': users})

    except Exception as e:
        print(f"Get users error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch users'})

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor(dictionary=True)

        # Get user statistics
        cursor.execute("SELECT COUNT(*) as total_users FROM users")
        total_users = cursor.fetchone()['total_users']

        cursor.execute("SELECT COUNT(*) as active_users FROM users WHERE is_active = TRUE")
        active_users = cursor.fetchone()['active_users']

        cursor.execute("SELECT COUNT(*) as inactive_users FROM users WHERE is_active = FALSE")
        inactive_users = cursor.fetchone()['inactive_users']

        # Get recent logins (last 24 hours)
        cursor.execute(
            "SELECT COUNT(DISTINCT user_id) as recent_logins FROM user_sessions WHERE login_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR)"
        )
        recent_logins = cursor.fetchone()['recent_logins']

        cursor.close()
        connection.close()

        stats = {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'recent_logins': recent_logins
        }

        return jsonify({'success': True, 'stats': stats})

    except Exception as e:
        print(f"Stats error: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch statistics'})

@app.route('/toggle-user', methods=['POST'])
def toggle_user_status():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        is_active = data.get('is_active')

        if user_id is None or is_active is None:
            return jsonify({'success': False, 'message': 'Invalid parameters'})

        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'})

        cursor = connection.cursor()

        # Update user status and set updated_at
        cursor.execute(
            "UPDATE users SET is_active = %s, updated_at = NOW() WHERE id = %s",
            (is_active, user_id)
        )
        connection.commit()

        cursor.close()
        connection.close()

        status_text = 'activated' if is_active else 'deactivated'
        return jsonify({'success': True, 'message': f'User {status_text} successfully'})

    except Exception as e:
        print(f"Toggle user error: {e}")
        return jsonify({'success': False, 'message': 'Failed to update user status'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host='0.0.0.0', port=port)
