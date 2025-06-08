import os
import shutil
from pathlib import Path

def create_project_structure():
    """Create the organized project structure"""
    
    base_path = Path("/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce")
    
    # Create directories including images folder
    directories = ['css', 'js', 'html', 'assets', 'images', 'components']
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    
    print("\n📁 Project structure created successfully!")
    print("📂 Ecommerce/")
    print("├── 📁 css/          # Stylesheets")
    print("├── 📁 js/           # JavaScript files") 
    print("├── 📁 html/         # HTML templates")
    print("├── 📁 assets/       # Images, fonts, etc.")
    print("├── 📁 images/       # Logo and image files")
    print("└── 📁 components/   # Reusable components")

def generate_logo_files():
    """Generate SVG and create PNG conversion HTML for the logo"""
    
    base_path = Path("/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce")
    
    # Create SVG logo file
    svg_content = '''<svg width="50" height="50" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
  <!-- Background circle -->
  <circle cx="25" cy="25" r="24" fill="#1a73e8" stroke="#fff" stroke-width="1"/>
  
  <!-- Shopping cart icon -->
  <g transform="translate(12, 12)">
    <!-- Cart body -->
    <path d="M7 4V2a2 2 0 0 0-2-2H3v2h2v2H3l1.68 7.39A2 2 0 0 0 6.62 15h8.76A2 2 0 0 0 17.32 13.39L19 6H7z" 
          fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Cart wheels -->
    <circle cx="9" cy="20" r="1" fill="#fff"/>
    <circle cx="15" cy="20" r="1" fill="#fff"/>
    
    <!-- Handle -->
    <path d="M19 6h3l-1 4" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>
    
    <!-- Items in cart -->
    <rect x="8" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
    <rect x="11" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
    <rect x="14" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
  </g>
</svg>'''
    
    # Save SVG file
    svg_path = base_path / "images" / "logo.svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✅ Created SVG logo: {svg_path}")
    
    # Create PNG generator HTML file
    png_generator_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PNG Logo Generator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
        .logo-container { margin: 20px 0; }
        .download-btn { 
            background: #1a73e8; color: white; border: none; 
            padding: 12px 24px; border-radius: 8px; margin: 10px;
            cursor: pointer; font-size: 14px;
        }
        .download-btn:hover { background: #1565c0; }
        .size-btn { 
            background: #f1f3f4; border: 1px solid #dadce0; 
            padding: 8px 16px; margin: 5px; border-radius: 4px; cursor: pointer;
        }
        .size-btn.active { background: #1a73e8; color: white; }
        .instructions { margin-top: 30px; color: #666; }
    </style>
</head>
<body>
    <h1>🛒 Ecommerce Logo Generator</h1>
    
    <div class="logo-container">
        <svg id="logo" width="100" height="100" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
            <circle cx="25" cy="25" r="24" fill="#1a73e8" stroke="#fff" stroke-width="1"/>
            <g transform="translate(12, 12)">
                <path d="M7 4V2a2 2 0 0 0-2-2H3v2h2v2H3l1.68 7.39A2 2 0 0 0 6.62 15h8.76A2 2 0 0 0 17.32 13.39L19 6H7z" 
                      fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="20" r="1" fill="#fff"/>
                <circle cx="15" cy="20" r="1" fill="#fff"/>
                <path d="M19 6h3l-1 4" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>
                <rect x="8" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
                <rect x="11" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
                <rect x="14" y="8" width="2" height="1.5" fill="#fff" rx="0.3"/>
            </g>
        </svg>
    </div>
    
    <div>
        <p><strong>Select PNG size:</strong></p>
        <button class="size-btn active" data-size="50">50x50</button>
        <button class="size-btn" data-size="100">100x100</button>
        <button class="size-btn" data-size="200">200x200</button>
        <button class="size-btn" data-size="512">512x512</button>
    </div>
    
    <div>
        <button class="download-btn" onclick="downloadPNG()">📥 Download PNG Logo</button>
        <button class="download-btn" onclick="downloadSVG()">📥 Download SVG Logo</button>
    </div>
    
    <div class="instructions">
        <h3>📋 Instructions:</h3>
        <p>1. Select your desired PNG size above</p>
        <p>2. Click "Download PNG Logo" to save the logo</p>
        <p>3. The file will be saved as "ecommerce-logo-[size].png"</p>
        <p>4. Use this logo in your ecommerce project!</p>
    </div>

    <script>
        let selectedSize = 50;
        
        document.querySelectorAll('.size-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                selectedSize = parseInt(this.dataset.size);
            });
        });
        
        function downloadPNG() {
            const svg = document.getElementById('logo');
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            canvas.width = selectedSize;
            canvas.height = selectedSize;
            
            const data = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([data], {type: 'image/svg+xml;charset=utf-8'});
            const url = URL.createObjectURL(svgBlob);
            
            const img = new Image();
            img.onload = function() {
                ctx.drawImage(img, 0, 0, selectedSize, selectedSize);
                
                canvas.toBlob(function(blob) {
                    const link = document.createElement('a');
                    link.download = `ecommerce-logo-${selectedSize}x${selectedSize}.png`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                    
                    URL.revokeObjectURL(url);
                    URL.revokeObjectURL(link.href);
                });
            };
            img.src = url;
        }
        
        function downloadSVG() {
            const svg = document.getElementById('logo');
            const data = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([data], {type: 'image/svg+xml;charset=utf-8'});
            
            const link = document.createElement('a');
            link.download = 'ecommerce-logo.svg';
            link.href = URL.createObjectURL(svgBlob);
            link.click();
            
            URL.revokeObjectURL(link.href);
        }
    </script>
