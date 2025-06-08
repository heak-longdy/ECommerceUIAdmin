# Ecommerce Dashboard

A modern, responsive ecommerce dashboard built with Flask, featuring a collapsible sidebar, dynamic topbar, and smooth animations.

## Features

- **Responsive Design**: Clean, modern interface that works on all screen sizes
- **Interactive Sidebar**: Collapsible sidebar with smooth animations and tooltips
- **Dynamic Topbar**: Changes appearance based on scroll position
- **Component-based Architecture**: Modular HTML templates using Jinja2
- **Modern Styling**: CSS Grid/Flexbox layouts with Material Design icons

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Templating**: Jinja2
- **Icons**: Material Symbols
- **Fonts**: DM Sans

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── sidebar.html      # Sidebar component
│   └── order/           # Order management templates
├── css/                  # Stylesheets
│   ├── styles.css       # Main styles
│   ├── form.css         # Form styling
│   ├── table.css        # Table styling
│   └── order.css        # Order-specific styles
├── js/                   # JavaScript files
│   ├── script.js        # Main application logic
│   └── purchase-order.js # Order management logic
└── html/                # Static HTML files
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

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

### Sidebar Navigation
- Click the toggle button to collapse/expand the sidebar
- Hover over collapsed items to see tooltips
- Navigate through different sections using the dropdown menus

### Dashboard Features
- Scroll down in the main content area to see the topbar animation
- Responsive design adapts to different screen sizes
- Clean, modern interface with smooth transitions

## Development

### Running in Development Mode
```bash
python app.py
```

### File Structure
- `templates/base.html`: Main layout template
- `templates/sidebar.html`: Reusable sidebar component
- `css/styles.css`: Main stylesheet with responsive design
- `js/script.js`: Core JavaScript functionality

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
