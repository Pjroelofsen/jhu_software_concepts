"""Flask application for graduate analysis data visualizations."""

from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'module3',
    'user': 'phillip',  # Change to your PostgreSQL username
    'port': '5432'
}

def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def execute_query(query, description="Query"):
    """Execute a query and return results with error handling."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg2.Error as err:
        print(f"Error executing {description}: {err}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_analysis_data():
    """Get all analysis data by running all queries."""
    data = {}
    # Query 1: Fall 2024 count
    query1 = "SELECT COUNT(*) as fall_2024_count FROM application_data WHERE term = 'Fall 2024';"
    result1 = execute_query(query1, "Fall 2024 Count")
    data['fall_2024_count'] = result1[0]['fall_2024_count'] if result1 else 0
    # Query 2: International percentage
    query2 = """
    SELECT 
        COUNT(*) as total_entries,
        COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) as international_entries,
        ROUND(
            (COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*)), 
            2
        ) as international_percentage
    FROM application_data;
    """
    result2 = execute_query(query2, "International Percentage")
    if result2:
        data['total_entries'] = result2[0]['total_entries']
        data['international_entries'] = result2[0]['international_entries']
        data['international_percentage'] = result2[0]['international_percentage']
    else:
        data['total_entries'] = 0
        data['international_entries'] = 0
        data['international_percentage'] = 0
    # Query 3: Average scores
    query3 = """
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
    result3 = execute_query(query3, "Average Scores")
    if result3:
        data['avg_gpa'] = result3[0]['avg_gpa']
        data['avg_gre_quant'] = result3[0]['avg_gre_quant']
        data['avg_gre_verbal'] = result3[0]['avg_gre_verbal']
        data['avg_gre_writing'] = result3[0]['avg_gre_writing']
    else:
        data['avg_gpa'] = 0
        data['avg_gre_quant'] = 0
        data['avg_gre_verbal'] = 0
        data['avg_gre_writing'] = 0
    # Query 4: American GPA Fall 2024
    query4 = """
    SELECT 
        COUNT(gpa) as american_students_with_gpa,
        ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_american_fall2024
    FROM application_data 
    WHERE us_or_international = 'American' 
      AND term = 'Fall 2024' 
      AND gpa IS NOT NULL;
    """
    result4 = execute_query(query4, "American GPA Fall 2024")
    data['avg_gpa_american_fall2024'] = result4[0]['avg_gpa_american_fall2024'] if result4 else 0
    # Query 5: Fall 2024 acceptance rate
    query5 = """
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
    result5 = execute_query(query5, "Fall 2024 Acceptance Rate")
    if result5:
        data['acceptance_percentage'] = result5[0]['acceptance_percentage']
        data['total_fall2024'] = result5[0]['total_fall2024']
        data['acceptances'] = result5[0]['acceptances']
    else:
        data['acceptance_percentage'] = 0
        data['total_fall2024'] = 0
        data['acceptances'] = 0
    # Query 6: Accepted GPA Fall 2024
    query6 = """
    SELECT 
        COUNT(gpa) as accepted_students_with_gpa,
        ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_accepted_fall2024
    FROM application_data 
    WHERE term = 'Fall 2024' 
      AND status LIKE '%Accept%'
      AND gpa IS NOT NULL;
    """
    result6 = execute_query(query6, "Accepted GPA Fall 2024")
    data['avg_gpa_accepted_fall2024'] = result6[0]['avg_gpa_accepted_fall2024'] if result6 else 0
    # Query 7: JHU CS Masters
    query7 = """
    SELECT COUNT(*) as jhu_cs_masters_count
    FROM application_data 
    WHERE (program ILIKE '%johns hopkins%' OR program ILIKE '%jhu%')
      AND program ILIKE '%computer science%'
      AND degree ILIKE '%masters%';
    """
    result7 = execute_query(query7, "JHU CS Masters")
    data['jhu_cs_masters_count'] = result7[0]['jhu_cs_masters_count'] if result7 else 0
    return data

@app.route('/')
def index():
    """Main route that displays the analysis page."""
    try:
        analysis_data = get_all_analysis_data()
        return render_template('analysis.html', data=analysis_data)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return f"Error loading data: {str(err)}", 500

@app.errorhandler(404)
def not_found(_error):
    """Handle 404 errors."""
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(_error):
    """Handle 500 internal errors."""
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
