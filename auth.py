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
            # Validate JSON format before writing to file
            try:
                # Try to fix common JSON formatting issues
                credentials_json = config.CREDENTIALS_JSON

                # If the JSON string starts with a single quote, it might be a string representation
                # that needs to be evaluated
                if credentials_json.startswith("'") and credentials_json.endswith("'"):
                    credentials_json = credentials_json[1:-1]

                # Try different approaches to parse the JSON
                try:
                    # First try to parse as is
                    json_obj = json.loads(credentials_json)
                except json.JSONDecodeError:
                    try:
                        # If that fails, try to replace single quotes with double quotes
                        import re
                        # Replace single quotes that are likely to be for property names or string values
                        # This regex looks for patterns like 'property': or 'value'
                        fixed_json = re.sub(r"'([^']*)':", r'"\1":', credentials_json)
                        fixed_json = re.sub(r":'([^']*)'", r':"\1"', fixed_json)

                        # Now try to parse again
                        json_obj = json.loads(fixed_json)
                    except json.JSONDecodeError:
                        try:
                            # If that still fails, it might be a Python dictionary literal
                            # Try to safely evaluate it (this is risky but we're in a controlled environment)
                            import ast
                            # Only attempt this if it looks like a dictionary
                            if credentials_json.strip().startswith('{') and credentials_json.strip().endswith('}'):
                                # Use ast.literal_eval which is safer than eval()
                                dict_obj = ast.literal_eval(credentials_json)
                                # Convert the dictionary to a JSON string
                                json_obj = dict_obj
                            else:
                                # If it doesn't look like a dictionary, re-raise the original error
                                raise
                        except Exception:
                            # If all attempts fail, raise a more helpful error
                            raise json.JSONDecodeError(
                                "Could not parse CREDENTIALS_JSON. Ensure it's a valid JSON string with double quotes.",
                                credentials_json, 0
                            )

                # Convert back to a properly formatted JSON string
                valid_json = json.dumps(json_obj)

                # Create a temporary file with the validated credentials JSON content
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                    temp_file.write(valid_json)
                    temp_credentials_path = temp_file.name

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(temp_credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                finally:
                    # Clean up the temporary file
                    if os.path.exists(temp_credentials_path):
                        os.unlink(temp_credentials_path)
            except json.JSONDecodeError as e:
                # Provide a more detailed error message with debugging information
                error_msg = f"Invalid JSON in CREDENTIALS_JSON environment variable: {str(e)}"

                # Add debugging information about the JSON string
                # Only show a snippet to avoid exposing sensitive information
                if credentials_json:
                    # Show the first 50 characters with sensitive parts masked
                    snippet = credentials_json[:50] + "..." if len(credentials_json) > 50 else credentials_json
                    # Mask any potential client secrets or IDs
                    import re
                    snippet = re.sub(r'"client_secret":"[^"]*"', '"client_secret":"***"', snippet)
                    snippet = re.sub(r'"client_id":"[^"]*"', '"client_id":"***"', snippet)
                    error_msg += f"\nJSON snippet (masked): {snippet}"

                # Provide guidance on how to format the JSON correctly
                error_msg += "\nEnsure that the JSON is properly formatted with double quotes around property names and string values."
                error_msg += "\nExample format: {\"property\": \"value\"}"

                raise ValueError(error_msg)
        else:
            # Fall back to credentials.json file
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the token for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
