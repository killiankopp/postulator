from googleapiclient.discovery import build
from auth import get_credentials

def replace_variables(document_id, replacements):
    """
    Replace variables in a Google Doc with provided values.
    
    Args:
        document_id (str): The ID of the Google Doc
        replacements (dict): Dictionary of variables and their replacement values
        
    Returns:
        None
    """
    creds = get_credentials()
    docs_service = build('docs', 'v1', credentials=creds)

    requests = []
    for key, value in replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': f'{{{{ {key} }}}}',
                    'matchCase': True,
                },
                'replaceText': value,
            }
        })

    docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()