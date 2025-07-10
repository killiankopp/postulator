from googleapiclient.discovery import build
from auth import get_credentials

def export_as_pdf(document_id, output_filename):
    """
    Export a Google Doc as PDF.
    
    Args:
        document_id (str): The ID of the Google Doc
        output_filename (str): The name of the output PDF file
        
    Returns:
        None
    """
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    request = drive_service.files().export_media(fileId=document_id,
                                               mimeType='application/pdf')
    with open(output_filename, 'wb') as f:
        f.write(request.execute())