"""
GradCafe Data Cleaner
Module 1 Assignment - JHU Software Concepts

This module processes the raw scraped data from scrape.py and generates
a clean, filtered JSON file with only the specified fields.

Input: gradcafe_complete_data.json (from scraper)
Output: applicant_data.json (clean, filtered data)

Author: [Your Name]
Date: June 2025
Python Version: 3.10+
"""

import json
import re
from datetime import datetime
import os


class GradCafeDataCleaner:
    """
    Cleans and filters GradCafe scraped data
    """
    
    def __init__(self, input_file="gradcafe_complete_data.json", output_file="applicant_data.json"):
        """
        Initialize the data cleaner
        
        Args:
            input_file (str): Path to raw scraped data JSON file
            output_file (str): Path to output clean data JSON file
        """
        self.input_file = input_file
        self.output_file = output_file
        
        # Fields to extract and include in clean data
        self.target_fields = [
            'institution',
            'program', 
            'notes',
            'added_on_date',
            'entry_url',
            'decision',
            'country_origin',
            'degree_type'
        ]
        
        # Statistics tracking
        self.total_entries_processed = 0
        self.entries_with_all_fields = 0
        self.entries_with_notes = 0
        self.missing_field_counts = {}
        
    def clean_data(self):
        """
        Main method to clean and filter the scraped data
        
        Returns:
            list: Cleaned and filtered data entries
        """
        print("="*60)
        print("GradCafe Data Cleaner")
        print("="*60)
        print(f"Input file: {self.input_file}")
        print(f"Output file: {self.output_file}")
        print(f"Target fields: {', '.join(self.target_fields)}")
        
        # Load raw data
        raw_data = self._load_raw_data()
        if not raw_data:
            print("❌ No raw data loaded. Exiting.")
            return []
        
        print(f"\n✅ Loaded {len(raw_data)} raw entries")
        
        # Clean and filter data
        print(f"\n{'='*60}")
        print("CLEANING AND FILTERING DATA")
        print(f"{'='*60}")
        
        clean_data = []
        for i, raw_entry in enumerate(raw_data):
            clean_entry = self._clean_single_entry(raw_entry, i+1)
            if clean_entry:
                clean_data.append(clean_entry)
        
        # Save clean data
        if clean_data:
            self._save_clean_data(clean_data)
            self._print_statistics(clean_data)
        
        return clean_data
    
    def _load_raw_data(self):
        """
        Load raw scraped data from JSON file
        
        Returns:
            list: Raw data entries or empty list if file not found
        """
        if not os.path.exists(self.input_file):
            print(f"❌ Input file '{self.input_file}' not found!")
            print("   Make sure you've run scrape.py first to generate the data.")
            return []
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return data
            else:
                print(f"❌ Expected list data, got {type(data)}")
                return []
                
        except Exception as e:
            print(f"❌ Error loading {self.input_file}: {e}")
            return []
    
    def _clean_single_entry(self, raw_entry, entry_num):
        """
        Clean and filter a single entry
        
        Args:
            raw_entry (dict): Raw entry from scraper
            entry_num (int): Entry number for logging
            
        Returns:
            dict: Clean entry with target fields only
        """
        self.total_entries_processed += 1
        
        # Create clean entry with only target fields
        clean_entry = {
            'entry_id': raw_entry.get('entry_id'),  # Keep entry_id for reference
            'processing_timestamp': datetime.now().isoformat()
        }
        
        # Extract and clean each target field
        fields_found = 0
        for field in self.target_fields:
            value = self._extract_and_clean_field(raw_entry, field)
            if value is not None:
                clean_entry[field] = value
                fields_found += 1
            else:
                # Track missing fields
                if field not in self.missing_field_counts:
                    self.missing_field_counts[field] = 0
                self.missing_field_counts[field] += 1
        
        # Statistics tracking
        if fields_found == len(self.target_fields):
            self.entries_with_all_fields += 1
        
        if clean_entry.get('notes', '').strip():
            self.entries_with_notes += 1
        
        # Show progress every 10 entries
        if entry_num % 10 == 0 or entry_num <= 5:
            institution = clean_entry.get('institution', 'Unknown')[:30]
            program = clean_entry.get('program', 'Unknown')[:30] 
            decision = clean_entry.get('decision', 'Unknown')
            notes_len = len(clean_entry.get('notes', ''))
            print(f"  Entry {entry_num}: {institution} | {program} | {decision} | Notes: {notes_len} chars")
        
        return clean_entry
    
    def _extract_and_clean_field(self, raw_entry, field_name):
        """
        Extract and clean a specific field from raw entry
        
        Args:
            raw_entry (dict): Raw entry data
            field_name (str): Name of field to extract
            
        Returns:
            str or None: Cleaned field value or None if not found/empty
        """
        # Try to get the field value from different possible keys
        possible_keys = [
            field_name,
            f"table_{field_name}",  # Table data
            field_name.replace('_', ' '),  # Convert underscores to spaces
        ]
        
        value = None
        for key in possible_keys:
            if key in raw_entry and raw_entry[key]:
                value = raw_entry[key]
                break
        
        if not value:
            return None
        
        # Clean the value based on field type
        if field_name == 'institution':
            return self._clean_institution(value)
        elif field_name == 'program':
            return self._clean_program(value)
        elif field_name == 'notes':
            return self._clean_notes(value)
        elif field_name == 'added_on_date':
            return self._clean_date(value)
        elif field_name == 'entry_url':
            return self._clean_url(value)
        elif field_name == 'decision':
            return self._clean_decision(value)
        elif field_name == 'country_origin':
            return self._clean_country_origin(value)
        elif field_name == 'degree_type':
            return self._clean_degree_type(value)
        else:
            return self._clean_generic_text(value)
    
    def _clean_institution(self, value):
        """Clean institution name"""
        if not value or value.strip() in ['Unknown', '-', 'N/A']:
            return None
        
        # Clean up institution name
        cleaned = value.strip()
        
        # Remove common suffixes that might be inconsistent
        suffixes_to_standardize = {
            ' Univ': ' University',
            ' U ': ' University ',
            ' Tech': ' Institute of Technology'
        }
        
        for old, new in suffixes_to_standardize.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned if len(cleaned) > 2 else None
    
    def _clean_program(self, value):
        """Clean program name"""
        if not value or value.strip() in ['Unknown', '-', 'N/A']:
            return None
        
        cleaned = value.strip()
        
        # Standardize common program abbreviations
        program_standardizations = {
            'CS': 'Computer Science',
            'EE': 'Electrical Engineering', 
            'ME': 'Mechanical Engineering',
            'Bio': 'Biology',
            'Chem': 'Chemistry',
            'Math': 'Mathematics',
            'Phys': 'Physics'
        }
        
        # Only apply if the value is exactly the abbreviation
        if cleaned in program_standardizations:
            cleaned = program_standardizations[cleaned]
        
        return cleaned if len(cleaned) > 1 else None
    
    def _clean_notes(self, value):
        """Clean notes text"""
        if not value:
            return None
        
        cleaned = value.strip()
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common boilerplate text
        boilerplate_patterns = [
            r'Details and information about the application\.',
            r'This data is estimated based on applicant submissions at The GradCafe\.',
        ]
        
        for pattern in boilerplate_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        cleaned = cleaned.strip()
        
        # Return None if notes are too short to be meaningful
        return cleaned if len(cleaned) > 5 else None
    
    def _clean_date(self, value):
        """Clean date field"""
        if not value:
            return None
        
        # Return the date as-is if it looks reasonable
        cleaned = str(value).strip()
        
        # Basic validation - should contain numbers
        if re.search(r'\d', cleaned) and len(cleaned) > 4:
            return cleaned
        
        return None
    
    def _clean_url(self, value):
        """Clean URL field"""
        if not value:
            return None
        
        cleaned = str(value).strip()
        
        # Basic URL validation
        if cleaned.startswith('http') and 'gradcafe.com' in cleaned:
            return cleaned
        
        return None
    
    def _clean_decision(self, value):
        """Clean decision field"""
        if not value:
            return None
        
        cleaned = value.strip().lower()
        
        # Standardize decision values
        if 'accept' in cleaned:
            return 'Accepted'
        elif 'reject' in cleaned or 'denied' in cleaned:
            return 'Rejected'
        elif 'waitlist' in cleaned:
            return 'Waitlisted'
        elif 'interview' in cleaned:
            return 'Interview'
        else:
            # Return original if it doesn't match standard patterns
            return value.strip() if len(value.strip()) > 0 else None
    
    def _clean_country_origin(self, value):
        """Clean country of origin field"""
        if not value or value.strip() in ['Unknown', '-', 'N/A']:
            return None
        
        cleaned = value.strip()
        
        # Standardize common values
        country_standardizations = {
            'US': 'United States',
            'USA': 'United States', 
            'UK': 'United Kingdom',
            'International': 'International',
            'Domestic': 'United States'
        }
        
        if cleaned in country_standardizations:
            return country_standardizations[cleaned]
        
        return cleaned if len(cleaned) > 1 else None
    
    def _clean_degree_type(self, value):
        """Clean degree type field"""
        if not value or value.strip() in ['Unknown', '-', 'N/A']:
            return None
        
        cleaned = value.strip()
        
        # Standardize degree types
        degree_standardizations = {
            'PhD': 'PhD',
            'Ph.D.': 'PhD',
            'Ph.D': 'PhD',
            'Masters': 'Masters',
            'Master\'s': 'Masters',
            'MS': 'Masters',
            'M.S.': 'Masters',
            'MA': 'Masters',
            'M.A.': 'Masters',
            'MBA': 'MBA',
            'M.B.A.': 'MBA'
        }
        
        if cleaned in degree_standardizations:
            return degree_standardizations[cleaned]
        
        return cleaned if len(cleaned) > 1 else None
    
    def _clean_generic_text(self, value):
        """Clean generic text field"""
        if not value:
            return None
        
        cleaned = str(value).strip()
        return cleaned if len(cleaned) > 0 else None
    
    def _save_clean_data(self, clean_data):
        """Save cleaned data to JSON file"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Clean data saved to '{self.output_file}'")
            
        except Exception as e:
            print(f"\n❌ Error saving clean data: {e}")
    
    def _print_statistics(self, clean_data):
        """Print cleaning statistics"""
        print(f"\n{'='*60}")
        print("CLEANING STATISTICS")
        print(f"{'='*60}")
        
        print(f"Total entries processed: {self.total_entries_processed}")
        print(f"Clean entries output: {len(clean_data)}")
        print(f"Entries with all fields: {self.entries_with_all_fields}")
        print(f"Entries with notes: {self.entries_with_notes}")
        
        # Field coverage
        print(f"\n=== Field Coverage ===")
        for field in self.target_fields:
            present_count = len([e for e in clean_data if e.get(field)])
            coverage = (present_count / len(clean_data)) * 100 if clean_data else 0
            print(f"{field}: {present_count}/{len(clean_data)} ({coverage:.1f}%)")
        
        # Missing field summary
        if self.missing_field_counts:
            print(f"\n=== Missing Fields Summary ===")
            for field, count in sorted(self.missing_field_counts.items()):
                print(f"{field}: {count} missing")
        
        # Decision distribution
        decisions = {}
        for entry in clean_data:
            decision = entry.get('decision', 'Unknown')
            decisions[decision] = decisions.get(decision, 0) + 1
        
        if decisions:
            print(f"\n=== Decision Distribution ===")
            for decision, count in sorted(decisions.items()):
                percentage = (count / len(clean_data)) * 100
                print(f"{decision}: {count} ({percentage:.1f}%)")


def main():
    """
    Main function to run the data cleaner
    """
    # Initialize cleaner
    cleaner = GradCafeDataCleaner()
    
    # Clean the data
    clean_data = cleaner.clean_data()
    
    if clean_data:
        print(f"\n✅ Successfully cleaned {len(clean_data)} entries")
        
        # Show sample clean entries
        print(f"\n=== Sample Clean Entries ===")
        for i, entry in enumerate(clean_data[:3]):
            print(f"\nClean Entry {i+1}:")
            for field in cleaner.target_fields:
                value = entry.get(field, 'Not found')
                if field == 'notes' and len(str(value)) > 100:
                    print(f"  {field}: {str(value)[:100]}...")
                else:
                    print(f"  {field}: {value}")
    else:
        print("\n❌ No clean data generated")


if __name__ == "__main__":
    main()