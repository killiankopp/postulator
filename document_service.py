from googleapiclient.discovery import build
from auth import get_credentials
import time

def create_document_copy(document_id, copy_title=None):
    """
    Create a copy of a Google Doc.

    Args:
        document_id (str): The ID of the Google Doc to copy
        copy_title (str, optional): The title for the copy. If None, a timestamp will be added.

    Returns:
        str: The ID of the newly created copy
    """
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    # First, verify we can access the original document
    original_doc = docs_service.documents().get(documentId=document_id).execute()
    original_id = original_doc.get('documentId')

    if original_id != document_id:
        raise ValueError(f"Original document ID mismatch: expected {document_id}, got {original_id}")

    if copy_title is None:
        # Generate a title with timestamp if none provided
        timestamp = int(time.time())
        copy_title = f"Copy_{timestamp}"

    # Create a copy of the document
    copy_metadata = {
        'name': copy_title,
        'parents': []  # Copy to the same folder as the original
    }

    copied_file = drive_service.files().copy(
        fileId=document_id,
        body=copy_metadata
    ).execute()

    # Ensure we're using the ID of the copy, not the original
    copy_id = copied_file['id']

    # Verify the copy exists and is different from the original
    copy_doc = docs_service.documents().get(documentId=copy_id).execute()
    verified_copy_id = copy_doc.get('documentId')

    if verified_copy_id != copy_id:
        raise ValueError(f"Copy document ID mismatch: expected {copy_id}, got {verified_copy_id}")

    if verified_copy_id == original_id:
        raise ValueError(f"Copy has the same ID as the original: {verified_copy_id}")

    return copy_id

def delete_document(document_id):
    """
    Delete a Google Doc.

    Args:
        document_id (str): The ID of the Google Doc to delete

    Returns:
        None
    """
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    drive_service.files().delete(fileId=document_id).execute()

def replace_variables(document_id, replacements, template_id=None):
    """
    Replace variables in a Google Doc with provided values.

    Args:
        document_id (str): The ID of the Google Doc to modify
        replacements (dict): Dictionary of variables and their replacement values
        template_id (str, optional): The ID of the template document, to ensure we're not modifying it

    Returns:
        None
    """
    creds = get_credentials()
    docs_service = build('docs', 'v1', credentials=creds)

    # First, verify we can access the document with the provided ID
    doc = docs_service.documents().get(documentId=document_id).execute()

    # Ensure we're working with the correct document
    doc_id = doc.get('documentId')
    if doc_id != document_id:
        raise ValueError(f"Document ID mismatch: expected {document_id}, got {doc_id}")

    # If template_id is provided, ensure we're not modifying the template
    if template_id and doc_id == template_id:
        raise ValueError(f"Cannot modify template document: {template_id}")

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

    # Use the verified document ID for the batch update
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
