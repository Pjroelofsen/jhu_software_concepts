"""
GradCafe Data Scraper (Season Code Enhanced Version)
Module 1 Assignment - JHU Software Concepts

This module handles scraping data from thegradcafe.com by:
1. First scraping the main results table to get entry IDs + "Added On" dates + Season codes
2. Then fetching each individual entry page for detailed data + notes
3. Outputs single JSON file with complete data including season information

Enhanced to detect GradCafe season codes (F25=Fall 2025, S25=Spring 2025, etc.)

Author: [Your Name]
Date: June 2025
Python Version: 3.10+
"""

import urllib3
from bs4 import BeautifulSoup
import json
import time
import random
import re
from datetime import datetime
from urllib.parse import urljoin


class GradCafeScraper:
    """
    Scrapes graduate school admission data from thegradcafe.com using hybrid approach
    """
    
    def __init__(self):
        """Initialize the scraper with base configuration"""
        self.base_url = "https://www.thegradcafe.com"
        self.survey_url = f"{self.base_url}/survey"
        
        # Disable SSL warnings if needed
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Initialize urllib3 pool manager
        self.http_pool = urllib3.PoolManager(
            cert_reqs='CERT_NONE',  # Skip SSL verification if needed
            timeout=30.0
        )
        
        # Headers to simulate browser
        self.request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.thegradcafe.com/survey/'
        }
        
        # Track statistics
        self.total_pages_scraped = 0
        self.total_entries_found_in_table = 0
        self.total_entries_processed = 0
        self.entries_with_notes = 0
        self.failed_page_requests = 0
        self.failed_entry_requests = 0
    
    def scrape_data(self, target_entries=1000, max_pages=50, start_page=1):
        """
        Main method to scrape data using hybrid approach
        
        Args:
            target_entries (int): Target number of entries to collect
            max_pages (int): Maximum pages to scrape
            start_page (int): Starting page number
            
        Returns:
            list: Complete dataset with reliable data extraction
        """
        print(f"Starting GradCafe scraping for {target_entries} entries...")
        print(f"Step 1: Get entry IDs + 'Added On' dates + Season codes from results table")
        print(f"Step 2: Get detailed data + notes from individual entry pages")
        print(f"Step 3: Combine for complete dataset")
        
        # Step 1: Collect entry metadata from results table pages
        print(f"\n{'='*60}")
        print("STEP 1: Collecting entry IDs, 'Added On' dates, and Season codes from results tables")
        print(f"{'='*60}")
        
        entry_metadata = self._collect_entry_metadata(max_pages, start_page, target_entries)
        
        if not entry_metadata:
            print("❌ No entry metadata found. Cannot proceed.")
            return []
        
        print(f"✅ Collected metadata for {len(entry_metadata)} entries")
        
        # Step 2: Fetch detailed data from individual entry pages
        print(f"\n{'='*60}")
        print("STEP 2: Fetching detailed data from individual entries")
        print(f"{'='*60}")
        
        complete_entries = self._fetch_detailed_entries(entry_metadata)
        
        print(f"\n{'='*60}")
        print(f"Scraping completed!")
        print(f"Total pages scraped: {self.total_pages_scraped}")
        print(f"Entries found in tables: {self.total_entries_found_in_table}")
        print(f"Individual entries processed: {self.total_entries_processed}")
        print(f"Entries with notes: {self.entries_with_notes}")
        print(f"Failed page requests: {self.failed_page_requests}")
        print(f"Failed entry requests: {self.failed_entry_requests}")
        print(f"{'='*60}\n")
        
        # Save final data (single JSON file)
        if complete_entries:
            self._save_complete_data(complete_entries)
        
        return complete_entries
    
    def _collect_entry_metadata(self, max_pages, start_page, target_entries):
        """
        Collect entry IDs, "Added On" dates, and Season codes from results table pages
        
        Returns:
            list: List of dicts with entry_id, entry_url, added_on_date, season
        """
        all_metadata = []
        current_page = start_page
        consecutive_empty_pages = 0
        
        while (len(all_metadata) < target_entries and 
               current_page <= max_pages and 
               consecutive_empty_pages < 3):
            
            print(f"\nScraping page {current_page} for metadata... (Current entries: {len(all_metadata)})")
            
            page_metadata = self._scrape_metadata_from_page(current_page)
            
            if page_metadata:
                all_metadata.extend(page_metadata)
                consecutive_empty_pages = 0
                self.total_entries_found_in_table += len(page_metadata)
                print(f"✓ Found {len(page_metadata)} entries with metadata on page {current_page}")
            else:
                consecutive_empty_pages += 1
                print(f"✗ No metadata found on page {current_page}")
            
            current_page += 1
            self.total_pages_scraped += 1
            
            # Random delay between requests
            delay = random.uniform(1.0, 2.0)
            print(f"Waiting {delay:.1f} seconds...")
            time.sleep(delay)
        
        # Limit to target entries
        if len(all_metadata) > target_entries:
            all_metadata = all_metadata[:target_entries]
            print(f"Limited to first {target_entries} entries")
        
        return all_metadata
    
    def _scrape_metadata_from_page(self, page_number):
        """
        Scrape entry metadata from a single results table page
        
        Args:
            page_number (int): Page number to scrape
            
        Returns:
            list: List of metadata dicts for entries on this page
        """
        # Try different URL patterns for GradCafe results pages
        url_patterns = [
            f"{self.survey_url}/index.php?q=&t=a&o=&pp=250&p={page_number}",
            f"{self.survey_url}/?page={page_number}",
            f"{self.survey_url}/index.php?page={page_number}",
            f"{self.survey_url}/index.php?p={page_number}",
        ]
        
        for url in url_patterns:
            print(f"  Trying URL: {url}")
            page_metadata = self._extract_metadata_from_page(url)
            if page_metadata:
                return page_metadata
        
        return []
    
    def _extract_metadata_from_page(self, page_url):
        """
        Extract entry metadata from a single page
        
        Args:
            page_url (str): URL of the results page
            
        Returns:
            list: List of metadata dicts
        """
        try:
            # Make HTTP request
            response = self.http_pool.request(
                'GET', 
                page_url, 
                headers=self.request_headers,
                timeout=30.0,
                retries=3
            )
            
            if response.status != 200:
                print(f"    HTTP {response.status} error")
                self.failed_page_requests += 1
                return []
            
            # Decode response
            try:
                content = response.data.decode('utf-8')
            except:
                try:
                    content = response.data.decode('latin-1')
                except:
                    content = response.data.decode('utf-8', errors='ignore')
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract entry metadata from the results table
            entry_metadata = self._parse_results_table(soup)
            
            return entry_metadata
            
        except Exception as error:
            print(f"    Error: {str(error)}")
            self.failed_page_requests += 1
            return []
    
    def _parse_results_table(self, soup):
        """
        Parse the results table to extract entry IDs and "Added On" dates
        
        Args:
            soup (BeautifulSoup): Parsed HTML of results page
            
        Returns:
            list: List of metadata dicts
        """
        metadata_list = []
        
        # Find the results table
        table = self._find_results_table(soup)
        if not table:
            print("    Warning: Could not find results table")
            return []
        
        # Get all table rows
        rows = table.find_all('tr')
        print(f"    Found table with {len(rows)} rows")
        
        if len(rows) < 2:
            print("    Warning: Table has insufficient rows")
            return []
        
        # Analyze header row to find column positions
        header_row = rows[0]
        column_mapping = self._analyze_table_headers(header_row)
        
        # Process data rows (skip header)
        data_rows = rows[1:]
        
        for i, row in enumerate(data_rows):
            metadata = self._extract_row_metadata(row, column_mapping)
            if metadata:
                metadata_list.append(metadata)
                
                if i == 0:  # Debug first row
                    print(f"    Sample metadata: ID={metadata.get('entry_id')}, Added On={metadata.get('added_on_date')}, Season={metadata.get('season')}")
        
        return metadata_list
    
    def _find_results_table(self, soup):
        """
        Find the main results table on the page
        """
        # Look for table with results data
        tables = soup.find_all('table')
        
        for table in tables:
            # Check if table has expected columns
            first_row = table.find('tr')
            if first_row:
                header_text = first_row.get_text().lower()
                # Look for key column headers
                if any(keyword in header_text for keyword in 
                       ['institution', 'program', 'decision', 'added', 'date', 'school']):
                    print("    Found results table by analyzing headers")
                    return table
        
        # Fallback: use largest table
        if tables:
            largest_table = max(tables, key=lambda t: len(t.find_all('tr')))
            if len(largest_table.find_all('tr')) > 5:
                print("    Using largest table as results table")
                return largest_table
        
        return None
    
    def _analyze_table_headers(self, header_row):
        """
        Analyze table headers to find column positions
        """
        headers = header_row.find_all(['th', 'td'])
        column_mapping = {}
        
        print(f"    Analyzing table headers ({len(headers)} columns found):")
        
        for i, header in enumerate(headers):
            header_text = header.get_text().strip().lower()
            print(f"      Column {i}: '{header_text}'")
            
            # Map headers to fields
            if any(word in header_text for word in ['institution', 'university', 'school']):
                column_mapping['institution'] = i
            elif any(word in header_text for word in ['program', 'field', 'major']):
                column_mapping['program'] = i
            elif any(word in header_text for word in ['decision', 'result', 'status']):
                column_mapping['decision'] = i
            elif any(word in header_text for word in ['added', 'date added', 'submission date', 'posted']):
                column_mapping['added_on'] = i
                print(f"        -> ADDED ON COLUMN FOUND at index {i}")
            elif any(word in header_text for word in ['gpa']):
                column_mapping['gpa'] = i
            elif any(word in header_text for word in ['gre']):
                column_mapping['gre'] = i
        
        print(f"    Column mapping: {column_mapping}")
        return column_mapping
    
    def _extract_row_metadata(self, row, column_mapping):
        """
        Extract metadata from a single table row
        
        Args:
            row (BeautifulSoup Tag): Table row
            column_mapping (dict): Column position mapping
            
        Returns:
            dict: Entry metadata
        """
        try:
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < 3:
                return None
            
            # Extract entry ID from any links in the row
            entry_id = None
            entry_url = None
            
            # Look for links to individual entries
            links = row.find_all('a', href=True)
            for link in links:
                href = link['href']
                # Look for /result/XXXXX pattern
                match = re.search(r'/result/(\d+)', href)
                if match:
                    entry_id = int(match.group(1))
                    entry_url = urljoin(self.base_url, href)
                    break
            
            if not entry_id:
                return None
            
            # Extract "Added On" date
            added_on_date = None
            if 'added_on' in column_mapping:
                col_index = column_mapping['added_on']
                if col_index < len(cells):
                    date_text = cells[col_index].get_text().strip()
                    # Clean up date text and extract date
                    added_on_date = self._parse_added_on_date(date_text)
            
            # Extract Season - look for GradCafe season codes (F25, S25, etc.)
            season = None
            for i, cell in enumerate(cells):
                cell_text = cell.get_text().strip()
                season_found = self._parse_season_code(cell_text)
                if season_found:
                    season = season_found
                    print(f"    Found season code in cell {i}: '{season}'")
                    break
            
            # Extract other quick metadata for verification
            institution = None
            if 'institution' in column_mapping:
                col_index = column_mapping['institution']
                if col_index < len(cells):
                    institution = cells[col_index].get_text().strip()
            
            program = None
            if 'program' in column_mapping:
                col_index = column_mapping['program']
                if col_index < len(cells):
                    program = cells[col_index].get_text().strip()
            
            decision = None
            if 'decision' in column_mapping:
                col_index = column_mapping['decision']
                if col_index < len(cells):
                    decision = cells[col_index].get_text().strip()
            
            metadata = {
                'entry_id': entry_id,
                'entry_url': entry_url,
                'added_on_date': added_on_date,
                'season': season,
                'table_institution': institution,  # For verification
                'table_program': program,          # For verification  
                'table_decision': decision         # For verification
            }
            
            return metadata
            
        except Exception as e:
            print(f"    Error extracting row metadata: {e}")
            return None
    
    def _parse_added_on_date(self, date_text):
        """
        Parse the "Added On" date from table cell text
        """
        if not date_text:
            return None
            
        # Look for common date patterns
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',      # MM/DD/YYYY
            r'(\d{4}-\d{1,2}-\d{1,2})',      # YYYY-MM-DD
            r'(\d{1,2}-\d{1,2}-\d{4})',      # MM-DD-YYYY
            r'(\w+ \d{1,2}, \d{4})',         # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_text)
            if match:
                return match.group(1)
        
        # If no pattern matches, return cleaned text
        return date_text.strip() if date_text.strip() else None
    
    def _parse_season_code(self, text):
        """
        Parse GradCafe season codes (F25, S25, F24, S24, etc.) and convert to full format
        """
        if not text:
            return None
        
        text = text.strip()
        
        # Season code mapping
        season_mapping = {
            'F25': 'Fall 2025', 'S25': 'Spring 2025',
            'F24': 'Fall 2024', 'S24': 'Spring 2024', 
            'F23': 'Fall 2023', 'S23': 'Spring 2023',
            'F22': 'Fall 2022', 'S22': 'Spring 2022',
            'F21': 'Fall 2021', 'S21': 'Spring 2021',
            'F20': 'Fall 2020', 'S20': 'Spring 2020',
            'F19': 'Fall 2019', 'S19': 'Spring 2019',
            'F26': 'Fall 2026', 'S26': 'Spring 2026',  # Future years
        }
        
        # Look for exact season codes
        for code, full_name in season_mapping.items():
            if code in text:
                return full_name
        
        # Also look for season codes with word boundaries
        season_code_pattern = r'\b([FS]\d{2})\b'
        match = re.search(season_code_pattern, text)
        if match:
            code = match.group(1)
            if code in season_mapping:
                return season_mapping[code]
            else:
                # Try to convert unknown codes (e.g., F27 -> Fall 2027)
                if code[0] == 'F':
                    year = '20' + code[1:]
                    return f'Fall {year}'
                elif code[0] == 'S':
                    year = '20' + code[1:]
                    return f'Spring {year}'
        
        # Fallback: look for full season names
        full_season_patterns = [
            r'\b(Fall\s*20\d{2})\b',
            r'\b(Spring\s*20\d{2})\b',
            r'\b(Summer\s*20\d{2})\b',
            r'\b(Winter\s*20\d{2})\b'
        ]
        
        for pattern in full_season_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _fetch_detailed_entries(self, entry_metadata):
        """
        Fetch detailed data from individual entry pages and combine with metadata
        
        Args:
            entry_metadata (list): List of metadata dicts
            
        Returns:
            list: List of complete entry data
        """
        complete_entries = []
        
        for i, metadata in enumerate(entry_metadata):
            entry_url = metadata['entry_url']
            entry_id = metadata['entry_id']
            
            print(f"Fetching detailed entry {i+1}/{len(entry_metadata)}: ID {entry_id}")
            
            # Fetch detailed data from individual entry page
            detailed_data = self._fetch_single_entry_details(entry_url, entry_id)
            
            if detailed_data:
                # Combine metadata with detailed data
                complete_entry = {**metadata, **detailed_data}
                complete_entries.append(complete_entry)
                self.total_entries_processed += 1
                
                # Show combined data
                institution = detailed_data.get('institution', metadata.get('table_institution', 'Unknown'))
                program = detailed_data.get('program', metadata.get('table_program', 'Unknown'))
                decision = detailed_data.get('decision', metadata.get('table_decision', 'Unknown'))
                added_on = metadata.get('added_on_date', 'Unknown')
                season = metadata.get('season', 'Unknown')
                notes_len = len(detailed_data.get('notes', ''))
                
                print(f"  ✓ {institution} | {program} | {decision} | Season: {season} | Added: {added_on} | Notes: {notes_len} chars")
                
                if detailed_data.get('notes', '').strip():
                    self.entries_with_notes += 1
                
                # Save backup every 50 entries
                if len(complete_entries) % 50 == 0:
                    self._save_backup(complete_entries)
            else:
                print(f"  ✗ Failed to fetch detailed data for ID {entry_id}")
            
            # Delay between requests
            delay = random.uniform(0.8, 1.5)
            time.sleep(delay)
        
        return complete_entries
    
    def _fetch_single_entry_details(self, entry_url, entry_id):
        """
        Fetch detailed data from a single entry page
        """
        try:
            # Make HTTP request
            response = self.http_pool.request(
                'GET', 
                entry_url, 
                headers=self.request_headers,
                timeout=30.0,
                retries=3
            )
            
            if response.status != 200:
                self.failed_entry_requests += 1
                return None
            
            # Decode response
            try:
                content = response.data.decode('utf-8')
            except:
                try:
                    content = response.data.decode('latin-1')
                except:
                    content = response.data.decode('utf-8', errors='ignore')
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract detailed data
            detailed_data = self._parse_individual_entry(soup, entry_url, entry_id)
            
            return detailed_data
            
        except Exception as error:
            print(f"    Error fetching details for ID {entry_id}: {str(error)}")
            self.failed_entry_requests += 1
            return None
    
    def _parse_individual_entry(self, soup, entry_url, entry_id):
        """
        Parse detailed data from an individual entry page
        """
        entry_data = {}
        
        # Get all text and parse fields
        page_text = soup.get_text()
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        # Parse using field labels
        self._parse_gradcafe_fields(lines, entry_data)
        
        # Clean and validate
        entry_data = self._clean_and_validate_entry(entry_data)
        
        return entry_data
    
    def _parse_gradcafe_fields(self, lines, entry_data):
        """
        Parse GradCafe fields from individual entry page
        """
        field_labels = {
            'institution': 'Institution',
            'program': 'Program',
            'degree_type': 'Degree Type',
            'country_origin': 'Degree\'s Country of Origin',
            'decision': 'Decision',
            'notification': 'Notification',
            'gpa': 'Undergrad GPA',
            'gre_general': 'GRE General',
            'gre_verbal': 'GRE Verbal',
            'gre_quantitative': 'GRE Quantitative',
            'analytical_writing': 'Analytical Writing',
            'notes': 'Notes'
        }
        
        i = 0
        while i < len(lines):
            current_line = lines[i].strip()
            
            # Check for exact field label match
            field_found = None
            for field_key, field_label in field_labels.items():
                if current_line == field_label:
                    field_found = field_key
                    break
            
            if field_found:
                if field_found == 'notes':
                    # Collect notes until next section
                    notes_lines = []
                    j = i + 1
                    while j < len(lines):
                        line = lines[j].strip()
                        if (line in ['Timeline', 'Application Information'] or
                            line in field_labels.values() or
                            line.startswith('Received notification')):
                            break
                        if line and line not in ['Details and information about the application.',
                                               'This data is estimated based on applicant submissions at The GradCafe.']:
                            notes_lines.append(line)
                        j += 1
                    
                    if notes_lines:
                        entry_data[field_found] = ' '.join(notes_lines).strip()
                    i = j - 1
                else:
                    # Regular field
                    if i + 1 < len(lines):
                        value = lines[i + 1].strip()
                        if (value and value not in field_labels.values() and
                            value not in ['Submit yours', '-', 'Details and information about the application.']):
                            entry_data[field_found] = value
            
            i += 1
    
    def _clean_and_validate_entry(self, entry_data):
        """
        Clean and validate entry data
        """
        # Clean GPA
        if 'gpa' in entry_data:
            gpa_match = re.search(r'([0-4]\.[0-9]{1,2})', entry_data['gpa'])
            if gpa_match:
                entry_data['gpa'] = gpa_match.group(1)
        
        # Parse notification for date and method
        if 'notification' in entry_data:
            notification = entry_data['notification']
            date_match = re.search(r'on (\d{1,2}/\d{1,2}/\d{4})', notification)
            if date_match:
                entry_data['notification_date'] = date_match.group(1)
            method_match = re.search(r'via (\w+)', notification)
            if method_match:
                entry_data['notification_method'] = method_match.group(1)
        
        # Standardize decision
        if 'decision' in entry_data:
            decision = entry_data['decision'].lower()
            if 'accept' in decision:
                entry_data['decision_standardized'] = 'Accepted'
            elif 'reject' in decision:
                entry_data['decision_standardized'] = 'Rejected'
            elif 'waitlist' in decision:
                entry_data['decision_standardized'] = 'Waitlisted'
            elif 'interview' in decision:
                entry_data['decision_standardized'] = 'Interview'
            else:
                entry_data['decision_standardized'] = 'Other'
        
        # Add notes metadata
        if 'notes' in entry_data and entry_data['notes']:
            notes = entry_data['notes'].strip()
            entry_data['notes'] = notes
            entry_data['notes_length'] = len(notes)
            entry_data['notes_word_count'] = len(notes.split())
        
        return entry_data
    
    def _save_backup(self, data):
        """Save backup of current data"""
        filename = f"gradcafe_backup_{len(data)}_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  Backup saved: {filename}")
        except Exception as e:
            print(f"  Failed to save backup: {e}")
    
    def _save_complete_data(self, data):
        """Save complete data to single JSON file"""
        filename = "gradcafe_complete_data.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Complete data saved to {filename}")
            print(f"   Total entries: {len(data)}")
            
            # Show summary statistics
            with_notes = len([e for e in data if e.get('notes', '').strip()])
            with_added_on = len([e for e in data if e.get('added_on_date')])
            with_season = len([e for e in data if e.get('season')])
            
            print(f"   Entries with notes: {with_notes}/{len(data)} ({with_notes/len(data)*100:.1f}%)")
            print(f"   Entries with 'Added On' date: {with_added_on}/{len(data)} ({with_added_on/len(data)*100:.1f}%)")
            print(f"   Entries with 'Season': {with_season}/{len(data)} ({with_season/len(data)*100:.1f}%)")
            
            # Show decision distribution
            decisions = {}
            for entry in data:
                decision = entry.get('decision_standardized', 'Unknown')
                decisions[decision] = decisions.get(decision, 0) + 1
            
            print(f"   Decision distribution:")
            for decision, count in decisions.items():
                print(f"     {decision}: {count}")
            
        except Exception as e:
            print(f"❌ Failed to save complete data: {e}")


