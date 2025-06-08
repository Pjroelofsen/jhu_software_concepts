# Graduate Application Analysis Project

A comprehensive data analysis project that processes graduate school application data from JSON format, stores it in a PostgreSQL database, performs analytical queries, and displays results through a web interface.

## Project Overview

This project analyzes graduate school application data (originally from Grad Cafe) to provide insights about:
- Application volumes by term
- International vs domestic student percentages  
- Average GPA and GRE scores
- Acceptance rates
- Institution-specific application counts

## Architecture

- **Database**: PostgreSQL with pgAdmin 4
- **Data Processing**: Python with psycopg2
- **Web Interface**: Flask with HTML/CSS
- **Data Format**: JSON input, SQL storage, web display

## File Structure

```
graduate_analysis_project/
├── README.md                           # This file
├── data/
│   └── cleaned_applicant_data_10000_troubleshoot.json  # Input data
├── database_setup/
│   └── load_data.py                    # JSON to PostgreSQL loader
├── analysis/
│   └── query_data.py                   # Standalone query script
└── web_app/
    ├── app.py                          # Flask application
    ├── requirements.txt                # Python dependencies
    └── templates/
        └── analysis.html               # Web interface template
```

## Prerequisites

### Software Requirements
- PostgreSQL (version 12+)
- pgAdmin 4
- Python 3.7+
- pip (Python package manager)

### Python Dependencies
```
Flask==2.3.3
psycopg2-binary==2.9.7
Werkzeug==2.3.7
```

## Setup Instructions

### 1. Database Setup

#### Install PostgreSQL and pgAdmin 4
1. Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. Download and install pgAdmin 4 from [pgadmin.org](https://www.pgadmin.org/download/)

#### Create Database
1. Open pgAdmin 4
2. Connect to your local PostgreSQL server
3. Right-click on "Databases" → "Create" → "Database"
4. Name the database: `module3`
5. Click "Save"

### 2. Data Loading

#### Prepare Data Loading Script (`load_data.py`)
```python
import json
import psycopg2
from datetime import datetime

# Database configuration (update as needed)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'module3',
    'user': 'postgres',
    'port': '5432'
    # No password if using trust authentication
}

# Script creates table and loads JSON data with proper parsing of:
# - GPA values from "GPA 3.75" format
# - GRE scores from "GRE 165", "GRE V 156", "GRE AW 4.00" formats
# - Dates from "Added on March 31, 2024" format
```

#### Database Schema
The script creates a table with the following structure:
```sql
CREATE TABLE application_data (
    p_id SERIAL PRIMARY KEY,
    program TEXT,
    comments TEXT,
    date_added DATE,
    url TEXT,
    status TEXT,
    term TEXT,
    us_or_international TEXT,
    gpa FLOAT,
    gre FLOAT,
    gre_v FLOAT,
    gre_aw FLOAT,
    degree TEXT
);
```

#### Load Data
1. Place your JSON file in the project directory
2. Update the file path in `load_data.py`
3. Run: `python load_data.py`

### 3. Analysis Queries

The project includes 7 analytical queries:

1. **Fall 2024 Application Count**: Total applications for Fall 2024
2. **International Student Percentage**: Percentage of international applicants
3. **Average Academic Metrics**: Mean GPA and GRE scores for reporting applicants
4. **American Student GPA (Fall 2024)**: Average GPA for domestic Fall 2024 applicants
5. **Fall 2024 Acceptance Rate**: Percentage of Fall 2024 applicants accepted
6. **Accepted Student GPA (Fall 2024)**: Average GPA of accepted Fall 2024 applicants
7. **JHU Computer Science Masters**: Count of Johns Hopkins CS Masters applications

### 4. Web Application Setup

#### Install Dependencies
```bash
cd web_app
pip install -r requirements.txt
```

#### Configure Database Connection
Update `app.py` with your PostgreSQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'module3',
    'user': 'postgres',  # Your PostgreSQL username
    'port': '5432'
    # Add 'password': 'your_password' if needed
}
```

#### Run Flask Application
```bash
python app.py
```

#### Access Web Interface
Open browser and navigate to: `http://localhost:5001`

## Usage

### Standalone Query Script
Run individual queries or all queries:
```bash
# Run all queries
python query_data.py -1

# Run specific query (1-7)
python query_data.py 1

# See help
python query_data.py
```

### Web Interface
- Displays all analysis results in a formatted layout
- Automatically executes all queries when page loads
- Responsive design for different screen sizes
- Professional styling matching academic report format

## Key Features

### Data Processing
- **Robust JSON parsing** with error handling
- **Flexible text matching** for variations in university names
- **Date parsing** from natural language format
- **Score extraction** from formatted strings (e.g., "GPA 3.75")

### SQL Query Design
- **NULL-aware aggregation** using `COUNT(column)` vs `COUNT(*)`
- **Pattern matching** with `LIKE`/`ILIKE` for flexible text searches
- **Conditional aggregation** with `CASE WHEN` statements
- **Type-safe operations** with `::NUMERIC` casting
- **Percentage calculations** with proper floating-point arithmetic

### Web Interface
- **Real-time data display** from live database
- **Error handling** for database connectivity issues
- **Professional formatting** with number formatting (commas)
- **Responsive CSS** design

## Sample Results

Based on a dataset of ~22,000 graduate application records:

- **Fall 2024 Applications**: 19,290
- **International Students**: 50.09%
- **Average GPA**: 3.79 (among reporting students)
- **Average GRE Scores**: Quant 164.88, Verbal 160.38, Writing 5.17
- **Fall 2024 Acceptance Rate**: 39.28%
- **Johns Hopkins CS Masters Applications**: 11

## Troubleshooting

### Common Issues

**Database Connection Error**:
- Verify PostgreSQL is running
- Check username/password in configuration
- Ensure database 'module3' exists

**Port 5000 in Use**:
- Flask app uses port 5001 by default
- Change port in `app.py` if needed: `app.run(port=5002)`

**Import Errors**:
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment if needed

**Data Loading Issues**:
- Verify JSON file path and format
- Check PostgreSQL permissions
- Review error messages for specific issues

### Performance Notes
- Database queries optimized for single table scans
- Web interface caches results during page load
- JSON parsing handles ~10,000+ records efficiently

## Technical Details

### SQL Query Optimization
- Uses conditional aggregation instead of subqueries
- Implements proper NULL handling for optional fields
- Employs efficient pattern matching for text searches

### Data Quality Handling
- Handles missing GPA/GRE data gracefully
- Accommodates variations in university name formats
- Manages different status text formats ("Accepted", "Accepted on 21 Feb", etc.)

### Security Considerations
- Uses parameterized queries to prevent SQL injection
- Database connection properly closed after use
- Error messages don't expose sensitive information

## Future Enhancements

Potential improvements could include:
- Data visualization with charts and graphs
- Export functionality for query results
- Advanced filtering and search capabilities
- Historical trend analysis across multiple years
- Institution ranking and comparison features

## License

This project is for educational purposes. Original data courtesy of Grad Cafe community.

## Contact

For questions or issues with this project, please refer to the assignment documentation or course materials.