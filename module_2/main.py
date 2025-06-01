"""
GradCafe Main Processing Script
Module 2 Assignment - JHU Software Concepts

This is the main script that orchestrates the entire GradCafe data collection and cleaning process.
It runs scrape.py followed by clean.py with optimizations for large datasets.

Features:
- Configurable number of entries (supports 10,000+)
- Parallel processing for speed optimization
- Progress tracking and time estimation
- Error handling and recovery
- Memory-efficient processing

Author: Phillip Roelofsen
Date: June 2025
Python Version: 3.10+
"""

import argparse
import time
import json
import os
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import urllib3
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import random

# Import our modules
try:
    from gradcafe_complete_data import GradCafeScraper
except ImportError:
    # If import fails, we'll define an optimized scraper here
    pass


class OptimizedGradCafeScraper:
    """
    Optimized version of GradCafe scraper for large datasets
    """
    
    def __init__(self, max_workers=5, delay_range=(0.5, 1.0)):
        """
        Initialize with parallel processing capabilities
        
        Args:
            max_workers (int): Number of parallel workers for individual entries
            delay_range (tuple): Min and max delay between requests (seconds)
        """
        self.base_url = "https://www.thegradcafe.com"
        self.survey_url = f"{self.base_url}/survey"
        self.max_workers = max_workers
        self.delay_range = delay_range
        
        # Disable SSL warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Initialize urllib3 pool manager with more connections
        self.http_pool = urllib3.PoolManager(
            cert_reqs='CERT_NONE',
            timeout=30.0,
            maxsize=max_workers * 2  # More connections for parallel processing
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
        
        # Thread-safe counters
        self.stats_lock = Lock()
        self.total_pages_scraped = 0
        self.total_entries_found = 0
        self.total_entries_processed = 0
        self.entries_with_notes = 0
        self.failed_requests = 0
        
    def scrape_data_optimized(self, target_entries=10000, max_pages=100, batch_size=50):
        """
        Optimized scraping method for large datasets
        
        Args:
            target_entries (int): Target number of entries to collect
            max_pages (int): Maximum pages to scrape for metadata
            batch_size (int): Number of entries to process in parallel
            
        Returns:
            list: Complete dataset
        """
        print(f"🚀 Starting OPTIMIZED GradCafe scraping for {target_entries:,} entries")
        print(f"📊 Configuration:")
        print(f"   - Max workers: {self.max_workers}")
        print(f"   - Batch size: {batch_size}")
        print(f"   - Delay range: {self.delay_range[0]}-{self.delay_range[1]}s")
        print(f"   - Max pages: {max_pages}")
        
        start_time = time.time()
        
        # Step 1: Collect metadata from table pages (sequential)
        print(f"\n{'='*60}")
        print("STEP 1: Collecting entry metadata from results tables")
        print(f"{'='*60}")
        
        entry_metadata = self._collect_metadata_sequential(max_pages, target_entries)
        
        if not entry_metadata:
            print("❌ No metadata collected. Exiting.")
            return []
        
        print(f"✅ Collected {len(entry_metadata):,} entry metadata records")
        
        # Step 2: Process individual entries in parallel batches
        print(f"\n{'='*60}")
        print("STEP 2: Processing individual entries (PARALLEL)")
        print(f"{'='*60}")
        
        complete_entries = self._process_entries_parallel(entry_metadata, batch_size)
        
        elapsed_time = time.time() - start_time
        
        # Final statistics
        print(f"\n{'='*60}")
        print("🎉 SCRAPING COMPLETED!")
        print(f"{'='*60}")
        print(f"⏱️  Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
        print(f"📊 Entries processed: {len(complete_entries):,}")
        print(f"💬 Entries with notes: {self.entries_with_notes:,}")
        print(f"⚡ Processing rate: {len(complete_entries)/elapsed_time:.2f} entries/second")
        print(f"❌ Failed requests: {self.failed_requests}")
        
        # Save data
        if complete_entries:
            self._save_complete_data(complete_entries)
        
        return complete_entries
    
    def _collect_metadata_sequential(self, max_pages, target_entries):
        """
        Collect entry metadata from table pages (must be sequential for pagination)
        """
        all_metadata = []
        page = 1
        consecutive_empty = 0
        
        while len(all_metadata) < target_entries and page <= max_pages and consecutive_empty < 3:
            print(f"📄 Scraping page {page}... (entries: {len(all_metadata):,})")
            
            page_metadata = self._scrape_single_table_page(page)
            
            if page_metadata:
                all_metadata.extend(page_metadata)
                consecutive_empty = 0
                print(f"   ✅ Found {len(page_metadata)} entries")
            else:
                consecutive_empty += 1
                print(f"   ❌ No entries found")
            
            page += 1
            self.total_pages_scraped += 1
            
            # Brief delay between table pages
            time.sleep(random.uniform(1.0, 2.0))
        
        return all_metadata[:target_entries]  # Limit to target
    
    def _scrape_single_table_page(self, page_number):
        """Scrape metadata from a single table page"""
        url_patterns = [
            f"{self.survey_url}/index.php?q=&t=a&o=&pp=250&p={page_number}",
            f"{self.survey_url}/?page={page_number}",
            f"{self.survey_url}/index.php?page={page_number}",
        ]
        
        for url in url_patterns:
            try:
                response = self.http_pool.request('GET', url, headers=self.request_headers, timeout=30.0)
                if response.status == 200:
                    content = response.data.decode('utf-8', errors='ignore')
                    soup = BeautifulSoup(content, 'html.parser')
                    return self._extract_metadata_from_soup(soup)
            except Exception as e:
                print(f"   ⚠️  Error with URL {url}: {e}")
                continue
        
        return []
    
    def _extract_metadata_from_soup(self, soup):
        """Extract entry metadata from parsed table page"""
        metadata_list = []
        
        # Find table and extract entry links
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header
                # Look for result links
                links = row.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    match = re.search(r'/result/(\d+)', href)
                    if match:
                        entry_id = int(match.group(1))
                        entry_url = urljoin(self.base_url, href)
                        
                        # Extract basic metadata from row
                        cells = row.find_all(['td', 'th'])
                        cell_texts = [cell.get_text().strip() for cell in cells]
                        
                        metadata = {
                            'entry_id': entry_id,
                            'entry_url': entry_url,
                            'table_data': cell_texts  # Raw table data
                        }
                        metadata_list.append(metadata)
                        break
        
        return metadata_list
    
    def _process_entries_parallel(self, entry_metadata, batch_size):
        """
        Process individual entries in parallel batches
        """
        complete_entries = []
        total_batches = (len(entry_metadata) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(entry_metadata))
            batch = entry_metadata[start_idx:end_idx]
            
            print(f"\n🔄 Processing batch {batch_num + 1}/{total_batches} ({len(batch)} entries)")
            
            batch_start_time = time.time()
            batch_results = self._process_batch_parallel(batch)
            batch_time = time.time() - batch_start_time
            
            complete_entries.extend(batch_results)
            
            # Progress update
            processed_count = len(complete_entries)
            total_count = len(entry_metadata)
            progress = (processed_count / total_count) * 100
            
            print(f"   ✅ Batch completed in {batch_time:.1f}s")
            print(f"   📊 Progress: {processed_count:,}/{total_count:,} ({progress:.1f}%)")
            
            # Estimate remaining time
            if processed_count > 0:
                avg_time_per_entry = (time.time() - batch_start_time) / len(batch_results) if batch_results else 0
                remaining_entries = total_count - processed_count
                estimated_remaining = remaining_entries * avg_time_per_entry
                print(f"   ⏱️  Estimated remaining: {estimated_remaining/60:.1f} minutes")
            
            # Save progress backup
            if len(complete_entries) % 500 == 0:
                self._save_progress_backup(complete_entries)
        
        return complete_entries
    
    def _process_batch_parallel(self, batch_metadata):
        """Process a batch of entries in parallel"""
        batch_results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_metadata = {
                executor.submit(self._fetch_single_entry_safe, metadata): metadata 
                for metadata in batch_metadata
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_metadata):
                metadata = future_to_metadata[future]
                try:
                    result = future.result()
                    if result:
                        # Combine metadata with detailed data
                        complete_entry = {**metadata, **result}
                        batch_results.append(complete_entry)
                        
                        with self.stats_lock:
                            self.total_entries_processed += 1
                            if result.get('notes', '').strip():
                                self.entries_with_notes += 1
                    
                except Exception as e:
                    print(f"   ⚠️  Error processing entry {metadata.get('entry_id', 'unknown')}: {e}")
                    with self.stats_lock:
                        self.failed_requests += 1
        
        return batch_results
    
    def _fetch_single_entry_safe(self, metadata):
        """
        Thread-safe method to fetch a single entry with error handling
        """
        entry_url = metadata['entry_url']
        entry_id = metadata['entry_id']
        
        try:
            # Add random delay for politeness
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
            
            # Make request
            response = self.http_pool.request(
                'GET', 
                entry_url, 
                headers=self.request_headers,
                timeout=30.0,
                retries=2
            )
            
            if response.status != 200:
                return None
            
            # Parse content
            content = response.data.decode('utf-8', errors='ignore')
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract data
            return self._parse_individual_entry(soup)
            
        except Exception as e:
            # Silent failure for thread safety
            return None
    
    def _parse_individual_entry(self, soup):
        """Parse individual entry page"""
        entry_data = {}
        
        page_text = soup.get_text()
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        # Field labels to look for
        field_labels = {
            'institution': 'Institution',
            'program': 'Program',
            'degree_type': 'Degree Type',
            'country_origin': 'Degree\'s Country of Origin',
            'decision': 'Decision',
            'notification': 'Notification',
            'gpa': 'Undergrad GPA',
            'notes': 'Notes'
        }
        
        i = 0
        while i < len(lines):
            current_line = lines[i].strip()
            
            # Check for field labels
            for field_key, field_label in field_labels.items():
                if current_line == field_label:
                    if field_key == 'notes':
                        # Collect notes until next section
                        notes_lines = []
                        j = i + 1
                        while j < len(lines):
                            line = lines[j].strip()
                            if (line in field_labels.values() or 
                                line in ['Timeline', 'Application Information'] or
                                line.startswith('Received notification')):
                                break
                            if line and line not in ['Details and information about the application.',
                                                   'This data is estimated based on applicant submissions at The GradCafe.']:
                                notes_lines.append(line)
                            j += 1
                        
                        if notes_lines:
                            entry_data[field_key] = ' '.join(notes_lines).strip()
                        i = j - 1
                    else:
                        # Regular field
                        if i + 1 < len(lines):
                            value = lines[i + 1].strip()
                            if (value and value not in field_labels.values() and
                                value not in ['Submit yours', '-']):
                                entry_data[field_key] = value
                    break
            i += 1
        
        return entry_data
    
    def _save_progress_backup(self, data):
        """Save progress backup"""
        filename = f"gradcafe_progress_backup_{len(data)}_entries.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"   💾 Progress backup saved: {filename}")
        except Exception as e:
            print(f"   ⚠️  Failed to save backup: {e}")
    
    def _save_complete_data(self, data):
        """Save final complete data"""
        filename = "gradcafe_complete_data.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Complete data saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save complete data: {e}")


class GradCafeDataCleaner:
    """
    Simplified data cleaner for main.py
    """
    
    def __init__(self, input_file="gradcafe_complete_data.json", output_file="applicant_data.json"):
        self.input_file = input_file
        self.output_file = output_file
        self.target_fields = [
            'institution', 'program', 'notes', 'added_on_date',
            'entry_url', 'decision', 'country_origin', 'degree_type'
        ]
    
    def clean_data(self):
        """Clean the scraped data"""
        print(f"\n{'='*60}")
        print("🧹 CLEANING DATA")
        print(f"{'='*60}")
        
        if not os.path.exists(self.input_file):
            print(f"❌ Input file '{self.input_file}' not found!")
            return []
        
        # Load data
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            print(f"📁 Loaded {len(raw_data):,} raw entries")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return []
        
        # Clean data
        clean_data = []
        for i, raw_entry in enumerate(raw_data):
            clean_entry = self._clean_entry(raw_entry)
            if clean_entry:
                clean_data.append(clean_entry)
            
            if (i + 1) % 1000 == 0:
                print(f"   🔄 Cleaned {i + 1:,}/{len(raw_data):,} entries")
        
        # Save clean data
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Clean data saved to {self.output_file}")
            print(f"📊 Output: {len(clean_data):,} clean entries")
        except Exception as e:
            print(f"❌ Error saving clean data: {e}")
        
        return clean_data
    
    def _clean_entry(self, raw_entry):
        """Clean a single entry"""
        clean_entry = {
            'entry_id': raw_entry.get('entry_id'),
            'processing_timestamp': datetime.now().isoformat()
        }
        
        # Extract target fields
        for field in self.target_fields:
            value = raw_entry.get(field) or raw_entry.get(f"table_{field}")
            if value and str(value).strip():
                clean_entry[field] = str(value).strip()
        
        return clean_entry if len(clean_entry) > 2 else None


def main():
    """
    Main function with command line interface
    """
    parser = argparse.ArgumentParser(
        description="GradCafe Data Collection and Processing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --entries 1000                    # Collect 1,000 entries
  python main.py --entries 10000 --workers 8      # Collect 10,000 entries with 8 workers
  python main.py --entries 5000 --fast            # Fast mode (shorter delays)
  python main.py --clean-only                     # Only run cleaning step
        """
    )
    
    parser.add_argument(
        '--entries', 
        type=int, 
        default=1000,
        help='Number of entries to collect (default: 1000, supports 10,000+)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Number of parallel workers (default: 5, max recommended: 10)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Batch size for parallel processing (default: 50)'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Fast mode with shorter delays (less polite to server)'
    )
    
    parser.add_argument(
        '--clean-only',
        action='store_true',
        help='Skip scraping and only run data cleaning'
    )
    
    parser.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help='Maximum pages to scrape for metadata (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.workers > 10:
        print("⚠️  Warning: More than 10 workers may overwhelm the server")
    
    if args.entries > 50000:
        print("⚠️  Warning: Very large datasets may take several hours")
    
    # Set delay based on mode
    delay_range = (0.3, 0.7) if args.fast else (0.5, 1.2)
    
    print("="*60)
    print("🎓 GRADCAFE DATA COLLECTION PIPELINE")
    print("="*60)
    print(f"📊 Configuration:")
    print(f"   - Target entries: {args.entries:,}")
    print(f"   - Workers: {args.workers}")
    print(f"   - Batch size: {args.batch_size}")
    print(f"   - Mode: {'Fast' if args.fast else 'Normal'}")
    print(f"   - Delay range: {delay_range[0]}-{delay_range[1]}s")
    print(f"   - Clean only: {args.clean_only}")
    
    total_start_time = time.time()
    
    # Step 1: Scraping (unless clean-only)
    if not args.clean_only:
        print(f"\n{'='*60}")
        print("PHASE 1: DATA SCRAPING")
        print(f"{'='*60}")
        
        scraper = OptimizedGradCafeScraper(
            max_workers=args.workers,
            delay_range=delay_range
        )
        
        scraped_data = scraper.scrape_data_optimized(
            target_entries=args.entries,
            max_pages=args.max_pages,
            batch_size=args.batch_size
        )
        
        if not scraped_data:
            print("❌ No data scraped. Exiting.")
            return
    
    # Step 2: Data Cleaning
    print(f"\n{'='*60}")
    print("PHASE 2: DATA CLEANING")
    print(f"{'='*60}")
    
    cleaner = GradCafeDataCleaner()
    clean_data = cleaner.clean_data()
    
    # Final summary
    total_time = time.time() - total_start_time
    print(f"\n{'='*60}")
    print("🎉 PIPELINE COMPLETED!")
    print(f"{'='*60}")
    print(f"⏱️  Total pipeline time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    if clean_data:
        print(f"📊 Final output: {len(clean_data):,} clean entries")
        print(f"📁 Output file: applicant_data.json")
        
        # Show sample of final data
        print(f"\n=== Sample Final Entries ===")
        for i, entry in enumerate(clean_data[:2]):
            print(f"\nEntry {i+1}:")
            print(f"  Institution: {entry.get('institution', 'N/A')}")
            print(f"  Program: {entry.get('program', 'N/A')}")
            print(f"  Decision: {entry.get('decision', 'N/A')}")
            notes = entry.get('notes', '')
            if notes:
                print(f"  Notes: {notes[:100]}{'...' if len(notes) > 100 else ''}")
    
    print(f"\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    main()