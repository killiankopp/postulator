# Postulator - Document Generator

A tool for generating customized documents from Google Docs templates.

## Project Structure

The project has been refactored to follow the Single Responsibility Principle (SRP):

- **app.py**: Streamlit user interface for the application
- **auth.py**: Handles Google API authentication
- **document_service.py**: Manages document manipulation (replacing variables)
- **pdf_service.py**: Handles PDF export functionality
- **db_service.py**: Manages database operations for storing document data
- **config.py**: Stores configuration values
- **test_modules.py**: Tests the functionality of the modules

## Usage

### Configuration

The application can be configured using environment variables or a `.env` file:

- `DOCUMENT_ID`: Google Doc template ID (required)
- `OUTPUT_FILENAME`: Output PDF filename (defaults to "CV_Killian_KOPP.pdf")
- `CREDENTIALS_JSON`: Google API credentials JSON content (required)
- `DB_HOST`: Database host (defaults to "localhost")
- `DB_PORT`: Database port (defaults to "5432")
- `DB_NAME`: Database name (defaults to "postulator")
- `DB_USER`: Database user (defaults to "postgres")
- `DB_PASSWORD`: Database password (defaults to "")

You can set these variables directly in your environment or create a `.env` file in the project root directory. The application will automatically load variables from the `.env` file if it exists.

Example:
```bash
export DOCUMENT_ID="your-google-doc-id"
export OUTPUT_FILENAME="your-output-filename.pdf"
export CREDENTIALS_JSON='{"installed":{"client_id":"your-client-id","project_id":"your-project-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"your-client-secret","redirect_uris":["http://localhost"]}}'
export DB_HOST="your-database-host"
export DB_PORT="5432"
export DB_NAME="your-database-name"
export DB_USER="your-database-user"
export DB_PASSWORD="your-database-password"
```

### Docker Compose

The easiest way to run the application is using Docker Compose:

1. Make sure you have Docker and Docker Compose installed on your system
2. Set the required environment variables or create a `.env` file with:
   ```
   # Required variables
   DOCUMENT_ID=your-google-doc-id
   OUTPUT_FILENAME=your-output-filename.pdf

   # Database configuration (optional, defaults are set in docker-compose.yml)
   DB_HOST=postulator-db
   DB_PORT=5432
   DB_NAME=postulator
   DB_USER=postgres
   DB_PASSWORD=postulator_password

   # Google API credentials - required
   # Paste your credentials JSON content here
   CREDENTIALS_JSON={"installed":{"client_id":"your-client-id","project_id":"your-project-id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"your-client-secret","redirect_uris":["http://localhost"]}}
   ```
   You can copy the `.env.example` file to `.env` and modify it with your values.
4. Run the application:
   ```bash
   docker-compose up -d
   ```
5. Access the application at http://localhost:8501
6. To stop the application:
   ```bash
   docker-compose down
   ```

Generated PDF files will be saved in the `output` directory.

### Streamlit Interface (Local Development)

For local development, run the Streamlit application:

```bash
source .venv/bin/activate
streamlit run app.py
```

This will open a web interface where you can:
1. Enter company, position, source, identifier, and description information
2. Click "Générer le document" to create the document
3. The document data is stored in the database
4. Download the generated PDF


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
- PostgreSQL database
- psycopg2-binary (Python PostgreSQL adapter)

See `requirements.txt` for specific version requirements.
