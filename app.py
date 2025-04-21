import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------------------------------------------------------
# Configuration / Connection
# -----------------------------------------------------------------------------
@st.cache_resource
def get_engine():
    """
    Create SQLAlchemy engine using DATABASE_URL env var
    e.g., postgresql+psycopg2://username:password@127.0.0.1:5432/Natural_Product_db
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        st.error("Please set the DATABASE_URL environment variable.")
        st.info("Example: set DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/Natural_Product_db")
        st.stop()
    return create_engine(db_url)

# -----------------------------------------------------------------------------
# Query Logic
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)
def query_database(search_type: str, search_value: str) -> pd.DataFrame:
    """
    Search 'public.natural_products' by MNPI_ID, Name, or canonical_smiles
    """
    engine = get_engine()

    column_map = {
        "MNPI_ID": "mnpi_id::text",
        "Name":    "name",
        "SMILES":  "canonical_smiles"
    }

    col = column_map[search_type]
    sql = text(f"""
        SELECT * FROM public.natural_products
        WHERE {col} ILIKE :val
        LIMIT 500
    """)
    params = {"val": f"%{search_value}%"}
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)
    return df

# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="MNPI Compound Search", layout="wide")
st.title("🔎 Natural Products Search (Local PostgreSQL + RDKit)")

search_type = st.radio("Search by", ["MNPI_ID", "Name", "SMILES"], horizontal=True)
search_value = st.text_input(f"Enter {search_type}", placeholder={
    "MNPI_ID": "e.g. 1001",
    "Name":    "e.g. Aspirin",
    "SMILES":  "e.g. CC(=O)OC1=CC=CC=C1C(=O)O"
}[search_type])

if st.button("Search"):
    if not search_value.strip():
        st.error("Please enter a value.")
    else:
        with st.spinner("Querying database..."):
            try:
                results = query_database(search_type, search_value.strip())
            except Exception as e:
                st.error(f"Error querying database:\n{e}")
            else:
                if results.empty:
                    st.warning("No results found.")
                else:
                    st.success(f"Found {len(results)} result(s).")
                    st.dataframe(results, use_container_width=True)

st.caption("🧪 Powered by Streamlit • PostgreSQL • RDKit")
