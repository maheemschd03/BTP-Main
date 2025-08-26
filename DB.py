import psycopg2
from typing import Union

def run_query(query: str) -> str:
    """
    Executes a given SQL query using a PostgreSQL connection.
    Handles all SQL queries (including JOINs) and returns detailed results as a string.

    Parameters:
        query (str): The SQL query to be executed.

    Returns:
        str: Detailed results or error message.
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="HumanDB",
            user="postgres",
            password="Mysql=124",
            port="5432"
        )
        cur = conn.cursor()

        # Normalize query
        query_clean = query.strip().lower()

        # Handle MySQL-style "SHOW TABLES"
        if query_clean == "show tables":
            cur.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
            rows = cur.fetchall()
            if rows:
                result_str = "Tables in the database:\n"
                for idx, row in enumerate(rows, start=1):
                    result_str += f"{idx}. {row[0]}\n"
            else:
                result_str = "No tables found in the database."

        # Handle MySQL-style "DESC table_name"
        elif query_clean.startswith("desc "):
            table_name = query_clean.split("desc", 1)[1].strip()
            cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s;
            """, (table_name,))
            rows = cur.fetchall()
            if rows:
                result_str = f"Description of table '{table_name}':\n"
                result_str += f"{'Column':<20} {'Type':<15} {'Nullable':<10}\n"
                result_str += "-" * 45 + "\n"
                for col, dtype, nullable in rows:
                    result_str += f"{col:<20} {dtype:<15} {nullable:<10}\n"
            else:
                result_str = f"Table '{table_name}' not found."

        # Handle SELECT queries (including JOINs!)
        elif query_clean.startswith("select"):
            cur.execute(query)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]

            if rows:
                # Calculate column widths for pretty alignment
                col_widths = [max(len(str(col)), 12) for col in colnames]
                for row in rows:
                    for idx, item in enumerate(row):
                        col_widths[idx] = max(col_widths[idx], len(str(item)))

                # Header
                result_str = " | ".join(f"{col:<{col_widths[idx]}}" for idx, col in enumerate(colnames)) + "\n"
                result_str += "-" * (sum(col_widths) + 3 * (len(colnames) - 1)) + "\n"

                # Rows
                for row in rows:
                    row_str = " | ".join(f"{str(item):<{col_widths[idx]}}" for idx, item in enumerate(row))
                    result_str += row_str + "\n"
            else:
                result_str = "Query executed successfully, but no results found."

        # Handle other queries (INSERT, UPDATE, DELETE, CREATE, DROP, etc.)
        else:
            cur.execute(query)
            conn.commit()
            result_str = "Query executed successfully."

        # Cleanup
        cur.close()
        conn.close()
        return result_str

    except Exception as e:
        return f"Error: {str(e)}"





