# GraduateCafe Scraper & Cleaner

This project scrapes graduate application data from The GradCafe survey pages and cleans the resulting dataset into a structured JSON file.

## Features

* **Parallel scraping**: Uses `concurrent.futures.ThreadPoolExecutor` with HTTP keep-alive (`requests.Session`) for speed.
* **Configurable target**: Specify how many entries to collect (`TARGET` in `main.py`).
* **In-memory cleaning**: Collapses whitespace, strips unwanted artifacts, and extracts eight key fields.
* **One-step execution**: Run `main.py` to scrape and clean; outputs `cleaned_applicant_data.json`.

## Prerequisites

* **Python**: 3.10 or later
* **Virtual environment** (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

* Open `main.py` and adjust the following constants at the top if needed:

  ```python
  BASE_URL    = 'https://www.thegradcafe.com'
  TARGET      = 10000        # total entries to scrape
  MAX_WORKERS = 10           # threads for parallel fetching
  ```
* You can also tweak `time.sleep(0.2)` between pages to balance speed and politeness.

## Usage

Simply run the main script:

```bash
python main.py
```

This will:

1. Scrape survey pages starting from page 1 until it collects `TARGET` entries.
2. Clean the raw data in memory (no intermediate JSON files).
3. Write the final output to `cleaned_applicant_data.json`.

## Output

The output JSON contains an array of objects, each with the following fields:

* `program`: e.g. `Information Studies, McGill University`
* `comments`
* `date_added`: e.g. `Added on March 31, 2024`
* `url`
* `status`: e.g. `Accepted`, `Rejected`, `Wait listed`
* `term`: e.g. `Fall 2024`
* `US/International`
* `Degree`: e.g. `Masters`

## File Structure

```
├── main.py
├── requirements.txt
├── cleaned_applicant_data.json  # generated output
└── README.md
```

## License

This project is provided under the MIT License. Feel free to use and modify as needed.
