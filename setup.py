#!/usr/bin/env python3
"""
Setup script for PostgreSQL Ecommerce project
"""
import os
import sys
import subprocess
from src.db import test_connection, create_tables

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📄 Creating .env file from template...")
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created! Please update it with your database credentials.")
        else:
            print("❌ .env.example file not found!")
            return False
    else:
        print("ℹ️  .env file already exists")
    return True

def test_db_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    if test_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        print("Please check your database credentials in the .env file")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up PostgreSQL Ecommerce Project")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        return False
    
    # Step 2: Create .env file
    if not create_env_file():
        return False
    
    # Step 3: Test database connection
    if not test_db_connection():
        print("\n📋 Setup completed with database connection issues.")
        print("Please:")
        print("1. Make sure PostgreSQL is running")
        print("2. Update the .env file with correct database credentials")
        print("3. Run 'python setup.py' again to test the connection")
        return False
    
    # Step 4: Create tables
    print("📊 Creating database tables...")
    if create_tables():
        print("✅ Database tables created successfully!")
    else:
        print("⚠️  Warning: Could not create tables (this is normal if using direct SQL)")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your database credentials")
    print("2. Run: python example_app.py")
    print("3. Test the API at http://localhost:5000")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
