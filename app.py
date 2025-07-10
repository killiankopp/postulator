import streamlit as st
import os
from document_service import replace_variables
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

            # Replace variables in the document
            replace_variables(DOCUMENT_ID, variables)

            # Export as PDF
            export_as_pdf(DOCUMENT_ID, OUTPUT_FILENAME)

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
    else:
        st.error("Veuillez remplir au moins les champs 'Entreprise' et 'Poste'.")
