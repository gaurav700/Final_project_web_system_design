import sqlite3

def initialize_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL UNIQUE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        timestamp INTEGER NOT NULL,
        notes TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (item_id) REFERENCES items (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
