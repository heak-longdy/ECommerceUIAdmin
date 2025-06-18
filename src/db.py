"""
Database configuration and utilities for Flask-SQLAlchemy
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration class
class DatabaseConfig:
    """Database configuration for Flask applications"""
    
    @staticmethod
    def get_database_uri():
        """Get database URI from environment variables"""
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'ecommerce_db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    @staticmethod
    def configure_app(app):
        """Configure Flask app with database settings"""
        app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfig.get_database_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True
        }
        return app

# Flask-SQLAlchemy instance (to be initialized by the app)
db = SQLAlchemy()

print(os.getenv('DB_PASSWORD', ''))  # Debugging line to check if password is loaded correctly

def init_db(app):
    """Initialize database with Flask app"""
    DatabaseConfig.configure_app(app)
    db.init_app(app)
    return db

def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        try:
            db.create_all()
            logger.info("✅ Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating tables: {e}")
            return False

def drop_tables(app):
    """Drop all database tables (use with caution!)"""
    with app.app_context():
        try:
            db.drop_all()
            logger.info("⚠️  Database tables dropped successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error dropping tables: {e}")
            return False
# Direct PostgreSQL connection utilities (for advanced use cases)
class PostgreSQLConnection:
    """Direct PostgreSQL connection using psycopg2 (for advanced queries)"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'ecommerce_db'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                cursor_factory=RealDictCursor
            )
            self.cursor = self.connection.cursor()
            logger.info("✅ Direct PostgreSQL connection established")
            return True
        except psycopg2.Error as e:
            logger.error(f"❌ Error connecting to PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("PostgreSQL connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error executing query: {e}")
            self.connection.rollback()
            return None
    
    def execute_insert(self, query, params=None):
        """Execute INSERT, UPDATE, or DELETE query"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except psycopg2.Error as e:
            logger.error(f"Error executing insert: {e}")
            self.connection.rollback()
            return None

@contextmanager
def get_raw_connection():
    """Context manager for raw PostgreSQL connection"""
    conn = PostgreSQLConnection()
    if conn.connect():
        try:
            yield conn
        finally:
            conn.disconnect()
    else:
        raise Exception("Failed to connect to PostgreSQL")

def test_connection():
    """Test PostgreSQL connection"""
    try:
        with get_raw_connection() as conn:
            result = conn.execute_query("SELECT version();")
            if result:
                logger.info(f"✅ PostgreSQL version: {result[0]['version']}")
                return True
        return False
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False

def test_flask_db_connection(app):
    """Test Flask-SQLAlchemy connection"""
    with app.app_context():
        try:
            # Test connection by executing a simple query using text()
            from sqlalchemy import text
            result = db.engine.execute(text("SELECT 1")).fetchone()
            if result:
                logger.info("✅ Flask-SQLAlchemy connection successful")
                return True
        except Exception as e:
            # Try alternative method for newer SQLAlchemy versions
            try:
                with db.engine.connect() as connection:
                    result = connection.execute(text("SELECT 1")).fetchone()
                    if result:
                        logger.info("✅ Flask-SQLAlchemy connection successful")
                        return True
            except Exception as e2:
                logger.error(f"❌ Flask-SQLAlchemy connection failed: {e2}")
                return False
    return False

# Flask utilities
def get_db():
    """Get database instance (for use in Flask routes)"""
    return db

def reset_database(app):
    """Reset database (drop all tables and recreate)"""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            logger.info("✅ Database reset successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error resetting database: {e}")
            return False

# Database backup utilities
def backup_table_to_json(table_name, output_file):
    """Backup a table to JSON format"""
    try:
        with get_raw_connection() as conn:
            query = f"SELECT * FROM {table_name};"
            data = conn.execute_query(query)
            
            if data:
                import json
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                logger.info(f"✅ Table {table_name} backed up to {output_file}")
                return True
        return False
    except Exception as e:
        logger.error(f"❌ Error backing up table {table_name}: {e}")
        return False

# Sample usage and testing
if __name__ == "__main__":
    print("🧪 Testing database configuration...")
    
    # Test environment variables
    print(f"Database URI: {DatabaseConfig.get_database_uri()}")
    
    # Test direct connection
    print("\n📡 Testing direct PostgreSQL connection...")
    if test_connection():
        print("✅ Direct connection successful!")
    else:
        print("❌ Direct connection failed!")
    
    # Create a sample Flask app for testing
    print("\n🧪 Testing Flask-SQLAlchemy integration...")
    from flask import Flask
    
    app = Flask(__name__)
    init_db(app)
    
    if test_flask_db_connection(app):
        print("✅ Flask-SQLAlchemy integration successful!")
    else:
        print("❌ Flask-SQLAlchemy integration failed!")
    
    # Test table creation
    print("\n📋 Testing table creation...")
    if create_tables(app):
        print("✅ Table creation successful!")
    else:
        print("❌ Table creation failed!")