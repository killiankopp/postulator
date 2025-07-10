import streamlit as st
import os
import pandas as pd
import logging
from document_service import replace_variables, create_document_copy, delete_document
from pdf_service import export_as_pdf
from config import DOCUMENT_ID, OUTPUT_FILENAME
from db_service import init_db, save_document, get_all_documents

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    st.error(f"Erreur de connexion à la base de données: {e}")
    st.warning("L'application fonctionnera sans enregistrement en base de données.")

st.title("Postulator")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Postuler", "Candidatures"])

# Tab 1: Document generation form
with tab1:
    # Input fields
    entreprise = st.text_input("Entreprise")
    poste = st.text_input("Poste")
    source = st.text_input("Source")
    identifiant = st.text_input("Identifiant")
    description = st.text_area("Description")

    # Submit button
    if st.button("Générer les documents"):
        if entreprise and poste:  # Basic validation
            with st.spinner("Génération des documents en cours..."):
                # Create variables dictionary with all fields
                variables = {
                    "entreprise": entreprise,
                    "poste": poste,
                    "source": source,
                    "identifiant": identifiant,
                    "description": description
                }

                try:
                    # Store the original template ID for reference
                    template_id = DOCUMENT_ID

                    # Create a copy of the template document
                    copy_id = create_document_copy(template_id)

                    # Ensure copy_id is different from template_id
                    if copy_id == template_id:
                        raise ValueError("Copy ID is the same as template ID")

                    # Replace variables in the copy, not the template
                    # Pass template_id to ensure we're not modifying the original template
                    replace_variables(copy_id, variables, template_id=template_id)

                    # Export the copy as PDF
                    export_as_pdf(copy_id, OUTPUT_FILENAME)

                    # Delete the copy as it's no longer needed
                    delete_document(copy_id)

                    # Save document data to the database
                    try:
                        document_id = save_document(variables)
                        if document_id:
                            logger.info(f"Document saved to database with ID: {document_id}")
                            st.success(f"Document généré avec succès et enregistré dans la base de données (ID: {document_id})!")
                        else:
                            logger.warning("Failed to save document to database")
                            st.warning("Document généré avec succès, mais non enregistré dans la base de données.")
                    except Exception as db_error:
                        logger.error(f"Error saving document to database: {db_error}")
                        st.warning(f"Document généré avec succès, mais erreur lors de l'enregistrement en base de données: {db_error}")

                    # Provide download link
                    if os.path.exists(OUTPUT_FILENAME):
                        with open(OUTPUT_FILENAME, "rb") as file:
                            btn = st.download_button(
                                label="Télécharger le PDF",
                                data=file,
                                file_name=OUTPUT_FILENAME,
                                mime="application/pdf"
                            )
                except Exception as e:
                    st.error(f"Une erreur est survenue: {str(e)}")
        else:
            st.error("Veuillez remplir au moins les champs 'Entreprise' et 'Poste'.")

# Tab 2: View records
with tab2:
    try:
        # Get all documents from the database
        logger.info("Retrieving all documents for display")
        documents = get_all_documents()

        if documents:
            # Create a DataFrame with just the company and position columns
            df = pd.DataFrame([(doc['entreprise'], doc['poste']) for doc in documents], 
                            columns=['Entreprise', 'Poste'])

            # Display the DataFrame as a table
            st.dataframe(df, use_container_width=True)
            logger.info(f"Displayed {len(documents)} documents")
        else:
            st.info("Aucun enregistrement trouvé dans la base de données.")
            logger.info("No documents found in database")
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        st.error(f"Erreur lors de la récupération des enregistrements: {e}")
        st.warning("Impossible d'afficher les candidatures enregistrées.")
