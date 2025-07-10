"""
Database service for storing and retrieving document data.
"""
import psycopg2
from psycopg2 import sql
from config import DATABASE_URL

def init_db():
    """
    Initialize the database by creating the necessary tables if they don't exist.
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Create documents table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                entreprise TEXT NOT NULL,
                poste TEXT NOT NULL,
                source TEXT,
                identifiant TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error initializing database: {error}")
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
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Insert document data
        query = sql.SQL("""
            INSERT INTO documents (entreprise, poste, source, identifiant, description)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """)
        
        cur.execute(query, (
            variables.get('entreprise', ''),
            variables.get('poste', ''),
            variables.get('source', ''),
            variables.get('identifiant', ''),
            variables.get('description', '')
        ))
        
        document_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error saving document: {error}")
    finally:
        if conn is not None:
            conn.close()
    
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
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        query = sql.SQL("""
            SELECT id, entreprise, poste, source, identifiant, description, created_at
            FROM documents
            WHERE id = %s
        """)
        
        cur.execute(query, (document_id,))
        row = cur.fetchone()
        
        if row:
            document = {
                'id': row[0],
                'entreprise': row[1],
                'poste': row[2],
                'source': row[3],
                'identifiant': row[4],
                'description': row[5],
                'created_at': row[6]
            }
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error retrieving document: {error}")
    finally:
        if conn is not None:
            conn.close()
    
    return document