import sqlite3

def print_tables_and_columns(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables and Columns in the Database:")
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get the columns for the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for column in columns:
            column_name = column[1]
            print(f"  Column: {column_name}")
    
    # Close the connection
    conn.close()

# Example usage:
db_path = 'test.db'  # Replace with the path to your .db file
print_tables_and_columns(db_path)
