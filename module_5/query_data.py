# module_5/query_data.py

"""
Provides functions to connect to the database and execute predefined analytics queries,
and a CLI to run them.
"""

import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "module3",
    "user": "postgres",          # Change as needed
    "password": "your_password", # Change as needed
    "port": "5432",
}


def get_connection():
    """Create and return a database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as error:
        print(f"Error connecting to database: {error}")
        sys.exit(1)


def execute_query(query, description="Query"):
    """Execute a SQL query and return fetched results."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        return cur.fetchall()
    except psycopg2.Error as error:
        print(f"Error executing {description}: {error}")
        return []
    finally:
        if conn:
            conn.close()


def query_1_fall_2024_count():
    """Query 1: Count entries for Fall 2024."""
    sql = (
        "SELECT COUNT(*) AS fall_2024_count "
        "FROM application_data WHERE term = 'Fall 2024';"
    )
    results = execute_query(sql, "Fall 2024 Count")
    if results:
        count = results[0]["fall_2024_count"]
        print("=== QUERY 1: Fall 2024 Applications ===")
        print(f"Total Fall 2024 applications: {count:,}")
    return results


def query_2_international_percentage():
    """Query 2: International students percentage."""
    sql = """
    SELECT
      COUNT(*) AS total_entries,
      COUNT(CASE WHEN us_or_international = 'International' THEN 1 END)
        AS international_entries,
      ROUND(
        COUNT(CASE WHEN us_or_international = 'International' THEN 1 END)
        * 100.0 / COUNT(*),
        2
      ) AS international_percentage
    FROM application_data;
    """
    results = execute_query(sql, "International Percentage")
    if results:
        data = results[0]
        print("=== QUERY 2: International Students ===")
        print(f"Total entries: {data['total_entries']:,}")
        print(f"International entries: {data['international_entries']:,}")
        print(f"International percentage: {data['international_percentage']}%")
    return results


def query_3_average_scores():
    """Query 3: Average GPA and GRE scores for those who provided them."""
    sql = """
    SELECT
      COUNT(gpa) AS gpa_count,
      ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa,
      COUNT(gre) AS gre_quant_count,
      ROUND(AVG(gre)::NUMERIC, 2) AS avg_gre_quant,
      COUNT(gre_v) AS gre_verbal_count,
      ROUND(AVG(gre_v)::NUMERIC, 2) AS avg_gre_verbal,
      COUNT(gre_aw) AS gre_writing_count,
      ROUND(AVG(gre_aw)::NUMERIC, 2) AS avg_gre_writing
    FROM application_data;
    """
    results = execute_query(sql, "Average Scores")
    if results:
        data = results[0]
        print("=== QUERY 3: Average Scores ===")
        print(f"GPA: {data['gpa_count']:,} applicants, avg = {data['avg_gpa']}")
        print(
            f"GRE Quant: {data['gre_quant_count']:,}, "
            f"avg = {data['avg_gre_quant']}"
        )
        print(
            f"GRE Verbal: {data['gre_verbal_count']:,}, "
            f"avg = {data['avg_gre_verbal']}"
        )
        print(
            f"GRE Writing: {data['gre_writing_count']:,}, "
            f"avg = {data['avg_gre_writing']}"
        )
    return results


def query_4_american_gpa_fall_2024():
    """Query 4: Average GPA of American students in Fall 2024."""
    sql = """
    SELECT
      COUNT(gpa) AS american_students_with_gpa,
      ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa_american_fall2024
    FROM application_data
    WHERE us_or_international = 'American'
      AND term = 'Fall 2024'
      AND gpa IS NOT NULL;
    """
    results = execute_query(sql, "American GPA Fall 2024")
    if results:
        data = results[0]
        print("=== QUERY 4: American Students GPA ===")
        print(
            f"American with GPA: "
            f"{data['american_students_with_gpa']:,}"
        )
        print(f"Average GPA: {data['avg_gpa_american_fall2024']}")
    return results


def query_5_fall_2024_acceptance_rate():
    """Query 5: Acceptance rate for Fall 2024."""
    sql = """
    SELECT
      COUNT(*) AS total_fall2024,
      COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END)
        AS acceptances,
      ROUND(
        COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END)
        * 100.0 / COUNT(*),
        2
      ) AS acceptance_percentage
    FROM application_data
    WHERE term = 'Fall 2024';
    """
    results = execute_query(sql, "Fall 2024 Acceptance Rate")
    if results:
        data = results[0]
        print("=== QUERY 5: Acceptance Rate ===")
        print(f"Total: {data['total_fall2024']:,}")
        print(f"Acceptances: {data['acceptances']:,}")
        print(f"Rate: {data['acceptance_percentage']}%")
    return results


def query_6_accepted_gpa_fall_2024():
    """Query 6: Average GPA of accepted applicants for Fall 2024."""
    sql = """
    SELECT
      COUNT(gpa) AS accepted_students_with_gpa,
      ROUND(AVG(gpa)::NUMERIC, 2)
        AS avg_gpa_accepted_fall2024
    FROM application_data
    WHERE term = 'Fall 2024'
      AND status LIKE '%Accept%'
      AND gpa IS NOT NULL;
    """
    results = execute_query(sql, "Accepted GPA Fall 2024")
    if results:
        data = results[0]
        print("=== QUERY 6: Accepted Students GPA ===")
        print(
            f"Accepted with GPA: "
            f"{data['accepted_students_with_gpa']:,}"
        )
        print(
            f"Avg GPA: {data['avg_gpa_accepted_fall2024']}"
        )
    return results


def query_7_jhu_cs_masters():
    """Query 7: Johns Hopkins CS Masters applications."""
    sql = """
    SELECT COUNT(*) AS jhu_cs_masters_count
    FROM application_data
    WHERE (program ILIKE '%johns hopkins%' OR program ILIKE '%jhu%')
      AND program ILIKE '%computer science%'
      AND degree ILIKE '%masters%';
    """
    results = execute_query(sql, "JHU CS Masters")
    if results:
        count = results[0]["jhu_cs_masters_count"]
        print("=== QUERY 7: JHU CS Masters ===")
        print(f"Applications: {count:,}")
    return results


def run_all_queries():
    """Run all queries in sequence."""
    print("Running all database queries...\n")
    query_1_fall_2024_count()
    print()
    query_2_international_percentage()
    print()
    query_3_average_scores()
    print()
    query_4_american_gpa_fall_2024()
    print()
    query_5_fall_2024_acceptance_rate()
    print()
    query_6_accepted_gpa_fall_2024()
    print()
    query_7_jhu_cs_masters()
    print()


def run_specific_query(query_num):
    """Run a specific query by its number."""
    queries = {
        -1: run_all_queries,
        1: query_1_fall_2024_count,
        2: query_2_international_percentage,
        3: query_3_average_scores,
        4: query_4_american_gpa_fall_2024,
        5: query_5_fall_2024_acceptance_rate,
        6: query_6_accepted_gpa_fall_2024,
        7: query_7_jhu_cs_masters,
    }
    func = queries.get(query_num)
    if func:
        return func()
    print(f"Invalid query number: {query_num}")
    print("Use -1 for all queries, or 1–7 for specific ones.")
    return []


def main():
    """CLI entry point."""
    if len(sys.argv) > 1:
        try:
            query_number = int(sys.argv[1])
            if query_number == -1:
                run_all_queries()
            else:
                run_specific_query(query_number)
        except ValueError as error:
            print(f"Please provide a valid integer query number: {error}")
    else:
        print("Usage: python query_data.py [query_number]")
        print("  -1 = run all; 1–7 = individual queries.")


if __name__ == "__main__":
    main()
