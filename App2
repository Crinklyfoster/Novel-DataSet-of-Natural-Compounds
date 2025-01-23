import streamlit as st
import pandas as pd

# Mock Data
mock_data = {
    "Name": ["Aspirin", "Caffeine", "Paracetamol", "Ibuprofen"],
    "SMILES": [
        "CC(=O)OC1=CC=CC=C1C(=O)O",
        "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "CC(=O)NC1=CC=C(O)C=C1",
        "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    ],
    "Formula": ["C9H8O4", "C8H10N4O2", "C8H9NO2", "C13H18O2"],
    "Molecular Weight": [180.16, 194.19, 151.16, 206.29],
}

mock_df = pd.DataFrame(mock_data)

# Sidebar
with st.sidebar:
    st.title("Compound Search - PubChem Inspired")
    st.info("Search for compounds by Name or SMILES. Results include molecular properties.")

# Main Page Layout
st.title("Compound Search")
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        margin: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tabs for search
tab1, tab2 = st.tabs(["Search by Name", "Search by SMILES"])

with tab1:
    st.subheader("Search by Name")
    name_query = st.text_input("Enter compound name (e.g., Aspirin):")
    if st.button("Search by Name"):
        name_query = name_query.strip()
        if name_query:
            results = mock_df[mock_df["Name"].str.contains(name_query, case=False, na=False)]
            if not results.empty:
                st.success(f"Found {len(results)} compound(s).")
                st.dataframe(results)
            else:
                st.warning("No compounds found.")
        else:
            st.error("Please enter a name.")

with tab2:
    st.subheader("Search by SMILES")
    smiles_query = st.text_input("Enter SMILES string (e.g., CC(=O)OC1=CC=CC=C1C(=O)O):")
    if st.button("Search by SMILES"):
        smiles_query = smiles_query.strip().replace(" ", "")
        if smiles_query:
            results = mock_df[mock_df["SMILES"].apply(lambda x: x == smiles_query)]
            if not results.empty:
                st.success(f"Found {len(results)} compound(s).")
                st.dataframe(results)
            else:
                st.warning("No compounds found.")
        else:
            st.error("Please enter a SMILES string.")

# Footer
st.markdown("---")
st.caption("Powered by Streamlit - Inspired by PubChem")

