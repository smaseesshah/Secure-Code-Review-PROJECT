import sqlite3

DB_FILE = 'taskvault.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row 
    return conn

def search_tasks(search_term):
    """
    VULNERABLE FUNCTION: SQL INJECTION
    The search_term is concatenated directly into the query string.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Intentionally vulnerable query construction
    query = f"SELECT * FROM tasks WHERE title LIKE '%{search_term}%'"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            tasks.append({
                'id': row['id'],
                'title': row['title'],
                'owner': row['owner_username']
            })
        return tasks
    except Exception as e:
        print(f"SQL Error: {str(e)}")
        return []
    finally:
        conn.close()