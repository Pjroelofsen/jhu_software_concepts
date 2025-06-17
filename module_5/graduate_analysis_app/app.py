"""Flask application for graduate analysis data visualizations."""

from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

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
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as err:
        print(f"Error connecting to database: {err}")
        return None


def execute_query(query, params=None, description="Query"):
    """Execute a SQL object with optional parameters and return results with error handling."""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            return None
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params)
        return cur.fetchall()
    except psycopg2.Error as err:
        print(f"Error executing {description}: {err}")
        return None
    finally:
        if conn:
            conn.close()


# Composed SQL statements with identifiers, placeholders, and inherent limits
TABLE = sql.Identifier('application_data')

SQL_FALL_2024_COUNT = sql.SQL(
    "SELECT COUNT(*) AS fall_2024_count FROM {tbl} WHERE term = %s LIMIT 1"
).format(tbl=TABLE)

SQL_INTERNATIONAL_PERCENTAGE = sql.SQL(
    "SELECT "
    "COUNT(*) AS total_entries, "
    "COUNT(CASE WHEN us_or_international = %s THEN 1 END) AS international_entries, "
    "ROUND((COUNT(CASE WHEN us_or_international = %s THEN 1 END) * 100.0 / COUNT(*)), 2) "
    "AS international_percentage FROM {tbl} LIMIT 1"
).format(tbl=TABLE)

SQL_AVERAGE_SCORES = sql.SQL(
    "SELECT "
    "ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa, "
    "ROUND(AVG(gre)::NUMERIC, 2) AS avg_gre_quant, "
    "ROUND(AVG(gre_v)::NUMERIC, 2) AS avg_gre_verbal, "
    "ROUND(AVG(gre_aw)::NUMERIC, 2) AS avg_gre_writing "
    "FROM {tbl} LIMIT 1"
).format(tbl=TABLE)

SQL_AVG_GPA_AMERICAN_FALL2024 = sql.SQL(
    "SELECT ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa_american_fall2024 "
    "FROM {tbl} WHERE us_or_international = %s AND term = %s AND gpa IS NOT NULL LIMIT 1"
).format(tbl=TABLE)

SQL_ACCEPTANCE_RATE = sql.SQL(
    "SELECT ROUND((COUNT(CASE WHEN status LIKE %s THEN 1 END) * 100.0 / COUNT(*))::NUMERIC, 2) "
    "AS acceptance_percentage FROM {tbl} WHERE term = %s LIMIT 1"
).format(tbl=TABLE)

SQL_AVG_GPA_ACCEPTED_FALL2024 = sql.SQL(
    "SELECT ROUND(AVG(gpa)::NUMERIC, 2) AS avg_gpa_accepted_fall2024 "
    "FROM {tbl} WHERE term = %s AND status LIKE %s AND gpa IS NOT NULL LIMIT 1"
).format(tbl=TABLE)

SQL_JHU_CS_MASTERS_COUNT = sql.SQL(
    "SELECT COUNT(*) AS jhu_cs_masters_count FROM {tbl}"
    "WHERE (program ILIKE %s OR program ILIKE %s)"
    "AND program ILIKE %s AND degree ILIKE %s LIMIT 1"
).format(tbl=TABLE)


def get_all_analysis_data():
    """Get all analysis data by running each composed SQL statement with placeholders."""
    data = {}

    # Query 1
    res1 = execute_query(SQL_FALL_2024_COUNT, ('Fall 2024',), "Fall 2024 Count")
    data['fall_2024_count'] = res1[0]['fall_2024_count'] if res1 else 0

    # Query 2
    res2 = execute_query(
        SQL_INTERNATIONAL_PERCENTAGE,
        ('International', 'International'),
        "International Percentage"
    )
    if res2:
        data['total_entries'] = res2[0]['total_entries']
        data['international_entries'] = res2[0]['international_entries']
        data['international_percentage'] = res2[0]['international_percentage']
    else:
        data.update({
            'total_entries': 0,
            'international_entries': 0,
            'international_percentage': 0
        })

    # Query 3
    res3 = execute_query(SQL_AVERAGE_SCORES, None, "Average Scores")
    if res3:
        data.update({
            'avg_gpa': res3[0]['avg_gpa'],
            'avg_gre_quant': res3[0]['avg_gre_quant'],
            'avg_gre_verbal': res3[0]['avg_gre_verbal'],
            'avg_gre_writing': res3[0]['avg_gre_writing']
        })
    else:
        data.update({
            'avg_gpa': 0,
            'avg_gre_quant': 0,
            'avg_gre_verbal': 0,
            'avg_gre_writing': 0
        })

    # Query 4
    res4 = execute_query(
        SQL_AVG_GPA_AMERICAN_FALL2024,
        ('American', 'Fall 2024'),
        "American GPA Fall 2024"
    )
    data['avg_gpa_american_fall2024'] = res4[0]['avg_gpa_american_fall2024'] if res4 else 0

    # Query 5
    res5 = execute_query(
        SQL_ACCEPTANCE_RATE,
        ('%Accept%', 'Fall 2024'),
        "Fall 2024 Acceptance Rate"
    )
    data['acceptance_percentage'] = res5[0]['acceptance_percentage'] if res5 else 0

    # Query 6
    res6 = execute_query(
        SQL_AVG_GPA_ACCEPTED_FALL2024,
        ('Fall 2024', '%Accept%'),
        "Accepted GPA Fall 2024"
    )
    data['avg_gpa_accepted_fall2024'] = res6[0]['avg_gpa_accepted_fall2024'] if res6 else 0

    # Query 7
    res7 = execute_query(
        SQL_JHU_CS_MASTERS_COUNT,
        ('%johns hopkins%', '%jhu%', '%computer science%', '%masters%'),
        "JHU CS Masters"
    )
    data['jhu_cs_masters_count'] = res7[0]['jhu_cs_masters_count'] if res7 else 0

    return data


@app.route('/')
def index():
    """Main route that displays the analysis page."""
    try:
        analysis_data = get_all_analysis_data()
        return render_template('analysis.html', data=analysis_data)
    except Exception as err:  # pylint: disable=broad-exception-caught
        return f"Error loading data: {err}", 500


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
