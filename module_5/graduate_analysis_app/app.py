# module_5/graduate_analysis_app/app.py

"""
Flask application that serves analysis of the GradCafe data.
"""

from flask import Flask, render_template
from query_data import execute_query

app = Flask(__name__)


@app.route("/")
def index():
    """Main route that displays the analysis page."""
    try:
        data = {}
        data["fall_2024_count"] = execute_query(
            "SELECT COUNT(*) AS fall_2024_count "
            "FROM application_data WHERE term = 'Fall 2024';",
            "Fall 2024 Count"
        )[0]["fall_2024_count"]
        # … repeat the same pattern for the remaining six queries …
        return render_template("analysis.html", data=data)
    except (IndexError, KeyError, TypeError) as error:
        return f"Error loading data: {error}", 500


@app.errorhandler(404)
def not_found(_error):
    """Custom 404 handler."""
    return "Page not found", 404


@app.errorhandler(500)
def internal_error(_error):
    """Custom 500 handler."""
    return "Internal server error", 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
