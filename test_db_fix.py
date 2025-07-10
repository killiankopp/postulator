import logging
from db_service import init_db, get_all_documents

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize the database (this should add the base_line column if it doesn't exist)
        logger.info("Initializing database...")
        init_db()
        
        # Try to retrieve all documents (this was failing before with the column error)
        logger.info("Retrieving all documents...")
        documents = get_all_documents()
        
        # Print the number of documents retrieved
        logger.info(f"Successfully retrieved {len(documents)} documents")
        
        # Print the first document if any exist
        if documents:
            logger.info(f"First document: {documents[0]}")
        
        logger.info("Test completed successfully!")
    except Exception as e:
        logger.error(f"Test failed with error: {e}")

if __name__ == "__main__":
    main()