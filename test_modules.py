"""
Test script to verify that the refactored modules work correctly.
"""
import os
from document_service import replace_variables
from pdf_service import export_as_pdf
from config import DOCUMENT_ID, OUTPUT_FILENAME

def test_document_generation():
    """
    Test the document generation process.
    """
    print("Testing document generation...")
    
    # Test variables
    test_variables = {
        "entreprise": "Test Company",
        "poste": "Test Position",
        "source": "Test Source",
        "identifiant": "Test ID",
        "description": "This is a test description."
    }
    
    # Replace variables in the document
    try:
        replace_variables(DOCUMENT_ID, test_variables)
        print("✓ Variable replacement successful")
    except Exception as e:
        print(f"✗ Variable replacement failed: {e}")
        return False
    
    # Export as PDF
    try:
        export_as_pdf(DOCUMENT_ID, "test_output.pdf")
        print("✓ PDF export successful")
    except Exception as e:
        print(f"✗ PDF export failed: {e}")
        return False
    
    # Check if the file exists
    if os.path.exists("test_output.pdf"):
        print(f"✓ Output file created: test_output.pdf")
        # Clean up
        os.remove("test_output.pdf")
        print("✓ Test cleanup completed")
        return True
    else:
        print("✗ Output file not created")
        return False

if __name__ == "__main__":
    if test_document_generation():
        print("All tests passed!")
    else:
        print("Tests failed!")