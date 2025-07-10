"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Doc template ID - raise if not defined
if 'DOCUMENT_ID' in os.environ:
    DOCUMENT_ID = os.environ['DOCUMENT_ID']
else:
    raise ValueError("Environment variable 'DOCUMENT_ID' is not defined")

# Output PDF filename - raise if not defined
if 'OUTPUT_FILENAME' in os.environ:
    OUTPUT_FILENAME = os.environ['OUTPUT_FILENAME']
else:
    raise ValueError("Environment variable 'OUTPUT_FILENAME' is not defined")

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
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
