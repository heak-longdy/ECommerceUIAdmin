# Jinja2 Template Structure

This project has been refactored to use Jinja2 templates with a modular structure for better maintainability and reusability.

## Template Structure

```
templates/
├── base.html          # Main base template with common layout
├── sidebar.html       # Reusable sidebar component
├── index.html         # Dashboard page (extends base)
└── PurchaseOrder.html # Purchase order page (extends base)
```

## Template Breakdown

### 1. `base.html` - Base Template
- Contains the main HTML structure
- Includes sidebar via `{% include 'sidebar.html' %}`
- Defines blocks for content, title, CSS, and JS
- Handles top navigation bar
- Uses `url_for()` for static files

### 2. `sidebar.html` - Sidebar Component
- Reusable sidebar that can be included in any template
- Dynamic active states based on `active_page` variable
- Conditional dropdown expansion via `expanded_sections`
- Template variables:
  - `active_page`: Highlights current page in sidebar
  - `project_name`: Project name display
  - `expanded_sections`: List of sections to show as expanded

### 3. `index.html` - Dashboard Template
- Extends `base.html`
- Implements the main dashboard content
- Supports dynamic build cards via `build_cards` variable
- Template variables:
  - `build_cards`: List of dashboard cards with title, stat, descriptions
  - `user_email`: User email for display
  - `plan_type`: Plan type (Spark, Pro, Enterprise)

### 4. `PurchaseOrder.html` - Purchase Order Template
- Extends `base.html`
- Purchase order form and recent orders display
- Template variables:
  - `recent_orders`: List of recent purchase orders

## Usage in Flask

### Basic Route
```python
@app.route('/')
def home():
    return render_template('index.html', 
                         active_page='overview',
                         project_name='Ecommerce',
                         plan_type='Pro plan',
                         expanded_sections=['ai'])
```

### Route with Dynamic Data
```python
@app.route('/dashboard')
def dashboard():
    build_cards = [
        {
            'title': 'Hosting',
            'stat': '2.5GB',
            'descriptions': ['Downloads (7d total)', 'Status: <b>Active</b>']
        }
    ]
    
    return render_template('index.html',
                         active_page='overview',
                         build_cards=build_cards,
                         expanded_sections=['ai', 'build'])
```

## Template Variables

### Common Variables (used across templates)
- `active_page`: Current page identifier for sidebar highlighting
- `project_name`: Project name (default: 'Ecommerce')
- `plan_type`: Plan type (default: 'Pro plan')
- `expanded_sections`: List of sidebar sections to show expanded
- `user_email`: User email address

### Dashboard Specific (`index.html`)
- `build_cards`: Array of card objects with:
  - `title`: Card title
  - `stat`: Main statistic
  - `descriptions`: Array of description strings (HTML allowed)

### Purchase Order Specific (`PurchaseOrder.html`)
- `recent_orders`: Array of order objects with:
  - `id`: Order ID
  - `vendor`: Vendor name
  - `total`: Total amount
  - `status`: Order status
  - `date`: Order date

## Benefits

1. **Reusability**: Sidebar and base layout can be reused across all pages
2. **Maintainability**: Changes to sidebar or base layout affect all pages
3. **Consistency**: Uniform look and feel across the application
4. **Dynamic Content**: Easy to pass data from Flask routes to templates
5. **Modularity**: Each template has a specific purpose and responsibility

## Running the Demo

1. Use the main app: `python app.py`
2. Use the demo app: `python jinja_demo.py`
3. Access at: http://localhost:5000

The demo includes multiple routes showing different template variable combinations.
