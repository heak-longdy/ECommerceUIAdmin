#!/usr/bin/env python3
"""
Database Migration Script for Ecommerce Application
Handles only database table creation for all discovered models in src modules.
"""

import os
import sys
from dotenv import load_dotenv
from flask import Flask
from src.db import init_db, create_tables
import importlib

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

# --- Import all models here to ensure they are registered with SQLAlchemy ---
# Dynamically import all model files in src/Models
models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'Models')
for filename in os.listdir(models_dir):
    if filename.endswith('.py') and not filename.startswith('__'):
        module_name = filename[:-3]
        importlib.import_module(f'src.Models.{module_name}')

class DatabaseMigration:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = init_db(self.app)
    def create_all_tables(self):
        print("📋 Creating database tables...")
        with self.app.app_context():
            if create_tables(self.app):
                print("✅ All tables created successfully")
                return True
            else:
                print("❌ Failed to create tables")
                return False

def main():
    migration = DatabaseMigration()
    migration.create_all_tables()

if __name__ == '__main__':
    main()
