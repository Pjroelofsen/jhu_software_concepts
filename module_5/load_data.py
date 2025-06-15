# module_5/load_data.py
"""Module for loading applicant JSON data into PostgreSQL."""

# pylint: disable=too-many-locals,too-many-branches,too-many-statements,duplicate-code

import json
from datetime import datetime
import psycopg2


def parse_gpa(gpa_str):
    """Parse GPA from string like 'GPA 3.75'."""
    if not gpa_str or not gpa_str.startswith("GPA "):
        return None
    try:
        return float(gpa_str.replace("GPA ", "").strip())
    except ValueError:
        return None


def parse_gre_score(score_str, prefix):
    """Parse GRE score from string with given prefix."""
    if not score_str or not score_str.startswith(prefix):
        return None
    try:
        return float(score_str.replace(prefix, "").strip())
    except ValueError:
        return None


def parse_date(date_str):
    """Parse date from 'Added on Month DD, YYYY'."""
    if not date_str or not date_str.startswith("Added on "):
        return None
    try:
        _, date_part = date_str.split("Added on ", 1)
        return datetime.strptime(date_part, "%B %d, %Y").date()
    except (ValueError, IndexError):
        return None


def load_json_to_postgres():
    """Load JSON data into PostgreSQL table application_data."""
    db_config = {
        'host': 'localhost',
        'database': 'module3',
        'user': 'postgres',  # Change as needed
        'password': 'your_password',
        'port': '5432'
    }
    json_file_path = "cleaned_applicant_data_10000.json"

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        create_table_sql = (
            "CREATE TABLE IF NOT EXISTS application_data ("
            "p_id SERIAL PRIMARY KEY, "
            "program TEXT, "
            "comments TEXT, "
            "date_added DATE, "
            "url TEXT, "
            "status TEXT, "
            "term TEXT, "
            "us_or_international TEXT, "
            "gpa NUMERIC, "
            "gre NUMERIC, "
            "gre_v NUMERIC, "
            "gre_aw NUMERIC"
            ");"
        )
        cur.execute(create_table_sql)
        conn.commit()

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        insert_sql = (
            "INSERT INTO application_data "
            "(program, comments, date_added, url, status, term, "
            "us_or_international, gpa, gre, gre_v, gre_aw) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        for record in data:
            date_added = parse_date(record.get("Added on", ""))
            gpa = parse_gpa(record.get("GPA", ""))
            gre = parse_gre_score(record.get("GRE", ""), "GRE ")
            gre_v = parse_gre_score(record.get("GRE V", ""), "GRE V ")
            gre_aw = parse_gre_score(record.get("GRE AW", ""), "GRE AW ")

            cur.execute(
                insert_sql,
                (
                    record.get("program"),
                    record.get("notes"),
                    date_added,
                    record.get("url"),
                    record.get("status"),
                    record.get("term"),
                    record.get("US/International"),
                    gpa,
                    gre,
                    gre_v,
                    gre_aw,
                ),
            )
        conn.commit()
    except FileNotFoundError as error:
        print(f"JSON file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON format: {error}")
    except psycopg2.Error as error:
        print(f"Database error: {error}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_json_to_postgres()
