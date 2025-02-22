import streamlit as st
import pandas as pd

# Cache the loaded data so that it only downloads once per session.
@st.cache_data
def load_data():
    # Replace with your actual Google Drive file ID
    file_id = "coconut_complete-10-2024"
    # Construct the direct download URL for CSV
    url = f"https://drive.google.com/uc?id={coconut_complete-10-2024}&export=download"
    df = pd.read_csv(url)
    return df

# Load your database CSV from Google Drive
data_df = load_data()

st.title("Compound Search - PubChem Style")

# Search options: here we assume your CSV has columns "Name" and "SMILES"
search_type = st.radio("Search by", ["Name", "SMILES"])
search_value = st.text_input(f"Enter {search_type}")

if st.button("Search"):
    if search_value:
        search_value = search_value.strip()
        with st.spinner("Searching..."):
            if search_type == "SMILES":
                # Remove extra spaces from the input SMILES string
                search_value = search_value.replace(" ", "")
                filtered_data = data_df[data_df["SMILES"].apply(lambda x: x == search_value)]
            else:
                filtered_data = data_df[data_df["Name"].str.contains(search_value, case=False, na=False)]
            
            if not filtered_data.empty:
                st.success(f"Found {len(filtered_data)} compound(s).")
                st.dataframe(filtered_data)
            else:
                st.warning("No compounds found.")
    else:
        st.error("Please enter a search value.")

st.caption("Powered by Streamlit")
