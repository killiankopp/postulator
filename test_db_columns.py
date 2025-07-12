import logging
import psycopg2
from db_service import get_database_url, init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_table_columns():
    """
    Check if all required columns exist in the documents table.
    """
    conn = None
    try:
        # Get the database URL
        db_url = get_database_url()
        
        # Initialize the database (this should create the table and add any missing columns)
        init_db()
        
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Get all columns from the documents table
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='documents'
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Define the required columns
        required_columns = ['entreprise', 'poste', 'source', 'identifiant', 'base_line', 'salaire', 
                           'description', 'skills_text', 'skill1', 'skill2', 'skill3']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if missing_columns:
            logger.error(f"Missing columns in documents table: {missing_columns}")
        else:
            logger.info("All required columns exist in the documents table.")
            logger.info(f"Existing columns: {existing_columns}")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error checking table columns: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    check_table_columns()