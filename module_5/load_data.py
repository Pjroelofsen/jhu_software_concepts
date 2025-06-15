import json
import psycopg2
from datetime import datetime
import sys

def parse_gpa(gpa_str):
    """Parse GPA from 'GPA 3.75' format"""
    if not gpa_str or not gpa_str.startswith('GPA '):
        return None
    try:
        return float(gpa_str.replace('GPA ', '').strip())
    except:
        return None

def parse_gre_score(score_str, prefix):
    """Parse GRE score from 'GRE 165' or 'GRE V 156' format"""
    if not score_str or not score_str.startswith(prefix):
        return None
    try:
        return float(score_str.replace(prefix, '').strip())
    except:
        return None

def parse_date(date_str):
    """Parse date from 'Added on March 31, 2024' format"""
    if not date_str or not date_str.startswith('Added on '):
        return None
    try:
        date_part = date_str.replace('Added on ', '')
        return datetime.strptime(date_part, '%B %d, %Y').date()
    except:
        return None

def load_json_to_postgres():
    # Database connection parameters
    db_config = {
        'host': 'localhost',
        'database': 'module3',
        'user': 'postgres',  # Change to your PostgreSQL username
        'password': 'your_password',  # Change to your PostgreSQL password
        'port': '5432'
    }
    
    # File path to your JSON file
    json_file_path = 'cleaned_applicant_data_10000.json'  # Your uploaded file
    
    conn = None
    cur = None
    
    try:
        # Step 1: Connect to PostgreSQL
        print("Step 1: Connecting to PostgreSQL...")
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        print("✓ Connected successfully!")
        
        # Step 2: Create table
        print("\nStep 2: Creating table...")
        create_table_query = """
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
        cur.execute(create_table_query)
        conn.commit()
        print("✓ Table created successfully!")
        
        # Step 3: Load JSON data
        print("\nStep 3: Loading JSON data...")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✓ Loaded {len(data)} records from JSON file")
        
        # Step 4: Process and insert data
        print("\nStep 4: Processing and inserting data...")
        
        insert_query = """
        INSERT INTO application_data 
        (program, comments, date_added, url, status, term, us_or_international, gpa, gre, gre_v, gre_aw, degree)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        successful_inserts = 0
        failed_inserts = 0
        
        for i, record in enumerate(data):
            try:
                # Parse all fields
                row_data = (
                    record.get('program', '').strip(),
                    record.get('comments', ''),
                    parse_date(record.get('date_added', '')),
                    record.get('url', ''),
                    record.get('status', ''),
                    record.get('term', ''),
                    record.get('US/International', ''),
                    parse_gpa(record.get('GPA', '')),
                    parse_gre_score(record.get('GRE', ''), 'GRE '),
                    parse_gre_score(record.get('GRE V', ''), 'GRE V '),
                    parse_gre_score(record.get('GRE AW', ''), 'GRE AW '),
                    record.get('Degree', '')
                )
                
                # Insert single record
                cur.execute(insert_query, row_data)
                successful_inserts += 1
                
                # Show progress every 1000 records
                if (i + 1) % 1000 == 0:
                    print(f"  Processed {i + 1} records...")
                    
            except Exception as e:
                failed_inserts += 1
                print(f"  Error on record {i + 1}: {e}")
                if failed_inserts > 10:  # Stop if too many errors
                    print("  Too many errors, stopping...")
                    break
        
        # Commit all changes
        conn.commit()
        print(f"✓ Successfully inserted {successful_inserts} records")
        if failed_inserts > 0:
            print(f"  Failed to insert {failed_inserts} records")
        
        # Step 5: Verify data
        print("\nStep 5: Verifying insertion...")
        try:
            cur.execute("SELECT COUNT(*) FROM application_data")
            result = cur.fetchone()
            if result and len(result) > 0:
                count = result[0]
                print(f"✓ Total records in database: {count}")
            else:
                print("✗ Could not get count")
        except Exception as e:
            print(f"✗ Error getting count: {e}")
        
        # Step 6: Show sample data
        print("\nStep 6: Showing sample data...")
        try:
            cur.execute("SELECT p_id, program, gpa, gre, degree FROM application_data LIMIT 3")
            samples = cur.fetchall()
            
            if samples:
                print("Sample records:")
                for i, row in enumerate(samples):
                    if row and len(row) >= 5:
                        print(f"  {i+1}. ID: {row[0]}, Program: {row[1][:50]}..., GPA: {row[2]}, GRE: {row[3]}, Degree: {row[4]}")
                    else:
                        print(f"  {i+1}. Incomplete row: {row}")
            else:
                print("No sample data found")
                
        except Exception as e:
            print(f"✗ Error retrieving samples: {e}")
        
        print("\n✓ Process completed successfully!")
        
    except psycopg2.Error as e:
        print(f"✗ Database error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError:
        print(f"✗ JSON file not found: {json_file_path}")
        print("Please check the file path and make sure the file exists.")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON format: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close connections
        if cur:
            cur.close()
        if conn:
            conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    load_json_to_postgres()