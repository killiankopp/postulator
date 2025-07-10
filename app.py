import streamlit as st
import os
from document_service import replace_variables, create_document_copy, delete_document
from pdf_service import export_as_pdf
from config import DOCUMENT_ID, OUTPUT_FILENAME

st.title("Générateur de Document")

# Input fields
entreprise = st.text_input("Entreprise")
poste = st.text_input("Poste")
source = st.text_input("Source")
identifiant = st.text_input("Identifiant")
description = st.text_area("Description")

# Submit button
if st.button("Générer le document"):
    if entreprise and poste:  # Basic validation
        with st.spinner("Génération du document en cours..."):
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

                st.success("Document généré avec succès!")

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
