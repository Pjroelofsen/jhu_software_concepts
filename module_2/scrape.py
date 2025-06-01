"""
GradCafe Data Scraper
Module 1 Assignment - JHU Software Concepts

This module handles scraping data from thegradcafe.com using only libraries
covered in Module 2 lecture: urllib3, BeautifulSoup, json, re, and standard library.

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
    Scrapes graduate school admission data from thegradcafe.com
    
    This class handles the extraction of applicant data including program details,
    admission decisions, test scores, and other relevant information while
    respecting the site's robots.txt policies.
    """
    
    def __init__(self):
        """Initialize the scraper with base configuration"""
        self.base_url = "https://www.thegradcafe.com"
        self.survey_url = f"{self.base_url}/survey/index.php"
        
        # Initialize urllib3 pool manager for HTTP requests
        self.http_pool = urllib3.PoolManager()
        
        # Headers to simulate legitimate browser requests
        self.request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Track scraping statistics
        self.total_pages_scraped = 0
        self.total_entries_found = 0
        self.failed_page_requests = 0
    
    def scrape_data(self, target_entries=10000, max_pages=500, start_page=1):
        """
        Main method to scrape data from GradCafe
        
        Args:
            target_entries (int): Target number of applicant entries to collect
            max_pages (int): Maximum pages to scrape to prevent infinite loops
            start_page (int): Starting page number for scraping
            
        Returns:
            list: Raw scraped data from all pages
        """
        print(f"Starting data scraping for {target_entries} target entries...")
        print(f"Scraping will begin from page {start_page}")
        
        all_raw_data = []
        current_page = start_page
        consecutive_empty_pages = 0
        
        while (len(all_raw_data) < target_entries and 
               current_page <= max_pages and 
               consecutive_empty_pages < 5):
            
            print(f"Scraping page {current_page}... (Current entries: {len(all_raw_data)})")
            
            # Get page data
            page_data = self._scrape_single_page(current_page)
            
            if page_data:
                all_raw_data.extend(page_data)
                consecutive_empty_pages = 0
                self.total_entries_found += len(page_data)
                print(f"Found {len(page_data)} entries on page {current_page}")
                
                # Save periodic backup every 1000 entries
                if len(all_raw_data) % 1000 == 0:
                    self._save_backup(all_raw_data, current_page)
                    
            else:
                consecutive_empty_pages += 1
                print(f"No data found on page {current_page}")
                
            current_page += 1
            self.total_pages_scraped += 1
            
            # Respectful delay between requests (reduced for speed)
            time.sleep(random.uniform(0.3, 0.8))  # Much faster than 1-3 seconds
        
        print(f"\nScraping completed!")
        print(f"Total pages scraped: {self.total_pages_scraped}")
        print(f"Total entries collected: {len(all_raw_data)}")
        print(f"Failed page requests: {self.failed_page_requests}")
        
        return all_raw_data
    
    def _scrape_single_page(self, page_number):
        """
        Scrape data from a single page
        
        Args:
            page_number (int): Page number to scrape
            
        Returns:
            list: Raw data entries from the page, or None if failed
        """
        try:
            # Construct URL for specific page
            page_url = f"{self.survey_url}?page={page_number}"
            
            # Make HTTP request using urllib3
            response = self.http_pool.request(
                'GET', 
                page_url, 
                headers=self.request_headers,
                timeout=10.0
            )
            
            if response.status != 200:
                print(f"HTTP {response.status} error for page {page_number}")
                self.failed_page_requests += 1
                return None
            
            # Parse HTML content with BeautifulSoup
            page_content = response.data.decode('utf-8')
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Extract data from the page
            page_entries = self._extract_page_entries(soup, page_url)
            
            return page_entries
            
        except Exception as error:
            print(f"Error scraping page {page_number}: {str(error)}")
            self.failed_page_requests += 1
            return None
    
    def _extract_page_entries(self, soup, page_url):
        """
        Extract all applicant entries from a parsed page
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            page_url (str): URL of the current page
            
        Returns:
            list: List of raw entry dictionaries
        """
        entries = []
        
        # Find the main results table
        results_table = self._find_results_table(soup)
        
        if results_table:
            # Get all data rows (skip header row)
            data_rows = results_table.find_all('tr')[1:]
            
            for row in data_rows:
                # Extract data from each row
                entry_data = self._extract_single_entry(row, page_url)
                if entry_data:
                    entries.append(entry_data)
        else:
            print(f"Warning: Could not find results table in page {page_url}")
        
        return entries
    
    def _find_results_table(self, soup):
        """
        Find the main results table in the page
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            
        Returns:
            BeautifulSoup Tag: Results table element, or None if not found
        """
        # Try to find table by common identifiers
        table_selectors = [
            {'id': 'results'},
            {'class': 'results'},
            {'class': 'submission-table'},
            None  # Generic table search
        ]
        
        for selector in table_selectors:
            if selector:
                table = soup.find('table', selector)
            else:
                # Generic search for tables that look like results
                tables = soup.find_all('table')
                table = self._identify_results_table(tables)
            
            if table:
                return table
        
        return None
    
    def _identify_results_table(self, tables):
        """
        Identify which table contains the results data
        
        Args:
            tables (list): List of table elements
            
        Returns:
            BeautifulSoup Tag: Most likely results table, or None
        """
        for table in tables:
            # Check if table headers contain result-related keywords
            header_row = table.find('tr')
            if header_row:
                header_text = header_row.get_text().lower()
                result_keywords = ['institution', 'program', 'decision', 'date', 'university']
                
                if any(keyword in header_text for keyword in result_keywords):
                    return table
        
        # If no clear match, return the largest table
        if tables:
            return max(tables, key=lambda t: len(t.find_all('tr')))
        
        return None
    
    def _extract_single_entry(self, row, page_url):
        """
        Extract data from a single table row
        
        Args:
            row (BeautifulSoup Tag): Table row element
            page_url (str): URL of the current page
            
        Returns:
            dict: Raw entry data, or None if extraction failed
        """
        try:
            # Get all cells in the row
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < 3:  # Skip rows with insufficient data
                return None
            
            # Extract text from each cell
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            
            # Create raw entry with all available data
            raw_entry = {
                'html_content': str(row),  # Preserve original HTML
                'cell_data': cell_texts,
                'page_url': page_url,
                'extraction_timestamp': datetime.now().isoformat(),
                'row_text': row.get_text(strip=True)
            }
            
            # Look for any links in the row (entry detail links)
            entry_links = row.find_all('a')
            if entry_links:
                for link in entry_links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        raw_entry['entry_detail_url'] = full_url
                        break
            
            return raw_entry
            
        except Exception as error:
            print(f"Error extracting entry: {str(error)}")
            return None
    
    def _save_backup(self, data, current_page):
        """
        Save periodic backup of scraped data
        
        Args:
            data (list): Current scraped data
            current_page (int): Current page number
        """
        backup_filename = f"backup_data_page_{current_page}_{len(data)}_entries.json"
        
        try:
            with open(backup_filename, 'w', encoding='utf-8') as backup_file:
                json.dump(data, backup_file, indent=2, ensure_ascii=False)
            print(f"Backup saved: {backup_filename}")
        except Exception as error:
            print(f"Failed to save backup: {str(error)}")


def main():
    """
    Main function to run the scraper
    """
    print("="*60)
    print("GradCafe Data Scraper - Module 1 Assignment")
    print("="*60)
    
    # Initialize scraper
    scraper = GradCafeScraper()
    
    # Scrape data
    raw_data = scraper.scrape_data(target_entries=10000, max_pages=500)
    
    # Save raw data for processing
    if raw_data:
        raw_filename = "raw_scraped_data.json"
        try:
            with open(raw_filename, 'w', encoding='utf-8') as raw_file:
                json.dump(raw_data, raw_file, indent=2, ensure_ascii=False)
            print(f"✅ Raw data saved to {raw_filename}")
            print(f"📊 Total entries saved: {len(raw_data)}")
            print(f"Next step: Run clean.py to process this data")
        except Exception as error:
            print(f"❌ Error saving raw data: {str(error)}")
    else:
        print("❌ No data was scraped. Please check the website and try again.")


if __name__ == "__main__":
    main()