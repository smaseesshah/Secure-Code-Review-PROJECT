from flask import Flask, request, jsonify, render_template
import hashlib
import os

# Import our custom modules
import database
import init_db 
import sqlite3

# Initialize Flask to look for HTML in 'templates' and assets in 'static'
app = Flask(__name__, template_folder='templates', static_folder='static')

# VULNERABILITY 1: HARDCODED SECRET
SENDGRID_API_KEY = "sg-secret-key-987654321-taskvault"

# --- Automatic Database Initialization ---
if not os.path.exists(database.DB_FILE):
    print(f"Database file '{database.DB_FILE}' not found. Initializing...")
    init_db.initialize_database()

# --- Helper Functions ---
def get_current_user():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    return None

# ==========================================
# FRONTEND ROUTES (Serving HTML)
# ==========================================

@app.route('/')
@app.route('/login.html')
def serve_login():
    return render_template('login.html')

@app.route('/register.html')
def serve_register():
    return render_template('register.html')

@app.route('/dashboard.html')
def serve_dashboard():
    return render_template('dashboard.html')

@app.route('/task.html')
def serve_task():
    return render_template('task.html')


# ==========================================
# BACKEND API ROUTES
# ==========================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    search_query = request.args.get('search')
    
    if search_query:
        tasks = database.search_tasks(search_query)
        return jsonify(tasks), 200
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = [{"id": r["id"], "title": r["title"], "owner": r["owner_username"]} for r in rows]
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    title = request.json.get('title')
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, owner_username) VALUES (?, ?)", (title, current_user))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task created"}), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"id": row["id"], "title": row["title"], "owner": row["owner_username"]}), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, comment_text FROM comments WHERE task_id = ?", (task_id,))
    rows = cursor.fetchall()
    conn.close()

    comments = [{"username": r["username"], "text": r["comment_text"]} for r in rows]
    return jsonify(comments), 200

@app.route('/api/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    text = request.json.get('text')

    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (task_id, username, comment_text) VALUES (?, ?, ?)", 
                   (task_id, current_user, text))
    conn.commit()
    conn.close()

    return jsonify({"message": "Comment added"}), 201

if __name__ == '__main__':
    # Changed port to 3000 as requested
    app.run(debug=True, port=3000)