</body>
</html>'''
    
    # Save PNG generator HTML
    generator_path = base_path / "logo-generator.html"
    with open(generator_path, 'w', encoding='utf-8') as f:
        f.write(png_generator_html)
    print(f"✅ Created PNG generator: {generator_path}")
    
    return svg_path, generator_path

def copy_original_file():
    """Copy the original firebase dashboard file to the new structure"""
    
    source = Path("/Users/longdy/Documents/Projects/Python/NewProject/firebase_dashboard0000.html")
    destination = Path("/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce/firebase_dashboard_backup.html")
    
    try:
        if source.exists():
            shutil.copy2(source, destination)
            print(f"✅ Copied original file to: {destination}")
        else:
            print(f"❌ Source file not found: {source}")
    except Exception as e:
        print(f"❌ Error copying file: {e}")

def show_file_info():
    """Show information about the created files"""
    
    base_path = Path("/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce")
    
    files_info = {
        "css/styles.css": "All CSS styles with Boxicons integration",
        "js/script.js": "JavaScript functionality for sidebar and dropdowns", 
        "html/index.html": "Clean HTML structure with external references",
        "images/logo.svg": "SVG logo file for the ecommerce project",
        "logo-generator.html": "PNG logo generator tool",
        "copy_files.py": "This Python script for project organization"
    }
    
    print("\n📋 Created Files:")
    print("=" * 50)
    
    for file_path, description in files_info.items():
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"📄 {file_path}")
            print(f"   📝 {description}")
            print(f"   📊 Size: {size} bytes")
            print(f"   📍 Path: {full_path}")
            print()

def main():
    """Main function to run the file organization"""
    
    print("🚀 Ecommerce Project Organizer with Logo Generator")
    print("=" * 50)
    
    # Create project structure
    create_project_structure()
    
    # Generate logo files
    svg_path, generator_path = generate_logo_files()
    
    # Copy original file as backup
    copy_original_file()
    
    # Show file information
    show_file_info()
    
    print("✨ Project organization complete!")
    print("\n🎨 Logo Generation:")
    print(f"1. Open {generator_path} in your browser")
    print("2. Select your desired PNG size (50x50, 100x100, 200x200, or 512x512)")
    print("3. Click 'Download PNG Logo' to save the logo file")
    print("4. The PNG will be downloaded to your Downloads folder")
    print("5. Move the PNG file to the images/ folder in your project")
    
    print("\n📖 Next Steps:")
    print("1. Generate your PNG logo using the logo generator")
    print("2. Open html/index.html in your browser")
    print("3. Customize css/styles.css for your design")
    print("4. Extend js/script.js for additional functionality")

if __name__ == "__main__":
    main()
