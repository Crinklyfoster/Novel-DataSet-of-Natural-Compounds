import streamlit as st
import pandas as pd

# Mock data for demonstration
mock_data = {
    "Name": ["Aspirin", "Caffeine", "Paracetamol", "Ibuprofen"],
    "SMILES": [
        "CC(=O)OC1=CC=CC=C1C(=O)O",
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "CC(=O)NC1=CC=C(O)C=C1",
        "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
        "CC(=O)OC1=CC=CC=C1C(=O)O",  # Aspirin
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # Caffeine
        "CC(=O)NC1=CC=C(O)C=C1",  # Paracetamol
        "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",  # Ibuprofen
    ],
    "Formula": ["C9H8O4", "C8H10N4O2", "C8H9NO2", "C13H18O2"],
    "Molecular Weight": [180.16, 194.19, 151.16, 206.29],
}

# Convert mock data to a DataFrame
mock_df = pd.DataFrame(mock_data)

# Streamlit app layout
st.title("Compound Search - PubChem Style")

# Search bar and options
search_type = st.radio("Search by", ["Name", "SMILES"])
search_value = st.text_input(f"Enter {search_type}")

# Button to trigger search
if st.button("Search"):
    if search_value:
        search_value = search_value.strip()  # Trim any leading/trailing whitespace
        with st.spinner("Searching..."):
            if search_type == "SMILES":
                # Clean the input SMILES string by removing unnecessary spaces
                search_value = search_value.replace(" ", "")
                # Filter mock data based on the SMILES search type
                filtered_data = mock_df[mock_df["SMILES"].str.contains(search_value, case=False, na=False)]
                # Check for exact SMILES match
                filtered_data = mock_df[mock_df["SMILES"].apply(lambda x: x == search_value)]
            else:
                # Filter mock data based on the Name search type
                filtered_data = mock_df[mock_df["Name"].str.contains(search_value, case=False, na=False)]

            if not filtered_data.empty:
                st.success(f"Found {len(filtered_data)} compound(s).")
                st.dataframe(filtered_data)
            else:
                st.warning("No compounds found.")
    else:
        st.error("Please enter a search value.")

# Additional styling and information
st.caption("Powered by Streamlit - Mock UI")
