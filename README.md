# Postulator - Document Generator

A tool for generating customized documents from Google Docs templates.

## Project Structure

The project has been refactored to follow the Single Responsibility Principle (SRP):

- **app.py**: Streamlit user interface for the application
- **auth.py**: Handles Google API authentication
- **document_service.py**: Manages document manipulation (replacing variables)
- **pdf_service.py**: Handles PDF export functionality
- **config.py**: Stores configuration values
- **test_modules.py**: Tests the functionality of the modules

## Usage

### Configuration

The application can be configured using environment variables:

- `DOCUMENT_ID`: Google Doc template ID (defaults to '1xdg-OGy5NCIIA5OGnU8OHPb-E40X9MJsJw8KuQBX7Sg')
- `OUTPUT_FILENAME`: Output PDF filename (defaults to "CV_Killian_KOPP.pdf")
- `CREDENTIALS_JSON`: Google API credentials JSON content (defaults to reading from credentials.json file)

Example:
```bash
export DOCUMENT_ID="your-google-doc-id"
export OUTPUT_FILENAME="your-output-filename.pdf"
export CREDENTIALS_JSON='{"installed":{"client_id":"your-client-id","project_id":"your-project-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"your-client-secret","redirect_uris":["http://localhost"]}}'
```

### Streamlit Interface

Run the Streamlit application:

```bash
streamlit run app.py
```

This will open a web interface where you can:
1. Enter company, position, source, identifier, and description information
2. Click "Générer le document" to create the document
3. Download the generated PDF


## Development

### Testing

Run the test script to verify that the modules work correctly:

```bash
python test_modules.py
```

### Adding New Features

To add new features:
1. Identify which module should contain the feature based on its responsibility
2. Add the feature to the appropriate module
3. Update the UI in app.py if needed
4. Update the tests in test_modules.py

## Requirements

- Python 3.6+
- Streamlit
- Google API client libraries
