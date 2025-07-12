import streamlit as st
import os
import pandas as pd
import logging
from document_service import replace_variables, create_document_copy, delete_document
from pdf_service import export_as_pdf
from config import DOCUMENT_ID, OUTPUT_FILENAME, COVER_LETTER_DOCUMENT_ID, COVER_LETTER_OUTPUT_FILENAME
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
    base_line = st.text_input("Base Line", value="Expert IA - pipelines ML - Data - DevOps - cybersecurity")
    source = st.text_input("Source")
    identifiant = st.text_input("Identifiant")
    salaire = st.text_input("Salaire")
    description = st.text_area("Description")

    # Submit button
    if st.button("Générer les documents"):
        if entreprise and poste:  # Basic validation
            with st.spinner("Génération des documents en cours..."):
                # Create variables dictionary with all fields
                variables = {
                    "entreprise": entreprise,
                    "poste": poste,
                    "base_line": base_line,
                    "source": source,
                    "identifiant": identifiant,
                    "salaire": salaire,
                    "description": description
                }

                try:
                    # Process CV document
                    logger.info("Processing CV document")
                    # Store the original template ID for reference
                    cv_template_id = DOCUMENT_ID

                    # Create a copy of the template document
                    cv_copy_id = create_document_copy(cv_template_id)

                    # Ensure copy_id is different from template_id
                    if cv_copy_id == cv_template_id:
                        raise ValueError("CV Copy ID is the same as template ID")

                    # Replace variables in the copy, not the template
                    # Pass template_id to ensure we're not modifying the original template
                    replace_variables(cv_copy_id, variables, template_id=cv_template_id)

                    # Export the copy as PDF
                    export_as_pdf(cv_copy_id, OUTPUT_FILENAME)

                    # Delete the copy as it's no longer needed
                    delete_document(cv_copy_id)

                    # Process Cover Letter document
                    logger.info("Processing Cover Letter document")
                    # Store the original template ID for reference
                    cover_letter_template_id = COVER_LETTER_DOCUMENT_ID

                    # Create a copy of the template document
                    cover_letter_copy_id = create_document_copy(cover_letter_template_id)

                    # Ensure copy_id is different from template_id
                    if cover_letter_copy_id == cover_letter_template_id:
                        raise ValueError("Cover Letter Copy ID is the same as template ID")

                    # Replace variables in the copy, not the template
                    # Pass template_id to ensure we're not modifying the original template
                    replace_variables(cover_letter_copy_id, variables, template_id=cover_letter_template_id)

                    # Export the copy as PDF
                    export_as_pdf(cover_letter_copy_id, COVER_LETTER_OUTPUT_FILENAME)

                    # Delete the copy as it's no longer needed
                    delete_document(cover_letter_copy_id)

                    # Save document data to the database
                    try:
                        logger.info("Attempting to save document to database")
                        document_id = save_document(variables)
                        if document_id:
                            logger.info(f"Document saved to database with ID: {document_id}")
                            st.success(f"Documents générés avec succès et enregistrés dans la base de données (ID: {document_id})!")
                        else:
                            logger.warning("Failed to save document to database - save_document returned None")
                            st.warning("Documents générés avec succès, mais non enregistrés dans la base de données. Vérifiez la connexion à la base de données.")
                    except Exception as db_error:
                        logger.error(f"Error saving document to database: {db_error}")
                        st.warning(f"Documents générés avec succès, mais erreur lors de l'enregistrement en base de données: {db_error}")

                    # Provide download links
                    col1, col2 = st.columns(2)

                    with col1:
                        if os.path.exists(OUTPUT_FILENAME):
                            with open(OUTPUT_FILENAME, "rb") as file:
                                btn = st.download_button(
                                    label="Télécharger le CV",
                                    data=file,
                                    file_name=OUTPUT_FILENAME,
                                    mime="application/pdf"
                                )

                    with col2:
                        if os.path.exists(COVER_LETTER_OUTPUT_FILENAME):
                            with open(COVER_LETTER_OUTPUT_FILENAME, "rb") as file:
                                btn = st.download_button(
                                    label="Télécharger la Lettre de Motivation",
                                    data=file,
                                    file_name=COVER_LETTER_OUTPUT_FILENAME,
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
            # Create a DataFrame with company, position, base line, and salary columns
            df = pd.DataFrame([(doc['entreprise'], doc['poste'], doc.get('base_line', ''), doc.get('salaire', '')) for doc in documents], 
                            columns=['Entreprise', 'Poste', 'Base Line', 'Salaire'])

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
