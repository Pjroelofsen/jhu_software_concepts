import requests
from bs4 import BeautifulSoup
import re, json, time
from datetime import datetime
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL    = 'https://www.thegradcafe.com'
TARGET      = 100
MAX_WORKERS = 10

# reuse a session for keep-alive
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def scrape_result(url: str) -> dict:
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    text = soup.get_text('\n')

    entry = {'url': url}

    # Program & Institution
    title = soup.find('title').get_text(strip=True)
    if ' - ' in title:
        prog, inst = title.split(' - ', 1)
        entry['program'] = f"{prog}, {inst}  "
    else:
        entry['program'] = title

    # Degree Type
    if m := re.search(r'Degree Type\s*([\w\s]+)', text):
        entry['Degree'] = m.group(1).strip()

    # Country
    if m := re.search(r"Degree's Country of Origin\s*(\w+)", text):
        entry['US/International'] = m.group(1)

    # Decision & Notification Date
    m_dec = re.search(r'Decision\s*(Accepted|Rejected|Interview|Wait listed)', text)
    decision = m_dec.group(1) if m_dec else ''
    if m_not := re.search(r'Notification\s*on\s*(\d{2})/(\d{2})/(\d{4})', text):
        d, mth, y = m_not.groups()
        dt = datetime.strptime(f"{d}/{mth}/{y}", "%d/%m/%Y")
        entry['status']     = decision  # we'll clean off the " on ..." later
        entry['date_added'] = f"Added on {dt.strftime('%B')} {dt.day}, {dt.year}"
    else:
        entry['status']     = decision
        entry['date_added'] = ''

    # GPA
    if m := re.search(r'Undergrad GPA\s*([\d\.]+)', text):
        entry['GPA'] = f"GPA {m.group(1)}"

    # GRE
    if m := re.search(r'GRE General:\s*(\d+)', text):
        entry['GRE']   = f"GRE {m.group(1)}"
    if m := re.search(r'GRE Verbal:\s*(\d+)', text):
        entry['GRE V'] = f"GRE V {m.group(1)}"
    if m := re.search(r'Analytical Writing:\s*([\d\.]+)', text):
        entry['GRE AW'] = f"GRE AW {m.group(1)}"

    # Notes → comments (strict dt/dd, filter out UI dumps)
    comments = ''
    notes_dt = soup.find('dt', string=re.compile(r'^\s*Notes\s*$', re.I))
    if notes_dt and (dd := notes_dt.find_next_sibling('dd')):
        raw = dd.get_text(separator=' ', strip=True)
        if not raw.lower().startswith('timeline'):
            comments = raw
    entry['comments'] = comments

    return entry

def scrape_survey_page(page_url: str) -> list:
    resp = session.get(page_url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # build list of (detail_url, term) pairs
    url_term_pairs = []
    for a in soup.find_all('a', href=re.compile(r'^/result/\d+')):
        detail_url = urljoin(BASE_URL, a['href'])
        term_tag   = a.find_next(string=re.compile(r'^(Fall|Spring) \d{4}$'))
        term       = term_tag.strip() if term_tag else ''
        url_term_pairs.append((detail_url, term))

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        # map future -> (url, term)
        future_to_meta = {
            pool.submit(scrape_result, url): (url, term)
            for url, term in url_term_pairs
        }
        for fut in as_completed(future_to_meta):
            url, term = future_to_meta[fut]
            try:
                rec = fut.result()
                rec['term'] = term
                results.append(rec)
            except Exception as e:
                print(f"❌ {url}: {e}")
    return results

if __name__ == '__main__':
    all_records = []
    seen_urls   = set()
    page_number = 1

    while len(all_records) < TARGET:
        survey_url = f'{BASE_URL}/survey/?page={page_number}'
        print(f"Scraping page {page_number}…")
        page_recs = scrape_survey_page(survey_url)
        if not page_recs:
            break

        for rec in page_recs:
            if rec['url'] not in seen_urls:
                seen_urls.add(rec['url'])
                all_records.append(rec)
                if len(all_records) >= TARGET:
                    break

        print(f" → Collected {len(all_records)}/{TARGET}")
        page_number += 1
        time.sleep(0.2)  # polite but faster

    # write out exactly TARGET entries
    all_records = all_records[:TARGET]
    with open('applicant_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    print(f"Done! Wrote {len(all_records)} records.")
