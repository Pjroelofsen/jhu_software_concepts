import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'module3',
    'user': 'postgres',  # Change to your PostgreSQL username
    'password': 'your_password',  # Change to your PostgreSQL password
    'port': '5432'
}

def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def execute_query(query, description="Query"):
    """Execute a query and return results with error handling."""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg2.Error as e:
        print(f"Error executing {description}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_data():
    """Get all data from application_data table (use with caution for large datasets)."""
    query = "SELECT * FROM application_data LIMIT 100;"  # Limited to 100 for safety
    results = execute_query(query, "Get All Data")
    
    if results:
        print("=== ALL DATA (First 100 records) ===")
        print(f"Retrieved {len(results)} records")
        for i, record in enumerate(results[:5]):  # Show first 5 as sample
            print(f"\nRecord {i+1}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
        if len(results) > 5:
            print(f"\n... and {len(results) - 5} more records")
    return results

def query_1_fall_2024_count():
    """Query 1: Count entries for Fall 2024."""
    query = "SELECT COUNT(*) as fall_2024_count FROM application_data WHERE term = 'Fall 2024';"
    results = execute_query(query, "Fall 2024 Count")
    
    if results:
        count = results[0]['fall_2024_count']
        print("=== QUERY 1: Fall 2024 Applications ===")
        print(f"Total Fall 2024 applications: {count:,}")
    return results

def query_2_international_percentage():
    """Query 2: International students percentage."""
    query = """
    SELECT 
        COUNT(*) as total_entries,
        COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) as international_entries,
        ROUND(
            (COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*)), 
            2
        ) as international_percentage
    FROM application_data;
    """
    results = execute_query(query, "International Percentage")
    
    if results:
        data = results[0]
        print("=== QUERY 2: International Students ===")
        print(f"Total entries: {data['total_entries']:,}")
        print(f"International entries: {data['international_entries']:,}")
        print(f"International percentage: {data['international_percentage']}%")
    return results

def query_3_average_scores():
    """Query 3: Average GPA and GRE scores for applicants who provided these metrics."""
    query = """
    SELECT 
        COUNT(gpa) as gpa_count,
        ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa,
        COUNT(gre) as gre_quant_count,
        ROUND(AVG(gre)::NUMERIC, 2) as avg_gre_quant,
        COUNT(gre_v) as gre_verbal_count,
        ROUND(AVG(gre_v)::NUMERIC, 2) as avg_gre_verbal,
        COUNT(gre_aw) as gre_writing_count,
        ROUND(AVG(gre_aw)::NUMERIC, 2) as avg_gre_writing
    FROM application_data;
    """
    results = execute_query(query, "Average Scores")
    
    if results:
        data = results[0]
        print("=== QUERY 3: Average Scores ===")
        print(f"GPA: {data['gpa_count']:,} applicants, average = {data['avg_gpa']}")
        print(f"GRE Quant: {data['gre_quant_count']:,} applicants, average = {data['avg_gre_quant']}")
        print(f"GRE Verbal: {data['gre_verbal_count']:,} applicants, average = {data['avg_gre_verbal']}")
        print(f"GRE Writing: {data['gre_writing_count']:,} applicants, average = {data['avg_gre_writing']}")
    return results

def query_4_american_gpa_fall_2024():
    """Query 4: Average GPA of American students in Fall 2024."""
    query = """
    SELECT 
        COUNT(gpa) as american_students_with_gpa,
        ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_american_fall2024
    FROM application_data 
    WHERE us_or_international = 'American' 
      AND term = 'Fall 2024' 
      AND gpa IS NOT NULL;
    """
    results = execute_query(query, "American GPA Fall 2024")
    
    if results:
        data = results[0]
        print("=== QUERY 4: American Students GPA (Fall 2024) ===")
        print(f"American students with GPA: {data['american_students_with_gpa']:,}")
        print(f"Average GPA: {data['avg_gpa_american_fall2024']}")
    return results

def query_5_fall_2024_acceptance_rate():
    """Query 5: Acceptance rate for Fall 2024."""
    query = """
    SELECT 
        COUNT(*) as total_fall2024,
        COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END) as acceptances,
        ROUND(
            (COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END) * 100.0 / COUNT(*))::NUMERIC, 
            2
        ) as acceptance_percentage
    FROM application_data 
    WHERE term = 'Fall 2024';
    """
    results = execute_query(query, "Fall 2024 Acceptance Rate")
    
    if results:
        data = results[0]
        print("=== QUERY 5: Fall 2024 Acceptance Rate ===")
        print(f"Total Fall 2024 applications: {data['total_fall2024']:,}")
        print(f"Acceptances: {data['acceptances']:,}")
        print(f"Acceptance rate: {data['acceptance_percentage']}%")
    return results

def query_6_accepted_gpa_fall_2024():
    """Query 6: Average GPA of accepted applicants for Fall 2024."""
    query = """
    SELECT 
        COUNT(gpa) as accepted_students_with_gpa,
        ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_accepted_fall2024
    FROM application_data 
    WHERE term = 'Fall 2024' 
      AND status LIKE '%Accept%'
      AND gpa IS NOT NULL;
    """
    results = execute_query(query, "Accepted GPA Fall 2024")
    
    if results:
        data = results[0]
        print("=== QUERY 6: Accepted Students GPA (Fall 2024) ===")
        print(f"Accepted students with GPA: {data['accepted_students_with_gpa']:,}")
        print(f"Average GPA of accepted students: {data['avg_gpa_accepted_fall2024']}")
    return results

def query_7_jhu_cs_masters():
    """Query 7: Johns Hopkins University Computer Science Masters applications."""
    query = """
    SELECT COUNT(*) as jhu_cs_masters_count
    FROM application_data 
    WHERE (program ILIKE '%johns hopkins%' OR program ILIKE '%jhu%')
      AND program ILIKE '%computer science%'
      AND degree ILIKE '%masters%';
    """
    results = execute_query(query, "JHU CS Masters")
    
    if results:
        count = results[0]['jhu_cs_masters_count']
        print("=== QUERY 7: Johns Hopkins CS Masters ===")
        print(f"JHU Computer Science Masters applications: {count:,}")
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
    """Run a specific query by number."""
    query_functions = {
        0: get_all_data,
        1: query_1_fall_2024_count,
        2: query_2_international_percentage,
        3: query_3_average_scores,
        4: query_4_american_gpa_fall_2024,
        5: query_5_fall_2024_acceptance_rate,
        6: query_6_accepted_gpa_fall_2024,
        7: query_7_jhu_cs_masters
    }
    
    if query_num in query_functions:
        return query_functions[query_num]()
    else:
        print(f"Invalid query number: {query_num}")
        print("Available queries: 0 (all data), 1-7 (specific queries)")
        return None

def main():
    """Main function with interactive menu."""
    if len(sys.argv) > 1:
        try:
            query_num = int(sys.argv[1])
            if query_num == -1:
                run_all_queries()
            else:
                run_specific_query(query_num)
        except ValueError:
            print("Please provide a valid query number (0-7) or -1 for all queries")
    else:
        print("Database Query Tool")
        print("===================")
        print("Available options:")
        print("  0: Get all data (limited to 100 records)")
        print("  1: Fall 2024 application count")
        print("  2: International students percentage")
        print("  3: Average GPA and GRE scores")
        print("  4: American students GPA (Fall 2024)")
        print("  5: Fall 2024 acceptance rate")
        print("  6: Accepted students GPA (Fall 2024)")
        print("  7: Johns Hopkins CS Masters count")
        print("  -1: Run all queries")
        print("\nUsage:")
        print("  python query_data.py [query_number]")
        print("  python query_data.py -1  # Run all queries")
        print("  python query_data.py 1   # Run query 1 only")

if __name__ == "__main__":
    main()