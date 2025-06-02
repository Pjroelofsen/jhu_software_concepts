# GradCafe Data Scraper

A comprehensive Python-based data collection and processing pipeline for scraping graduate school admission results from [thegradcafe.com](https://www.thegradcafe.com/survey/). This project efficiently collects and processes thousands of admission entries with detailed applicant notes and decision information.

## 🎯 Project Overview

The GradCafe Scraper is designed to collect graduate school admission data at scale, supporting datasets of 10,000+ entries. It extracts detailed information including:

- **Institution names** and **program details**
- **Admission decisions** (Accepted/Rejected/Waitlisted/Interview)
- **Complete applicant notes** and experiences
- **Submission dates** and **entry URLs**
- **Academic credentials** (GPA, GRE scores)
- **Degree types** and **country of origin**

## 📁 Project Structure

```
gradcafe-scraper/
├── main.py                    # Main orchestration script with CLI
├── scrape.py                  # Core scraping functionality  
├── clean.py                   # Data cleaning and filtering
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── gradcafe_complete_data.json    # Raw scraped data (generated)
├── applicant_data.json           # Clean, filtered data (generated)
└── debug_*.html                   # Debug files (generated)
```

### Core Files

| File | Purpose | Key Features |
|------|---------|--------------|
| **`main.py`** | Pipeline orchestrator | CLI interface, parallel processing, progress tracking |
| **`scrape.py`** | Data scraping engine | Individual entry parsing, notes extraction |
| **`clean.py`** | Data processor | Field filtering, standardization, validation |

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project files
cd gradcafe-scraper

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```bash
# Collect 1,000 entries (default)
python main.py

# Collect 10,000 entries (large dataset)
python main.py --entries 10000

# Fast mode for quicker processing
python main.py --entries 5000 --fast
```

### 3. Output Files

- **`applicant_data.json`** - Clean, filtered data ready for analysis
- **`gradcafe_complete_data.json`** - Complete raw scraped data

## 📋 Detailed Usage

### Command Line Options

```bash
python main.py [OPTIONS]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--entries` | int | 1000 | Number of entries to collect |
| `--workers` | int | 5 | Parallel workers (5-10 recommended) |
| `--batch-size` | int | 50 | Entries per batch |
| `--fast` | flag | False | Fast mode with shorter delays |
| `--clean-only` | flag | False | Skip scraping, only clean existing data |
| `--max-pages` | int | 100 | Maximum table pages to scrape |

### Usage Examples

```bash
# Standard collection
python main.py --entries 2000

# Large dataset with optimization
python main.py --entries 15000 --workers 8 --batch-size 100

# Fast mode (use carefully - less server-friendly)
python main.py --entries 5000 --fast --workers 6

# Only clean existing raw data
python main.py --clean-only

# Custom configuration
python main.py --entries 8000 --workers 7 --max-pages 150
```

## 🏗️ System Architecture

### Two-Phase Pipeline

**Phase 1: Data Scraping**
1. **Sequential table scraping** - Collect entry URLs and metadata from results tables
2. **Parallel individual processing** - Fetch detailed data from individual entry pages
3. **Progress tracking** - Real-time statistics and time estimation

**Phase 2: Data Cleaning**
1. **Field extraction** - Extract specified target fields
2. **Data standardization** - Normalize institutions, decisions, degrees
3. **Quality filtering** - Remove invalid or incomplete entries

### Performance Optimization

- **Parallel processing** with configurable worker threads
- **Batch processing** for memory efficiency
- **Connection pooling** for network optimization
- **Progressive backups** every 500 entries
- **Smart error handling** with graceful degradation

## 📊 Performance Metrics

### Expected Processing Times

| Entries | Normal Mode | Fast Mode | Workers | Est. Time |
|---------|-------------|-----------|---------|-----------|
| 1,000 | 2-3/sec | 3-5/sec | 5 | 8-15 min |
| 5,000 | 2-3/sec | 3-5/sec | 6 | 30-60 min |
| 10,000 | 2-3/sec | 3-5/sec | 8 | 1-2 hours |
| 25,000+ | 2-3/sec | 3-5/sec | 8-10 | 3-5 hours |

### Resource Usage
- **Memory**: ~100-500MB depending on dataset size
- **Network**: ~1-2 KB per entry
- **CPU**: Low to moderate (depends on worker count)

## 📄 Output Data Structure

### Raw Data (`gradcafe_complete_data.json`)
Complete scraped data with all available fields:
```json
{
  "entry_id": 986072,
  "entry_url": "https://www.thegradcafe.com/result/986072",
  "added_on_date": "June 01, 2025",
  "institution": "Stanford University",
  "program": "Computer Science PhD",
  "decision": "Accepted",
  "decision_standardized": "Accepted",
  "gpa": "3.85",
  "gre_verbal": "165",
  "gre_quantitative": "170",
  "notes": "Amazing experience! The interview went really well...",
  "notes_length": 245,
  "degree_type": "PhD",
  "country_origin": "International"
}
```

### Clean Data (`applicant_data.json`)
Filtered data with target fields only:
```json
{
  "entry_id": 986072,
  "institution": "Stanford University",
  "program": "Computer Science PhD", 
  "notes": "Amazing experience! The interview went really well...",
  "added_on_date": "June 01, 2025",
  "entry_url": "https://www.thegradcafe.com/result/986072",
  "decision": "Accepted",
  "country_origin": "International",
  "degree_type": "PhD"
}
```

## 🛠️ Individual Module Usage

### Running Modules Separately

```bash
# Run only the scraper (generates gradcafe_complete_data.json)
python scrape.py

# Run only the cleaner (requires existing raw data)
python clean.py

# Custom scraping parameters
python scrape.py --target_entries 5000 --max_pages 50
```

### Module APIs

```python
# Use scraper programmatically
from scrape import GradCafeScraper

scraper = GradCafeScraper()
data = scraper.scrape_data(target_entries=1000, max_pages=20)

# Use cleaner programmatically  
from clean import GradCafeDataCleaner

cleaner = GradCafeDataCleaner()
clean_data = cleaner.clean_data()
```

## 🔧 Configuration & Customization

### Adjusting for Large Datasets

**For 10,000+ entries:**
```bash
python main.py --entries 15000 --workers 8 --batch-size 100
```

**For maximum speed (use carefully):**
```bash
python main.py --entries 10000 --fast --workers 10 --batch-size 150
```

### Server-Friendly Settings

**Recommended for continuous use:**
```bash
python main.py --entries 5000 --workers 4 --batch-size 25
```

### Memory Optimization

- Increase `--batch-size` for faster processing
- Decrease `--batch-size` for lower memory usage
- Monitor with Task Manager/Activity Monitor

## 🐛 Troubleshooting

### Common Issues

**1. No data collected**
```bash
# Check internet connection and try with fewer workers
python main.py --entries 100 --workers 2
```

**2. High failure rate**
```bash
# Use normal mode instead of fast mode
python main.py --entries 1000  # Remove --fast flag
```

**3. Memory issues with large datasets**
```bash
# Reduce batch size
python main.py --entries 10000 --batch-size 25
```

**4. Connection timeouts**
```bash
# Reduce workers and add delays
python main.py --entries 5000 --workers 3
```

### Debug Files

The scraper generates debug files for troubleshooting:
- `debug_results_table_page_*.html` - Main results table HTML
- `debug_individual_entry_*.html` - Sample individual entry pages
- `debug_headers_page_*.txt` - Table header analysis
- `gradcafe_progress_backup_*.json` - Progress backups

### Error Recovery

If the scraper fails partway through:
1. Check for progress backup files
2. Use `--clean-only` to process existing raw data
3. Restart with remaining entries needed

## ⚖️ Ethical Usage

### Rate Limiting
- Built-in delays between requests (0.5-1.2 seconds)
- Respectful parallel processing limits
- Server-friendly default settings

### Best Practices
- Use normal mode for large datasets
- Avoid excessive parallel workers (>10)
- Run during off-peak hours for large collections
- Respect the website's terms of service

## 📈 Scaling Recommendations

### Small Scale (1,000-5,000 entries)
```bash
python main.py --entries 3000 --workers 5
```

### Medium Scale (5,000-15,000 entries)
```bash
python main.py --entries 10000 --workers 6 --batch-size 75
```

### Large Scale (15,000+ entries)
```bash
python main.py --entries 25000 --workers 8 --batch-size 100
```

## 🤝 Contributing

### Code Structure
- `main.py` - Entry point and orchestration
- `scrape.py` - Core scraping logic
- `clean.py` - Data processing and filtering

### Adding Features
1. Modify individual modules as needed
2. Update main.py CLI options if necessary
3. Test with small datasets first

## 📝 License

This project is for educational and research purposes. Please respect thegradcafe.com's terms of service and use responsibly.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review debug files generated during execution
3. Start with smaller datasets to isolate problems
4. Ensure all dependencies are properly installed

## Known Bugs

The only bug I am currently aware of is that the season/term is not correctly extracted from the main survey URL. I was able to successfully extract the other fields in my scrape.py file. The clean.py file does not currently include all of the necessary information provided in the Module assignment documentation. To remedy this, I plan to work with an AI assistant to correctly extract the HTML portion that relates to the season/term the student intends to enroll in. I intend to use the inspect tool to dig into the HTML to find where the season/term is located to properly extract it.
---

**Happy scraping! 🎓📊**
