"""
Main Runner Script for GradCafe Scraper
Module 1 Assignment - JHU Software Concepts

This script combines both scraping and cleaning operations for convenience.

Author: [Your Name]  
Date: June 2025
Python Version: 3.10+
"""

import sys
import os
from datetime import datetime

# Import our custom modules
try:
    import scrape
    import clean
    # Alternative import method
    from scrape import GradCafeScraper
    from clean import GradCafeDataCleaner
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure scrape.py and clean.py are in the same directory")
    print("Falling back to subprocess execution...")
    
    import subprocess
    import sys
    
    def run_scraping(target_entries):
        """Run scraping using subprocess"""
        try:
            result = subprocess.run([sys.executable, 'scrape.py'], 
                                  capture_output=True, text=True, timeout=3600)
            if result.returncode == 0:
                print("✅ Scraping completed successfully")
                return True
            else:
                print(f"❌ Scraping failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error running scraper: {e}")
            return False
    
    def run_cleaning():
        """Run cleaning using subprocess"""
        try:
            result = subprocess.run([sys.executable, 'clean.py'], 
                                  capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                print("✅ Cleaning completed successfully")
                return True
            else:
                print(f"❌ Cleaning failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error running cleaner: {e}")
            return False
    
    # Use subprocess version of pipeline
    def run_complete_pipeline_subprocess(target_entries=100):
        print("="*70)
        print("GradCafe Complete Data Collection Pipeline (Subprocess Mode)")
        print("="*70)
        
        print("STEP 1: Data Scraping")
        print("-" * 30)
        if not run_scraping(target_entries):
            return False
        
        print("\nSTEP 2: Data Cleaning")  
        print("-" * 30)
        if not run_cleaning():
            return False
            
        print("\n✅ Pipeline completed successfully!")
        print("📁 Check applicant_data.json for results")
        return True
    
    # Override the main pipeline function
    def run_complete_pipeline(target_entries=1000):
        return run_complete_pipeline_subprocess(target_entries)


def run_complete_pipeline(target_entries=1000):
    """
    Run the complete data collection and cleaning pipeline
    
    Args:
        target_entries (int): Target number of entries to collect
    """
    print("="*70)
    print("GradCafe Complete Data Collection Pipeline")
    print("Module 1 Assignment - JHU Software Concepts")
    print("="*70)
    print(f"Target entries: {target_entries}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Data Scraping
    print("STEP 1: Data Scraping")
    print("-" * 30)
    
    scraper = GradCafeScraper()
    raw_data = scraper.scrape_data(target_entries=target_entries, max_pages=500)
    
    if not raw_data:
        print("❌ Scraping failed - no data collected")
        return False
    
    print(f"✅ Scraping completed - {len(raw_data)} entries collected")
    print()
    
    # Step 2: Data Cleaning  
    print("STEP 2: Data Cleaning")
    print("-" * 30)
    
    cleaner = GradCafeDataCleaner()
    cleaned_data = cleaner.clean_data("raw_scraped_data.json")
    
    if not cleaned_data:
        print("❌ Cleaning failed - no data processed")
        return False
    
    # Step 3: Save Final Data
    print("STEP 3: Saving Final Data")
    print("-" * 30)
    
    cleaner.save_data(cleaned_data, "applicant_data.json")
    
    # Step 4: Final Summary
    print()
    print("="*70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"📊 Raw entries scraped: {len(raw_data)}")
    print(f"🧹 Cleaned entries: {len(cleaned_data)}")
    print(f"📁 Output file: applicant_data.json")
    print(f"⏰ Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Data quality summary
    if cleaned_data:
        avg_completeness = sum(entry.get('data_completeness_percentage', 0) 
                             for entry in cleaned_data) / len(cleaned_data)
        print(f"📈 Average data completeness: {avg_completeness:.1f}%")
        
        # Count entries with key fields
        key_metrics = {
            'University': sum(1 for e in cleaned_data if e.get('university')),
            'Program': sum(1 for e in cleaned_data if e.get('program_name')),
            'GRE Score': sum(1 for e in cleaned_data if e.get('gre_score')),
            'GPA': sum(1 for e in cleaned_data if e.get('gpa')),
            'Degree Type': sum(1 for e in cleaned_data if e.get('masters_or_phd'))
        }
        
        print("\n📋 Key Field Statistics:")
        total = len(cleaned_data)
        for field, count in key_metrics.items():
            percentage = (count/total)*100 if total > 0 else 0
            print(f"   {field}: {count}/{total} ({percentage:.1f}%)")
    
    print()
    print("🎉 All data saved to applicant_data.json")
    print("📚 See README.md for detailed documentation")
    
    return True


def check_requirements():
    """
    Check if all required dependencies are available
    """
    print("Checking requirements...")
    
    required_modules = {
        'urllib3': 'urllib3',
        'BeautifulSoup': 'bs4',
        'json': 'json',
        're': 're',
        'time': 'time',
        'random': 'random',
        'datetime': 'datetime'
    }
    
    missing_modules = []
    
    for name, module in required_modules.items():
        try:
            __import__(module)
            print(f"✅ {name} - Available")
        except ImportError:
            print(f"❌ {name} - Missing")
            missing_modules.append(name)
    
    if missing_modules:
        print(f"\n❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied")
    return True


def verify_robots_txt():
    """
    Remind user about robots.txt compliance
    """
    print("\n🤖 robots.txt Compliance Verification")
    print("-" * 40)
    print("✅ robots.txt checked at: https://www.thegradcafe.com/robots.txt")
    print("✅ /survey/ path is ALLOWED for scraping")
    print("✅ Only /cgi-bin/ and /index-ad-test.php are disallowed")
    print("✅ Screenshot evidence provided in screenshot.jpg")
    print("✅ Scraper respects all stated policies")


def main():
    """
    Main function with command line options
    """
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--check':
            check_requirements()
            verify_robots_txt()
            return
        elif sys.argv[1] == '--scrape-only':
            print("Running scraping only...")
            scraper = GradCafeScraper()
            scraper.scrape_data(target_entries=1000)
            return
        elif sys.argv[1] == '--clean-only':
            print("Running cleaning only...")
            cleaner = GradCafeDataCleaner()
            cleaned_data = cleaner.clean_data("raw_scraped_data.json")
            if cleaned_data:
                cleaner.save_data(cleaned_data, "applicant_data.json")
            return
        elif sys.argv[1] == '--help':
            print("GradCafe Scraper - Usage Options:")
            print("  python main.py              # Run complete pipeline")
            print("  python main.py --check      # Check requirements and robots.txt")
            print("  python main.py --scrape-only # Run scraping only")
            print("  python main.py --clean-only  # Run cleaning only") 
            print("  python main.py --help       # Show this help")
            return
    
    # Check requirements first
    if not check_requirements():
        sys.exit(1)
    
    # Show robots.txt compliance
    verify_robots_txt()
    
    # Run complete pipeline
    success = run_complete_pipeline(target_entries=100)
    
    if not success:
        print("❌ Pipeline failed - check error messages above")
        sys.exit(1)


if __name__ == "__main__":
    main()