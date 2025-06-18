#!/usr/bin/env python3
"""
Database Migration Script for Ecommerce Application
Handles only database table creation for all discovered models in src modules.
"""

import os
import sys
import importlib
import inspect
from dotenv import load_dotenv
from flask import Flask
from src.db import init_db, create_tables

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

class ModelRegistry:
    """Dynamic model registry for table creation only"""
    def __init__(self):
        self.models = {}
    def discover_and_register(self, base_path='src'):
        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), base_path)
        for item in os.listdir(src_path):
            item_path = os.path.join(src_path, item)
            if (os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '__init__.py')) and item != '__pycache__'):
                model_file = os.path.join(item_path, 'model.py')
                if os.path.exists(model_file):
                    module_path = f'src.{item}.model'
                    model_module = importlib.import_module(module_path)
                    for name, obj in inspect.getmembers(model_module, inspect.isclass):
                        if obj.__module__ == model_module.__name__ and hasattr(obj, '__tablename__') and hasattr(obj, 'query'):
                            self.models[name] = obj

class DatabaseMigration:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = init_db(self.app)
        self.registry = ModelRegistry()
    def create_all_tables(self):
        print("📋 Creating database tables...")
        with self.app.app_context():
            self.registry.discover_and_register()
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
