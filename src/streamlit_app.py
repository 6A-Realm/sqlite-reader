import streamlit as st
from sqlalchemy import text


def connect_to_db():
    # Connect to the SQLite database using an experimental feature.
    conn = st.experimental_connection(
        "local_db",
        type = "sql",
        url = "sqlite:///active.db"
    )
    return conn

def retrieve_table_names(conn):
    with conn.session as s:
        # Query to retrieve all table names in the file.
        sql = text("SELECT name FROM sqlite_master WHERE type='table';")
        result = s.execute(sql)
        table_names = [row[0] for row in result.fetchall()]
    return table_names

def display_table_editor(conn, table_name):
    # Query the table data from the database.
    df = conn.query(f"SELECT * FROM {table_name}", ttl = 3600)

    # Usage of expander so you aren't spammed with a bunch of tables.
    expander = st.expander(label = table_name, expanded = False)

    # Usage of data_editor so that tables can be edited.
    expander.dataframe(df, use_container_width = True)

def save_changes_to_db(uploaded_file):
    # Save the uploaded file content as "active.db".
    bytes_data = uploaded_file.getvalue()
    with open("active.db", "wb") as file:
        file.write(bytes_data)

def main():
    st.sidebar.title("SQLite Viewer")
    st.sidebar.write("Upload and view.")

    uploaded_file = st.sidebar.file_uploader("Upload your SQLite file:", accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Save the uploaded file content as "active.db" initially.
        save_changes_to_db(uploaded_file)

        # Connect to the database.
        conn = connect_to_db()

        # Retrieve all table names in the file.
        table_names = retrieve_table_names(conn)

        # Loop through each table and display it using an expander to avoid spamming with tables.
        for table_name in table_names:
            display_table_editor(conn, table_name)

if __name__ == "__main__":
    main()
