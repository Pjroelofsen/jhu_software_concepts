#!/usr/bin/env python3
import json
import re

INPUT_FILE  = 'applicant_data.json'
OUTPUT_FILE = 'cleaned_applicant_data.json'

def clean_degree(raw_deg: str) -> str:
    # collapse all whitespace into single spaces, remove “Degree”
    deg = re.sub(r'\s+', ' ', raw_deg).strip()
    deg = re.sub(r'\bDegree\b', '', deg).strip()
    return deg

def clean_comments(raw: str) -> str:
    # collapse whitespace into single spaces
    txt = re.sub(r'\s+', ' ', raw).strip()
    # drop any full-page UI dumps
    if txt.lower().startswith("timeline"):
        return ""
    return txt

def clean_status(raw_status: str) -> str:
    # keep only the decision word(s) before " on ..."
    return raw_status.split(' on ', 1)[0].strip()

def clean_record(rec: dict) -> dict:
    return {
        'program':           rec.get('program', '').strip(),
        'comments':          clean_comments(rec.get('comments', '')),
        'date_added':        rec.get('date_added', '').strip(),
        'url':               rec.get('url', '').strip(),
        'status':            clean_status(rec.get('status', '').strip()),
        'term':              rec.get('term', '').strip(),
        'US/International':  rec.get('US/International', '').strip(),
        'Degree':            clean_degree(rec.get('Degree', ''))
    }

def main():
    # load raw scraped data
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    cleaned = []
    seen_urls = set()
    for rec in raw:
        url = rec.get('url', '').strip()
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        cleaned.append(clean_record(rec))

    # write out only the 8 clean fields per record
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=4)

    print(f"Cleaned {len(cleaned)} records → {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
