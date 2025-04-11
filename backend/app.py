from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
import os

# Configure Flask to serve from React's build output
app = Flask(
    __name__,
    static_folder='../frontend/users/dist',
    template_folder='../frontend/users/dist'
)

CORS(app)

# -------------------Database initialiation---------------------
@app.route('/init', methods=['GET'])
def create_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    return 'Database Created Successfully'

# ----------------------------------------
# CRUD ROUTES
# ----------------------------------------
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (data['name'], data['email']))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id, 'name': data['name'], 'email': data['email']}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users')
    users = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'name': row[1], 'email': row[2]})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (data['name'], data['email'], user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})

# ----------------------------------------
# STATIC ROUTES FOR REACT
# ----------------------------------------
@app.route('/')
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

@app.route('/vite.svg')
def vite_logo():
    return send_from_directory(app.static_folder, 'vite.svg')

# ----------------------------------------
# MAIN
# ----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