def main():
    """
    Main function to run the clean scraper
    """
    print("="*60)
    print("GradCafe Data Scraper (Season Code Enhanced)")
    print("- Detects GradCafe season codes: F25=Fall 2025, S25=Spring 2025")
    print("- Extracts entry IDs, dates, season, and detailed data")
    print("- Complete notes sections from individual entries")
    print("- Single JSON output with all fields including season")
    print("="*60)
    
    # Initialize scraper
    scraper = GradCafeScraper()
    
    # Scrape data
    complete_data = scraper.scrape_data(target_entries=50, max_pages=5)
    
    if complete_data:
        print(f"\n✅ Successfully collected {len(complete_data)} complete entries")
        
        # Show sample entries
        print("\n=== Sample Entries ===")
        for i, entry in enumerate(complete_data[:3]):
            print(f"\nEntry {i+1} (ID: {entry.get('entry_id', 'Unknown')}):")
            print(f"  Added On: {entry.get('added_on_date', 'Unknown')}")
            print(f"  Season: {entry.get('season', 'Unknown')}")
            print(f"  Institution: {entry.get('institution', 'Unknown')}")
            print(f"  Program: {entry.get('program', 'Unknown')}")
            print(f"  Decision: {entry.get('decision', 'Unknown')}")
            notes = entry.get('notes', '')
            if notes:
                print(f"  Notes: {notes[:100]}{'...' if len(notes) > 100 else ''}")
        
        # Show field coverage
        print(f"\n=== Field Coverage ===")
        field_counts = {}
        for entry in complete_data:
            for field in entry:
                if field not in ['entry_url', 'entry_id', 'table_institution', 'table_program', 'table_decision']:
                    field_counts[field] = field_counts.get(field, 0) + 1
        
        for field, count in sorted(field_counts.items()):
            coverage = (count / len(complete_data)) * 100
            print(f"{field}: {count}/{len(complete_data)} ({coverage:.1f}%)")
            
    else:
        print("\n❌ No data collected.")


if __name__ == "__main__":
    main()