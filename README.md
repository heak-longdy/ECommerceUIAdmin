# Ecommerce Dashboard

A modern, responsive ecommerce dashboard built with Flask, featuring a collapsible sidebar, dynamic topbar, smooth animations, and PostgreSQL database integration.

## Features

- **Responsive Design**: Clean, modern interface that works on all screen sizes
- **Interactive Sidebar**: Collapsible sidebar with smooth animations and tooltips
- **Dynamic Topbar**: Changes appearance based on scroll position
- **Component-based Architecture**: Modular HTML templates using Jinja2
- **Modern Styling**: CSS Grid/Flexbox layouts with Material Design icons
- **PostgreSQL Integration**: Robust database connectivity with both ORM and raw SQL support
- **RESTful API**: Complete user management endpoints

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with psycopg2 and SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Templating**: Jinja2
- **Icons**: Material Symbols
- **Fonts**: DM Sans

## Database Setup

### 1. Install PostgreSQL
**macOS (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database credentials
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Ecommerce
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
python setup.py
```

5. Run the application:
```bash
python app.py
# Or run the example API:
python example_app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Database Usage

### Connection Methods

**Method 1: Direct psycopg2**
```python
from src.db import PostgreSQLConnection

db = PostgreSQLConnection()
if db.connect():
    users = db.execute_query("SELECT * FROM users;")
    db.disconnect()
```

**Method 2: SQLAlchemy ORM**
```python
from src.db import get_db_session

with get_db_session() as session:
    # Use SQLAlchemy models here
    pass
```

### API Endpoints
- `GET /` - Health check
- `GET /health/db` - Database connection test
- `GET /users` - Get all users
- `POST /users` - Create new user
- `GET /users/<id>` - Get user by ID

### Test Database Connection
```python
from src.db import test_connection
print("Connected!" if test_connection() else "Failed!")
```
