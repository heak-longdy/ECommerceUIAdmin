"""
Example Flask application with PostgreSQL integration
"""
from flask import Flask, jsonify, request
from src.db import PostgreSQLConnection, get_db_session, test_connection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def home():
    """Home route"""
    return jsonify({
        'message': 'Ecommerce API with PostgreSQL',
        'status': 'running'
    })

@app.route('/health/db')
def health_check():
    """Database health check"""
    if test_connection():
        return jsonify({'database': 'connected', 'status': 'healthy'})
    else:
        return jsonify({'database': 'disconnected', 'status': 'unhealthy'}), 500

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users using direct psycopg2 connection"""
    db = PostgreSQLConnection()
    if not db.connect():
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        users = db.execute_query("SELECT * FROM users ORDER BY created_at DESC;")
        return jsonify({'users': users or []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    db = PostgreSQLConnection()
    if not db.connect():
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        # Create users table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute_insert(create_table_query)
        
        # Insert new user
        insert_query = """
        INSERT INTO users (name, email) 
        VALUES (%s, %s) 
        RETURNING id, name, email, created_at;
        """
        db.cursor.execute(insert_query, (data['name'], data['email']))
        new_user = db.cursor.fetchone()
        db.connection.commit()
        
        return jsonify({'user': dict(new_user)}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    db = PostgreSQLConnection()
    if not db.connect():
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        user = db.execute_query("SELECT * FROM users WHERE id = %s;", (user_id,))
        if user:
            return jsonify({'user': dict(user[0])})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.disconnect()

if __name__ == '__main__':
    # Test database connection on startup
    print("Testing database connection...")
    if test_connection():
        print("✅ Database connected successfully!")
    else:
        print("❌ Database connection failed!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
