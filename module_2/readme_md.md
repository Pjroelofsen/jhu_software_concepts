# GradCafe Data Scraper
**Module 1 Assignment - JHU Software Concepts**

## Overview
This project scrapes graduate school admission data from thegradcafe.com to collect comprehensive applicant information including program details, admission decisions, test scores, and demographic data. The scraper is designed to collect at least 10,000 graduate applicant entries while respecting the website's robots.txt policies.

## Requirements Compliance

### ✅ Technical Requirements
- **Python Version**: 3.10+
- **URL Management**: urllib3 library
- **Data Storage**: JSON format in `applicant_data.json`
- **Target Data**: 10,000+ graduate applicant entries
- **Libraries**: Only those covered in Module 2 lecture (urllib3, BeautifulSoup, json, re, standard library)

### ✅ Data Categories Extracted
1. **Program Name** - Name of the academic program
2. **University** - Name of the university/institution  
3. **Comments** - Additional comments from applicant (if available)
4. **Date of Information Added to Grad Café** - When entry was submitted
5. **URL Link to Applicant Entry** - Link to detailed entry page
6. **Applicant Status** - Admission decision outcome
   - **If Accepted**: Acceptance Date
   - **If Rejected**: Rejection Date
7. **Semester and Year of Program Start** - Program timeline (if available)
8. **International / American Student** - Student nationality status (if available)
9. **GRE Score** - Total GRE score (if available)
10. **GRE V Score** - GRE Verbal score (if available)
11. **Masters or PhD** - Degree type (if available)
12. **GPA** - Undergraduate GPA (if available)
13. **GRE AW** - GRE Analytical Writing score (if available)

## Project Structure
```
jhu_software_concepts/
└── module_1/
    ├── scrape.py              # Main scraping functionality
    ├── clean.py               # Data cleaning and processing
    ├── requirements.txt       # Environment dependencies
    ├── README.md             # This documentation
    ├── screenshot.jpg        # robots.txt compliance evidence
    └── applicant_data.json   # Final cleaned data (generated)
```

## Installation and Setup

### 1. Environment Setup
```bash
# Ensure Python 3.10+ is installed
python --version

# Install required packages
pip install -r requirements.txt
```

### 2. Verify robots.txt Compliance
The scraper complies with thegradcafe.com's robots.txt file:
- **Checked**: https://www.thegradcafe.com/robots.txt
- **Status**: Scraping `/survey/` path is ALLOWED
- **Evidence**: See `screenshot.jpg` for robots.txt verification
- **Restrictions**: Only `/cgi-bin/` and `/index-ad-test.php` are disallowed

## Usage

### Step 1: Data Scraping
```bash
python scrape.py
```
This will:
- Scrape data from thegradcafe.com/survey/
- Collect 10,000+ applicant entries
- Save raw data to `raw_scraped_data.json`
- Show progress and statistics

### Step 2: Data Cleaning
```bash
python clean.py
```
This will:
- Process raw scraped data
- Extract all required data categories
- Clean and validate fields
- Save final data to `applicant_data.json`

### Combined Usage
Run both steps sequentially:
```bash
python scrape.py && python clean.py
```

## Code Architecture

### Core Classes and Methods

#### `GradCafeScraper` (scrape.py)
- **`scrape_data()`** - Main scraping method that pulls data from GradCafe
- **`_scrape_single_page()`** - Scrapes individual pages
- **`_extract_page_entries()`** - Extracts entries from page HTML
- **`_find_results_table()`** - Locates data table in HTML

#### `GradCafeDataCleaner` (clean.py)
- **`clean_data()`** - Main cleaning method that converts data into structured format
- **`save_data()`** - Saves cleaned data into JSON file
- **`load_data()`** - Loads data from JSON file
- **`_extract_gre_scores()`** - Private method for GRE score extraction
- **`_extract_gpa()`** - Private method for GPA extraction
- **`_clean_text()`** - Private method for text cleaning

## Data Quality Features

### Data Extraction
- **Regex Patterns**: Advanced pattern matching for test scores, GPAs, and degree types
- **HTML Cleaning**: Removes all HTML tags and formatting
- **Field Validation**: Validates score ranges (GRE: 260-340, GPA: 0.0-4.0)
- **Consistent Format**: Missing data consistently stored as empty strings ""

### Data Completeness
- **Completeness Scoring**: Each entry gets a 0-100% completeness score
- **Field Statistics**: Tracks extraction success rate for each data category
- **Error Handling**: Graceful handling of malformed or missing data

### Respectful Scraping
- **Rate Limiting**: 1-3 second delays between requests
- **Error Recovery**: Retry logic for failed requests
- **Backup System**: Periodic saves every 1000 entries
- **robots.txt Compliance**: Respects website scraping policies

## Output Format

### applicant_data.json Structure
```json
{
  "metadata": {
    "total_applicants": 10000,
    "processing_timestamp": "2025-06-01T...",
    "data_source": "thegradcafe.com",
    "field_descriptions": {...}
  },
  "applicants": [
    {
      "program_name": "Computer Science PhD",
      "university": "Stanford University", 
      "applicant_status": "Accepted",
      "gre_score": "325",
      "gre_v_score": "162",
      "gpa": "3.85",
      "masters_or_phd": "PhD",
      "international_american_student": "International",
      "semester_and_year_program_start": "Fall 2025",
      "data_completeness_percentage": 87
    }
  ],
  "extraction_statistics": {...}
}
```

## Compliance Documentation

### robots.txt Verification
- **URL Checked**: https://www.thegradcafe.com/robots.txt
- **Result**: Scraping allowed for `/survey/` path
- **Screenshot**: `screenshot.jpg` provides visual evidence
- **Compliance**: Full adherence to stated policies

### Library Restrictions
- **urllib3**: URL and HTTP request management
- **BeautifulSoup**: HTML parsing and data extraction  
- **json**: Data storage and manipulation
- **re**: Regex pattern matching for data extraction
- **Standard Library**: time, random, datetime, urllib.parse

### Data Accuracy
- **Source Fidelity**: Data accurately reflects website content
- **No HTML Remnants**: All HTML tags completely removed
- **Validation**: Score ranges and data types validated
- **Consistent Nulls**: Missing data consistently formatted

## Development Notes

### Error Handling
- Network timeouts and connection errors
- Malformed HTML or unexpected page structures  
- Invalid data ranges and formats
- File I/O errors during save/load operations

### Performance Optimization
- Efficient regex compilation and reuse
- Minimal DOM traversal with targeted selectors
- Batch processing with periodic saves
- Memory-efficient streaming for large datasets

### Extensibility
- Modular design allows easy addition of new data categories
- Configurable patterns for different data extraction needs
- Pluggable cleaning and validation functions
- Support for different output formats

## Author Information
- **Course**: JHU Software Concepts
- **Module**: 1 
- **Assignment**: GradCafe Data Scraper
- **Python Version**: 3.10+
- **Date**: June 2025

## License
This project is for educational purposes as part of JHU Software Concepts coursework.