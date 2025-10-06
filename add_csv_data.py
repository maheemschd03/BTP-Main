import pandas as pd
from sqlalchemy import create_engine

def upload_csv_to_postgres(csv_path, table_name, db_name="HumanDB", user="postgres", password="Mysql=124", host='localhost', port=5432, if_exists='replace'):
    """
    Uploads a CSV file to a PostgreSQL table.

    Parameters:
        csv_path (str): Path to the CSV file.
        table_name (str): Name of the target table in PostgreSQL.
        db_name (str): Name of the PostgreSQL database.
        user (str): PostgreSQL username.
        password (str): PostgreSQL password.
        host (str): Host of the PostgreSQL server (default: 'localhost').
        port (int): Port number (default: 5432).
        if_exists (str): What to do if the table exists ('fail', 'replace', 'append').

    Returns:
        str: Success message.
    """
    try:
        # 1. Read CSV file
        df = pd.read_csv(csv_path)
        print(f"✅ CSV '{csv_path}' read successfully with {len(df)} rows.")

        # 2. Create connection engine
        engine_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(engine_url)

        # 3. Upload DataFrame to PostgreSQL
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        return f"✅ Data uploaded successfully to table '{table_name}' in database '{db_name}'."

    except Exception as e:
        return f"❌ Error: {e}"
