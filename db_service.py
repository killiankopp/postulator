"""
Database service for storing and retrieving document data.
"""
import os
import psycopg2
from psycopg2 import sql
import logging
from config import DATABASE_URL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_database_url():
    """
    Get the database URL based on the environment.

    Returns:
        str: The database URL to use for connections
    """
    # Use the configured DATABASE_URL from config.py
    db_url = DATABASE_URL

    # Log the connection details (without password)
    connection_info = db_url.replace(os.environ.get('DB_PASSWORD', ''), '********')
    logger.info(f"Connecting to database: {connection_info}")

    # Log environment variables for debugging
    logger.info(f"DB_HOST from env: {os.environ.get('DB_HOST', 'not set')}")
    logger.info(f"DB_PORT from env: {os.environ.get('DB_PORT', 'not set')}")

    return db_url

def init_db():
    """
    Initialize the database by creating the necessary tables if they don't exist.
    """
    conn = None
    try:
        # Get the database URL
        db_url = get_database_url()

        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Create documents table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                entreprise TEXT NOT NULL,
                poste TEXT NOT NULL,
                source TEXT,
                identifiant TEXT,
                base_line TEXT,
                salaire TEXT,
                description TEXT,
                skills_text TEXT,
                skill1 TEXT,
                skill2 TEXT,
                skill3 TEXT,
                skill4 TEXT,
                skill5 TEXT,
                skill6 TEXT,
                url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check for all required columns and add them if they don't exist
        required_columns = ['entreprise', 'poste', 'source', 'identifiant', 'base_line', 'salaire', 'description', 'skills_text', 'skill1', 'skill2', 'skill3', 'skill4', 'skill5', 'skill6', 'url']

        # Get existing columns
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='documents'
        """)
        existing_columns = [row[0] for row in cur.fetchall()]

        # Add any missing columns
        for column in required_columns:
            if column not in existing_columns:
                logger.info(f"Adding missing '{column}' column to documents table")
                cur.execute(f"""
                    ALTER TABLE documents 
                    ADD COLUMN {column} TEXT
                """)
                logger.info(f"Added '{column}' column successfully")

        conn.commit()
        cur.close()
        logger.info("Database initialized successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error initializing database: {error}")
        raise
    finally:
        if conn is not None:
            conn.close()

def save_document(variables):
    """
    Save document data to the database.

    Args:
        variables (dict): Dictionary containing document variables

    Returns:
        int: ID of the inserted record, or None if an error occurred
    """
    conn = None
    document_id = None
    try:
        # Get the database URL
        db_url = get_database_url()

        # Log connection attempt
        logger.info(f"Attempting to connect to database for document save operation")

        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Insert document data
        query = sql.SQL("""
            INSERT INTO documents (entreprise, poste, source, identifiant, base_line, salaire, description, skills_text, skill1, skill2, skill3, skill4, skill5, skill6, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """)

        # Log the document data being saved (without sensitive information)
        logger.info(f"Saving document for company: {variables.get('entreprise', '')}, position: {variables.get('poste', '')}")

        # Prepare values for insertion
        values = (
            variables.get('entreprise', ''),
            variables.get('poste', ''),
            variables.get('source', ''),
            variables.get('identifiant', ''),
            variables.get('base_line', ''),
            variables.get('salaire', ''),
            variables.get('description', ''),
            variables.get('skills_text', ''),
            variables.get('skill1', ''),
            variables.get('skill2', ''),
            variables.get('skill3', ''),
            variables.get('skill4', ''),
            variables.get('skill5', ''),
            variables.get('skill6', ''),
            variables.get('url', '')
        )

        # Log the query execution
        logger.info(f"Executing INSERT query with values: {values}")

        cur.execute(query, values)

        # Fetch the ID of the inserted record
        result = cur.fetchone()
        if result is None:
            logger.error("No ID returned after INSERT operation")
            conn.rollback()
            return None

        document_id = result[0]

        # Commit the transaction
        logger.info(f"Committing transaction for document ID: {document_id}")
        conn.commit()
        cur.close()

        logger.info(f"Document saved successfully with ID: {document_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error saving document: {error}")
        # Rollback the transaction if an error occurred
        if conn is not None:
            conn.rollback()
            logger.info("Transaction rolled back due to error")
        # Don't raise the exception here to maintain backward compatibility
        # Just return None to indicate failure
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection closed")

    return document_id

def get_document(document_id):
    """
    Retrieve document data from the database.

    Args:
        document_id (int): ID of the document to retrieve

    Returns:
        dict: Document data as a dictionary, or None if not found
    """
    conn = None
    document = None
    try:
        # Get the database URL
        db_url = get_database_url()

        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        query = sql.SQL("""
            SELECT id, entreprise, poste, source, identifiant, base_line, salaire, description, skills_text, skill1, skill2, skill3, skill4, skill5, skill6, url, created_at
            FROM documents
            WHERE id = %s
        """)

        logger.info(f"Retrieving document with ID: {document_id}")

        cur.execute(query, (document_id,))
        row = cur.fetchone()

        if row:
            document = {
                'id': row[0],
                'entreprise': row[1],
                'poste': row[2],
                'source': row[3],
                'identifiant': row[4],
                'base_line': row[5],
                'salaire': row[6],
                'description': row[7],
                'skills_text': row[8],
                'skill1': row[9],
                'skill2': row[10],
                'skill3': row[11],
                'skill4': row[12],
                'skill5': row[13],
                'skill6': row[14],
                'url': row[15],
                'created_at': row[16]
            }
            logger.info(f"Document retrieved successfully: {document['entreprise']}, {document['poste']}")
        else:
            logger.info(f"No document found with ID: {document_id}")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error retrieving document: {error}")
    finally:
        if conn is not None:
            conn.close()

    return document

def get_all_documents():
    """
    Retrieve all documents from the database.

    Returns:
        list: List of dictionaries containing document data
    """
    conn = None
    documents = []
    try:
        # Get the database URL
        db_url = get_database_url()

        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        query = sql.SQL("""
            SELECT id, entreprise, poste, source, identifiant, base_line, salaire, description, skills_text, skill1, skill2, skill3, skill4, skill5, skill6, url, created_at
            FROM documents
            ORDER BY created_at DESC
        """)

        logger.info("Retrieving all documents")

        cur.execute(query)
        rows = cur.fetchall()

        for row in rows:
            document = {
                'id': row[0],
                'entreprise': row[1],
                'poste': row[2],
                'source': row[3],
                'identifiant': row[4],
                'base_line': row[5],
                'salaire': row[6],
                'description': row[7],
                'skills_text': row[8],
                'skill1': row[9],
                'skill2': row[10],
                'skill3': row[11],
                'skill4': row[12],
                'skill5': row[13],
                'skill6': row[14],
                'url': row[15],
                'created_at': row[16]
            }
            documents.append(document)

        logger.info(f"Retrieved {len(documents)} documents successfully")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error retrieving documents: {error}")
    finally:
        if conn is not None:
            conn.close()

    return documents
