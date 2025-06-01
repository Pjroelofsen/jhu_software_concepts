================================================================================
                        MODULE 1: PERSONAL PORTFOLIO WEBSITE
================================================================================
 
PROJECT OVERVIEW
This is a personal portfolio website built with Flask as part of the Johns 
Hopkins University EN.605.256 Modern Software Concepts Course. The website showcases my 
professional background, contact information, and projects in a clean, 
responsive design.

AUTHOR
Phillip Roelofsen
Systems Engineer at Northrop Grumman
Data Science Student at Johns Hopkins University

FEATURES
- About Page: Professional bio with education, technical skills, and experience
- Contact Page: Contact form, email, and LinkedIn profile
- Projects Page: Showcase of current and future projects
- Responsive Design: Works on desktop and mobile devices
- Clean Navigation: Easy-to-use navigation bar with active page highlighting

TECHNOLOGY STACK
- Backend: Flask (Python web framework)
- Frontend: HTML5, CSS3, Jinja2 templates
- Architecture: Blueprint-based modular design
- Styling: Custom CSS with Poppins font family

PROJECT STRUCTURE
module_1/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── main/
│   │   ├── __init__.py          # Blueprint initialization
│   │   └── routes.py            # Route definitions
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css       # Main stylesheet
│   │   └── images/
│   │       └── profile.jpeg     # Profile photo
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # About page
│       ├── contact.html         # Contact page
│       └── projects.html        # Projects page
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.txt                   # This file

================================================================================
                            INSTALLATION & SETUP
================================================================================

PREREQUISITES
- Python 3.10 or higher
- pip (Python package installer)

STEP-BY-STEP INSTALLATION

1. Clone the repository (if using Git):
   git clone <repository-url>
   cd jhu_software_concepts/module_1

2. Create a virtual environment (recommended):
   python -m venv venv
   
   On Windows:
   venv\Scripts\activate
   
   On macOS/Linux:
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Add your profile image:
   - Place your profile photo as app/static/images/profile.jpeg
   - Or update the image path in templates/index.html

================================================================================
                            RUNNING THE APPLICATION
================================================================================

1. Start the Flask development server:
   python run.py

2. Access the website:
   - Open your web browser
   - Navigate to: http://127.0.0.1:5000/
   - Or: http://localhost:5000/

3. Stop the server:
   - Press Ctrl+C in the terminal

AVAILABLE PAGES
Route          Description
/              About page with professional bio and photo
/contact       Contact information and message form
/projects      Project showcase and GitHub links

================================================================================
                            DEVELOPMENT NOTES
================================================================================

FLASK CONFIGURATION
- Debug Mode: Enabled in development for auto-reload
- Blueprint Structure: Modular design for easy maintenance
- Template Inheritance: Base template for consistent layout

CSS FEATURES
- Responsive Design: Mobile-friendly layout
- Color Scheme: Professional blue theme (#004080)
- Typography: Poppins font family for modern appearance
- Interactive Elements: Hover effects and form styling

SECURITY CONSIDERATIONS
- Contact form includes CSRF protection placeholders
- External links open in new tabs for security
- Input validation on form fields

================================================================================
                                CUSTOMIZATION
================================================================================

UPDATING PERSONAL INFORMATION
1. Bio Content: Edit templates/index.html
2. Contact Details: Update templates/contact.html
3. Projects: Modify templates/projects.html

STYLING CHANGES
- Colors: Update CSS variables in static/css/styles.css
- Fonts: Change font family in CSS file
- Layout: Modify container widths and spacing

ADDING NEW PAGES
1. Create new route in app/main/routes.py
2. Add corresponding HTML template
3. Update navigation in templates/base.html

================================================================================
                              TROUBLESHOOTING
================================================================================

COMMON ISSUES

Port Already in Use:
# Kill process using port 5000
sudo lsof -ti:5000 | xargs sudo kill -9

Module Not Found Error:
# Ensure virtual environment is activated
pip install -r requirements.txt

Template Not Found:
- Check that templates are in app/templates/ directory
- Verify template names match route definitions

CSS Not Loading:
- Ensure CSS file is in app/static/css/ directory
- Clear browser cache (Ctrl+F5)

BROWSER COMPATIBILITY
- Recommended: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Mobile: iOS Safari, Chrome Mobile, Samsung Internet

================================================================================
                              VERSION HISTORY
================================================================================

v1.0: Initial release with core functionality
v1.1: Added responsive design and improved styling
v1.2: Enhanced contact form and project showcase

================================================================================
                                  CONTACT
================================================================================

For questions about this project:
- Email: proelof1@jh.edu
- LinkedIn: https://www.linkedin.com/in/phillip-roelofsen-ab5356189/
- GitHub: https://github.com/Pjroelofsen/jhu_software_concepts/tree/main/module_1

================================================================================
                                  LICENSE
================================================================================

This project is created for educational purposes as part of the Johns Hopkins 
University Modern Software Concepts course.

================================================================================
