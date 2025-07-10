"""
Configuration settings for the application.
"""
import os

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
