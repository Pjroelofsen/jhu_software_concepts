# module_5/query_data.py
"""Module for querying application data from PostgreSQL and printing results."""

# pylint: disable=duplicate-code

import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'module3',
    'user': 'postgres',  # Change as needed
    'password': 'your_password',
    'port': '5432'
}


def get_connection():
    """Create and return a new database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as error:
        print(f"Error connecting to database: {error}")
        return None


def execute_query(query, description):
    """Execute SQL query and return a list of dict results."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        return cur.fetchall()
    except psycopg2.Error as error:
        print(f"Error executing {description}: {error}")
        return None
    finally:
        conn.close()


def query_1_fall_2024_count():
    """Query 1: Count of Fall 2024 applications."""
    query = (
        "SELECT COUNT(*) AS total_fall2024 "
        "FROM application_data "
        "WHERE term = 'Fall 2024';"
    )
    results = execute_query(query, "Fall 2024 Count")
    if results:
        data = results[0]
        print("=== QUERY 1: Fall 2024 Application Count ===")
        print(f"Total Fall 2024 applications: {data['total_fall2024']:,}")
    return results


def query_2_international_percentage():
    """Query 2: Percentage of international students."""
    query = (
        "SELECT "
        "COUNT(*) AS total_entries, "
        "COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) AS international_entries, "
        "ROUND((COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*)), 2) AS international_percentage "
        "FROM application_data;"
    )
    results = execute_query(query, "International Percentage")
    if results:
        data = results[0]
        print("=== QUERY 2: International Students ===")
        print(f"Total entries: {data['total_entries']:,}")
        print(f"International entries: {data['international_entries']:,}")
        print(f"International percentage: {data['international_percentage']}%")
    return results


def main():
    """Interactive menu to run queries."""
    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
            if num == 1:
                query_1_fall_2024_count()
            elif num == 2:
                query_2_international_percentage()
            else:
                print(f"Query {num} not implemented.")
        except ValueError:
            print("Please provide a valid query number.")
    else:
        print("Usage: python query_data.py <query_number>")


if __name__ == "__main__":
    main()
