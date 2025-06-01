"""
GradCafe Data Cleaning and Processing
Module 1 Assignment - JHU Software Concepts

This module handles cleaning and structuring the raw scraped data from GradCafe
into the final format with all required data categories.

Author: [Your Name]
Date: June 2025
Python Version: 3.10+
"""

import json
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup


class GradCafeDataCleaner:
    """
    Cleans and structures raw GradCafe data into final format
    
    This class processes raw scraped data and extracts specific data categories
    including program details, admission decisions, test scores, and demographic information.
    """
    
    def __init__(self):
        """Initialize the data cleaner with configuration"""
        self.cleaned_entries = []
        self.processing_errors = []
        self.field_extraction_stats = {}
        
        # Initialize statistics tracking
        self._initialize_stats()
    
    def clean_data(self, raw_data_file="raw_scraped_data.json"):
        """
        Main method to clean raw scraped data
        
        Args:
            raw_data_file (str): Path to raw data JSON file
            
        Returns:
            list: Cleaned and structured applicant data
        """
        print(f"Starting data cleaning process...")
        print(f"Loading raw data from: {raw_data_file}")
        
        # Load raw data
        raw_data = self.load_data(raw_data_file)
        
        if not raw_data:
            print("No raw data found to clean.")
            return []
        
        print(f"Processing {len(raw_data)} raw entries...")
        
        # Process each raw entry
        for i, raw_entry in enumerate(raw_data):
            if i % 1000 == 0:
                print(f"Processed {i} entries...")
            
            cleaned_entry = self._clean_single_entry(raw_entry)
            
            if cleaned_entry:
                self.cleaned_entries.append(cleaned_entry)
            else:
                self.processing_errors.append(f"Failed to process entry {i}")
        
        print(f"\nCleaning completed!")
        print(f"Successfully cleaned: {len(self.cleaned_entries)} entries")
        print(f"Processing errors: {len(self.processing_errors)}")
        
        # Print extraction statistics
        self._print_extraction_stats()
        
        return self.cleaned_entries
    
    def _clean_single_entry(self, raw_entry):
        """
        Clean and structure a single raw entry
        
        Args:
            raw_entry (dict): Raw entry data from scraper
            
        Returns:
            dict: Cleaned entry with all required fields, or None if processing failed
        """
        try:
            # Initialize cleaned entry with all required fields
            cleaned_entry = {
                # Required data categories
                "program_name": "",
                "university": "",
                "comments": "",
                "date_information_added": "",
                "url_link_to_applicant_entry": "",
                "applicant_status": "",
                "acceptance_date": "",
                "rejection_date": "",
                "semester_and_year_program_start": "",
                "international_american_student": "",
                "gre_score": "",
                "gre_v_score": "",
                "masters_or_phd": "",
                "gpa": "",
                "gre_aw": "",
                
                # Metadata
                "entry_id": self._generate_entry_id(raw_entry),
                "data_completeness_percentage": 0,
                "cleaning_timestamp": datetime.now().isoformat()
            }
            
            # Extract basic information from cell data
            self._extract_basic_info(raw_entry, cleaned_entry)
            
            # Extract detailed information from text content
            self._extract_detailed_info(raw_entry, cleaned_entry)
            
            # Clean and validate all fields
            self._clean_and_validate_fields(cleaned_entry)
            
            # Calculate data completeness
            cleaned_entry["data_completeness_percentage"] = self._calculate_completeness(cleaned_entry)
            
            # Update extraction statistics
            self._update_extraction_stats(cleaned_entry)
            
            return cleaned_entry
            
        except Exception as error:
            self.processing_errors.append(f"Error cleaning entry: {str(error)}")
            return None
    
    def _extract_basic_info(self, raw_entry, cleaned_entry):
        """
        Extract basic information from cell data
        
        Args:
            raw_entry (dict): Raw entry data
            cleaned_entry (dict): Cleaned entry to populate
        """
        cell_data = raw_entry.get('cell_data', [])
        
        # Map cell data to basic fields (typical GradCafe column order)
        if len(cell_data) >= 1:
            cleaned_entry["university"] = self._clean_text(cell_data[0])
        
        if len(cell_data) >= 2:
            cleaned_entry["program_name"] = self._clean_text(cell_data[1])
        
        if len(cell_data) >= 3:
            cleaned_entry["applicant_status"] = self._clean_text(cell_data[2])
        
        if len(cell_data) >= 5:
            cleaned_entry["date_information_added"] = self._clean_date(cell_data[4])
        
        # Set URL link
        cleaned_entry["url_link_to_applicant_entry"] = raw_entry.get('entry_detail_url', raw_entry.get('page_url', ''))
    
    def _extract_detailed_info(self, raw_entry, cleaned_entry):
        """
        Extract detailed information using regex patterns
        
        Args:
            raw_entry (dict): Raw entry data
            cleaned_entry (dict): Cleaned entry to populate
        """
        # Get all text content for pattern matching
        text_content = raw_entry.get('row_text', '')
        html_content = raw_entry.get('html_content', '')
        
        # Remove HTML tags for cleaner text processing
        clean_text = self._remove_html_tags(html_content + ' ' + text_content)
        
        # Extract specific data categories using regex patterns
        self._extract_gre_scores(clean_text, cleaned_entry)
        self._extract_gpa(clean_text, cleaned_entry)
        self._extract_degree_type(clean_text, cleaned_entry)
        self._extract_student_status(clean_text, cleaned_entry)
        self._extract_semester_year(clean_text, cleaned_entry)
        self._extract_decision_dates(clean_text, cleaned_entry)
        self._extract_comments(clean_text, cleaned_entry)
    
    def _extract_gre_scores(self, text, cleaned_entry):
        """
        Extract GRE scores using regex patterns
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        text_lower = text.lower()
        
        # GRE Total Score (typically 260-340 range)
        gre_total_patterns = [
            r'gre\s*(?:total)?\s*[:=]?\s*(\d{3})',
            r'total\s*gre\s*[:=]?\s*(\d{3})',
            r'gre\s*(\d{3})',
            r'(\d{3})\s*gre'
        ]
        
        for pattern in gre_total_patterns:
            match = re.search(pattern, text_lower)
            if match:
                score = int(match.group(1))
                if 260 <= score <= 340:  # Valid GRE range
                    cleaned_entry["gre_score"] = str(score)
                    break
        
        # GRE Verbal Score (130-170 range)
        gre_verbal_patterns = [
            r'(?:gre\s*)?v(?:erbal)?\s*[:=]?\s*(\d{2,3})',
            r'verbal\s*[:=]?\s*(\d{2,3})',
            r'v\s*(\d{2,3})',
            r'(\d{2,3})\s*v(?:erbal)?'
        ]
        
        for pattern in gre_verbal_patterns:
            match = re.search(pattern, text_lower)
            if match:
                score = int(match.group(1))
                if 130 <= score <= 170:  # Valid GRE Verbal range
                    cleaned_entry["gre_v_score"] = str(score)
                    break
        
        # GRE Analytical Writing (0.0-6.0 range)
        gre_aw_patterns = [
            r'(?:gre\s*)?(?:aw|analytical\s*writing|writing)\s*[:=]?\s*(\d(?:\.\d)?)',
            r'aw\s*[:=]?\s*(\d(?:\.\d)?)',
            r'writing\s*[:=]?\s*(\d(?:\.\d)?)'
        ]
        
        for pattern in gre_aw_patterns:
            match = re.search(pattern, text_lower)
            if match:
                score = float(match.group(1))
                if 0.0 <= score <= 6.0:  # Valid GRE AW range
                    cleaned_entry["gre_aw"] = str(score)
                    break
    
    def _extract_gpa(self, text, cleaned_entry):
        """
        Extract GPA using regex patterns
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        text_lower = text.lower()
        
        gpa_patterns = [
            r'gpa\s*[:=]?\s*(\d\.\d{1,2})',
            r'(\d\.\d{1,2})\s*gpa',
            r'(?:undergraduate|undergrad)\s*gpa\s*[:=]?\s*(\d\.\d{1,2})',
            r'cgpa\s*[:=]?\s*(\d\.\d{1,2})'
        ]
        
        for pattern in gpa_patterns:
            match = re.search(pattern, text_lower)
            if match:
                gpa_value = float(match.group(1))
                if 0.0 <= gpa_value <= 4.0:  # Valid GPA range
                    cleaned_entry["gpa"] = str(gpa_value)
                    break
    
    def _extract_degree_type(self, text, cleaned_entry):
        """
        Extract degree type (Masters or PhD)
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        text_lower = text.lower()
        
        # Check for PhD indicators
        phd_patterns = [r'\bphd\b', r'\bph\.d\b', r'\bdoctorate\b', r'\bdoctoral\b']
        for pattern in phd_patterns:
            if re.search(pattern, text_lower):
                cleaned_entry["masters_or_phd"] = "PhD"
                return
        
        # Check for Masters indicators
        masters_patterns = [
            r'\bmasters?\b', r'\bmaster\b', r'\bms\b', r'\bm\.s\b', 
            r'\bma\b', r'\bm\.a\b', r'\bmeng\b', r'\bmba\b'
        ]
        for pattern in masters_patterns:
            if re.search(pattern, text_lower):
                cleaned_entry["masters_or_phd"] = "Masters"
                return
    
    def _extract_student_status(self, text, cleaned_entry):
        """
        Extract international/American student status
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        text_lower = text.lower()
        
        # Check for international student indicators
        international_patterns = [
            r'\binternational\b', r'\bintl\b', r'\bforeign\b', 
            r'\bf1\b', r'\bvisa\b', r'\bnon-us\b'
        ]
        for pattern in international_patterns:
            if re.search(pattern, text_lower):
                cleaned_entry["international_american_student"] = "International"
                return
        
        # Check for domestic/American student indicators
        domestic_patterns = [
            r'\bdomestic\b', r'\bamerican\b', r'\bus\b', r'\busa\b', 
            r'\bcitizen\b', r'\bnative\b'
        ]
        for pattern in domestic_patterns:
            if re.search(pattern, text_lower):
                cleaned_entry["international_american_student"] = "American"
                return
    
    def _extract_semester_year(self, text, cleaned_entry):
        """
        Extract semester and year of program start
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        text_lower = text.lower()
        
        # Patterns for semester and year combinations
        semester_year_patterns = [
            r'(fall|spring|summer|winter)\s*(\d{4})',
            r'(\d{4})\s*(fall|spring|summer|winter)',
            r'(fall|spring|summer|winter)\s*[\'"]?(\d{2})'
        ]
        
        for pattern in semester_year_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.group(2)) == 2:  # Convert 2-digit year
                    year = "20" + match.group(2)
                else:
                    year = match.group(2)
                
                semester = match.group(1).title()
                cleaned_entry["semester_and_year_program_start"] = f"{semester} {year}"
                return
        
        # If no semester found, just look for year
        year_pattern = r'\b(20\d{2})\b'
        year_match = re.search(year_pattern, text)
        if year_match:
            year = year_match.group(1)
            if 2020 <= int(year) <= 2030:  # Reasonable year range
                cleaned_entry["semester_and_year_program_start"] = year
    
    def _extract_decision_dates(self, text, cleaned_entry):
        """
        Extract acceptance/rejection dates based on applicant status
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        status = cleaned_entry.get("applicant_status", "").lower()
        date_added = cleaned_entry.get("date_information_added", "")
        
        if "accept" in status or "admit" in status:
            cleaned_entry["acceptance_date"] = date_added
        elif "reject" in status or "denied" in status:
            cleaned_entry["rejection_date"] = date_added
    
    def _extract_comments(self, text, cleaned_entry):
        """
        Extract comments and additional notes
        
        Args:
            text (str): Text content to search
            cleaned_entry (dict): Entry to populate
        """
        # Use the cleaned text as comments if it contains useful information
        if len(text) > 50:  # Only if substantial content
            cleaned_text = self._clean_text(text)
            # Remove redundant information already captured in other fields
            if not any(field in cleaned_text.lower() for field in ['gre', 'gpa', 'phd', 'masters']):
                cleaned_entry["comments"] = cleaned_text[:500]  # Limit length
    
    def _clean_text(self, text):
        """
        Clean text by removing extra whitespace and unwanted characters
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = re.sub(r'\s+', ' ', str(text).strip())
        
        # Remove non-printable characters
        cleaned = re.sub(r'[^\x20-\x7E]', '', cleaned)
        
        return cleaned
    
    def _clean_date(self, date_text):
        """
        Clean and standardize date format
        
        Args:
            date_text (str): Date text to clean
            
        Returns:
            str: Cleaned date string
        """
        if not date_text:
            return ""
        
        # Clean the date text
        cleaned_date = self._clean_text(date_text)
        
        # Basic date validation - could be enhanced with more sophisticated parsing
        return cleaned_date
    
    def _remove_html_tags(self, html_text):
        """
        Remove HTML tags from text content
        
        Args:
            html_text (str): Text containing HTML tags
            
        Returns:
            str: Text with HTML tags removed
        """
        if not html_text:
            return ""
        
        # Use BeautifulSoup to parse and extract text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def _clean_and_validate_fields(self, cleaned_entry):
        """
        Clean and validate all fields in the entry
        
        Args:
            cleaned_entry (dict): Entry to clean and validate
        """
        # Ensure all required fields exist and are properly formatted
        required_fields = [
            "program_name", "university", "comments", "date_information_added",
            "url_link_to_applicant_entry", "applicant_status", "acceptance_date",
            "rejection_date", "semester_and_year_program_start", 
            "international_american_student", "gre_score", "gre_v_score",
            "masters_or_phd", "gpa", "gre_aw"
        ]
        
        for field in required_fields:
            if field not in cleaned_entry or cleaned_entry[field] is None:
                cleaned_entry[field] = ""
            else:
                # Clean the field value
                cleaned_entry[field] = self._clean_text(str(cleaned_entry[field]))
    
    def _calculate_completeness(self, cleaned_entry):
        """
        Calculate data completeness percentage
        
        Args:
            cleaned_entry (dict): Cleaned entry
            
        Returns:
            int: Completeness percentage (0-100)
        """
        important_fields = [
            "program_name", "university", "applicant_status", "gre_score",
            "gpa", "masters_or_phd", "international_american_student",
            "semester_and_year_program_start"
        ]
        
        filled_fields = sum(1 for field in important_fields if cleaned_entry.get(field))
        return round((filled_fields / len(important_fields)) * 100)
    
    def _generate_entry_id(self, raw_entry):
        """
        Generate unique entry ID
        
        Args:
            raw_entry (dict): Raw entry data
            
        Returns:
            str: Unique entry identifier
        """
        # Create ID based on content hash
        content = str(raw_entry.get('row_text', '')) + str(raw_entry.get('page_url', ''))
        hash_value = hash(content) % 1000000
        return f"gc_{abs(hash_value):06d}"
    
    def _initialize_stats(self):
        """Initialize extraction statistics tracking"""
        self.field_extraction_stats = {
            "program_name": 0,
            "university": 0,
            "applicant_status": 0,
            "gre_score": 0,
            "gre_v_score": 0,
            "gre_aw": 0,
            "gpa": 0,
            "masters_or_phd": 0,
            "international_american_student": 0,
            "semester_and_year_program_start": 0
        }
    
    def _update_extraction_stats(self, cleaned_entry):
        """
        Update extraction statistics
        
        Args:
            cleaned_entry (dict): Cleaned entry data
        """
        for field in self.field_extraction_stats:
            if cleaned_entry.get(field):
                self.field_extraction_stats[field] += 1
    
    def _print_extraction_stats(self):
        """Print extraction statistics"""
        print(f"\n=== Data Extraction Statistics ===")
        total_entries = len(self.cleaned_entries)
        
        for field, count in self.field_extraction_stats.items():
            percentage = (count / total_entries * 100) if total_entries > 0 else 0
            print(f"{field}: {count}/{total_entries} ({percentage:.1f}%)")
    
    def save_data(self, cleaned_data, filename="applicant_data.json"):
        """
        Save cleaned data to JSON file with reasonable object keys
        
        Args:
            cleaned_data (list): Cleaned applicant data
            filename (str): Output filename
        """
        print(f"Saving cleaned data to {filename}...")
        
        # Structure data with metadata and reasonable object keys
        output_data = {
            "metadata": {
                "total_applicants": len(cleaned_data),
                "processing_timestamp": datetime.now().isoformat(),
                "data_source": "thegradcafe.com",
                "cleaning_version": "1.0",
                "processing_errors": len(self.processing_errors),
                "field_descriptions": {
                    "program_name": "Name of the academic program",
                    "university": "Name of the university/institution",
                    "comments": "Additional comments from applicant",
                    "date_information_added": "Date entry was added to GradCafe",
                    "url_link_to_applicant_entry": "URL to the detailed entry",
                    "applicant_status": "Admission decision (Accepted/Rejected/etc.)",
                    "acceptance_date": "Date of acceptance (if accepted)",
                    "rejection_date": "Date of rejection (if rejected)",
                    "semester_and_year_program_start": "Program start semester and year",
                    "international_american_student": "Student nationality status",
                    "gre_score": "Total GRE score",
                    "gre_v_score": "GRE Verbal score",
                    "masters_or_phd": "Degree type (Masters/PhD)",
                    "gpa": "Undergraduate GPA",
                    "gre_aw": "GRE Analytical Writing score"
                }
            },
            "applicants": cleaned_data,
            "extraction_statistics": self.field_extraction_stats
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as output_file:
                json.dump(output_data, output_file, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {len(cleaned_data)} cleaned entries to {filename}")
            
        except Exception as error:
            print(f"Error saving data: {str(error)}")
    
    def load_data(self, filename):
        """
        Load data from JSON file
        
        Args:
            filename (str): Input filename
            
        Returns:
            list: Loaded data, or empty list if failed
        """
        try:
            with open(filename, 'r', encoding='utf-8') as input_file:
                data = json.load(input_file)
            
            # Handle different data structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'applicants' in data:
                return data['applicants']
            else:
                return data
                
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return []
        except json.JSONDecodeError as error:
            print(f"Error parsing JSON from {filename}: {str(error)}")
            return []
        except Exception as error:
            print(f"Error loading data from {filename}: {str(error)}")
            return []


def main():
    """
    Main function to run the data cleaning process
    """
    print("="*60)
    print("GradCafe Data Cleaning - Module 1 Assignment")
    print("="*60)
    
    # Check if raw data file exists
    raw_file = "raw_scraped_data.json"
    if not os.path.exists(raw_file):
        print(f"❌ Error: {raw_file} not found!")
        print("Please run scraping first:")
        print("  python scrape.py")
        print("Or run the complete pipeline:")
        print("  python main.py")
        return
    
    # Initialize cleaner
    cleaner = GradCafeDataCleaner()
    
    # Clean the raw data
    cleaned_data = cleaner.clean_data(raw_file)
    
    if cleaned_data:
        # Save cleaned data to applicant_data.json
        cleaner.save_data(cleaned_data, "applicant_data.json")
        
        # Print summary
        print(f"\n=== Processing Summary ===")
        print(f"Total entries processed: {len(cleaned_data)}")
        print(f"Processing errors: {len(cleaner.processing_errors)}")
        
        # Show sample data
        if cleaned_data:
            print(f"\n=== Sample Cleaned Entry ===")
            sample_entry = cleaned_data[0]
            for key, value in sample_entry.items():
                if key not in ['entry_id', 'cleaning_timestamp'] and value:
                    print(f"{key}: {value}")
        
        print(f"\nCleaned data saved to applicant_data.json")
        
    else:
        print("No data was cleaned. Please check the raw data file.")


if __name__ == "__main__":
    main()