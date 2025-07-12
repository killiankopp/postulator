"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
# Use the directory of this file to find .env
from pathlib import Path
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)
# Log whether .env file was found
if env_path.exists():
    logger.info(f".env file found at {env_path}")
else:
    logger.warning(f".env file not found at {env_path}, using environment variables only")

# CV Google Doc template ID - raise if not defined
if 'DOCUMENT_ID' in os.environ:
    DOCUMENT_ID = os.environ['DOCUMENT_ID']
else:
    raise ValueError("Environment variable 'DOCUMENT_ID' is not defined")

# CV Output PDF filename - raise if not defined
if 'OUTPUT_FILENAME' in os.environ:
    OUTPUT_FILENAME = os.environ['OUTPUT_FILENAME']
else:
    raise ValueError("Environment variable 'OUTPUT_FILENAME' is not defined")

# Cover Letter Google Doc template ID - raise if not defined
if 'COVER_LETTER_DOCUMENT_ID' in os.environ:
    COVER_LETTER_DOCUMENT_ID = os.environ['COVER_LETTER_DOCUMENT_ID']
else:
    raise ValueError("Environment variable 'COVER_LETTER_DOCUMENT_ID' is not defined")

# Cover Letter Output PDF filename - raise if not defined
if 'COVER_LETTER_OUTPUT_FILENAME' in os.environ:
    COVER_LETTER_OUTPUT_FILENAME = os.environ['COVER_LETTER_OUTPUT_FILENAME']
else:
    raise ValueError("Environment variable 'COVER_LETTER_OUTPUT_FILENAME' is not defined")

# Google API credentials - raise if not defined
if 'CREDENTIALS_JSON' in os.environ:
    CREDENTIALS_JSON = os.environ['CREDENTIALS_JSON']
else:
    raise ValueError("Environment variable 'CREDENTIALS_JSON' is not defined")

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'postulator')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postulator_password')

# Log database configuration (without password)
logger.info(f"Database configuration: Host={DB_HOST}, Port={DB_PORT}, Name={DB_NAME}, User={DB_USER}")

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
