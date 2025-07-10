import os
import json
import tempfile
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import config

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

def get_credentials():
    """
    Get or refresh Google API credentials.

    Credentials can be provided either via the CREDENTIALS_JSON environment variable
    or through a credentials.json file in the current directory.

    Returns:
        Credentials: Google API credentials
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        # Check if credentials are provided via environment variable
        if config.CREDENTIALS_JSON:
            # Create a temporary file with the credentials JSON content
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file.write(config.CREDENTIALS_JSON)
                temp_credentials_path = temp_file.name

            try:
                flow = InstalledAppFlow.from_client_secrets_file(temp_credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_credentials_path):
                    os.unlink(temp_credentials_path)
        else:
            # Fall back to credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
