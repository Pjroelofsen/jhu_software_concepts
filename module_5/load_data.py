# module_5/load_data.py

"""
Loads cleaned GradCafe JSON into the PostgreSQL `application_data` table.
"""

import json
from datetime import datetime
from psycopg2 import Error as PqError

from query_data import get_connection

INSERT_QUERY = (
    """
    INSERT INTO application_data
      (program, comments, date_added, url, status, term,
       us_or_international, gpa, gre, gre_v, gre_aw, degree)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
)

CREATE_TABLE_SQL = (
    """
    CREATE TABLE IF NOT EXISTS application_data (
        p_id SERIAL PRIMARY KEY,
        program TEXT,
        comments TEXT,
        date_added DATE,
        url TEXT,
        status TEXT,
        term TEXT,
        us_or_international TEXT,
        gpa FLOAT,
        gre FLOAT,
        gre_v FLOAT,
        gre_aw FLOAT,
        degree TEXT
    );
    """
)


def parse_gpa(gpa_str):
    """Parse GPA string of form 'GPA 3.75' into float."""
    if not gpa_str or not gpa_str.startswith("GPA "):
        return None
    try:
        return float(gpa_str.replace("GPA ", "").strip())
    except ValueError:
        return None


def parse_gre(score_str, prefix):
    """Parse GRE score like 'GRE 165' or 'GRE V 156'."""
    if not score_str or not score_str.startswith(prefix):
        return None
    try:
        return float(score_str.replace(prefix, "").strip())
    except ValueError:
        return None


def parse_date(date_str):
    """Parse date string of form 'Added on March 31, 2024'."""
    if not date_str or not date_str.startswith("Added on "):
        return None
    try:
        part = date_str.replace("Added on ", "")
        return datetime.strptime(part, "%B %d, %Y").date()
    except ValueError:
        return None


def _load_json(path):
    """Load and return JSON data from file, or None on failure."""
    try:
        with open(path, encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Failed to read JSON file: {error}")
        return None


def _create_table(cur, conn):
    """Ensure application_data table exists."""
    try:
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
        print("✓ Table ready.")
    except PqError as error:
        print(f"Error creating table: {error}")
        conn.close()


def _insert_records(cur, conn, records):
    """Insert all records into the database, reporting progress."""
    success = 0
    errors = 0
    for idx, rec in enumerate(records, start=1):
        try:
            cur.execute(
                INSERT_QUERY,
                (
                    rec.get("program", "").strip(),
                    rec.get("comments", ""),
                    parse_date(rec.get("date_added", "")),
                    rec.get("url", ""),
                    rec.get("status", ""),
                    rec.get("term", ""),
                    rec.get("US/International", ""),
                    parse_gpa(rec.get("GPA", "")),
                    parse_gre(rec.get("GRE", ""), "GRE "),
                    parse_gre(rec.get("GRE V", ""), "GRE V "),
                    parse_gre(rec.get("GRE AW", ""), "GRE AW "),
                    rec.get("Degree", ""),
                ),
            )
            success += 1
        except PqError as error:
            errors += 1
            print(f"Error on record {idx}: {error}")
            if errors > 10:
                print("Too many errors, aborting.")
                break
    conn.commit()
    print(f"✓ Inserted {success} records; {errors} errors.")


def _verify_count(cur):
    """Print total record count from the database."""
    try:
        cur.execute("SELECT COUNT(*) FROM application_data;")
        total = cur.fetchone()[0]
        print(f"✓ Total in DB: {total}")
    except PqError as error:
        print(f"Count query error: {error}")


def _print_samples(cur):
    """Fetch and display a few sample rows."""
    try:
        cur.execute(
            "SELECT p_id, program, gpa, gre, degree "
            "FROM application_data LIMIT 3;"
        )
        rows = cur.fetchall()
        if rows:
            print("Sample records:")
            for i, row in enumerate(rows, start=1):
                pid, prog, gpa, gre, degree = row
                print(
                    f"  {i}. ID={pid}, prog={prog[:30]}..., "
                    f"GPA={gpa}, GRE={gre}, degree={degree}"
                )
        else:
            print("No samples.")
    except PqError as error:
        print(f"Sample query error: {error}")


def load_json_to_postgres(path="cleaned_applicant_data_10000.json"):
    """Orchestrate loading JSON data into PostgreSQL."""
    data = _load_json(path)
    if data is None:
        return

    conn = get_connection()
    cur = conn.cursor()
    print("✓ Connected to PostgreSQL.")

    _create_table(cur, conn)
    _insert_records(cur, conn, data)
    _verify_count(cur)
    _print_samples(cur)

    cur.close()
    conn.close()
    print("✓ Load complete.")


if __name__ == "__main__":
    load_json_to_postgres()
