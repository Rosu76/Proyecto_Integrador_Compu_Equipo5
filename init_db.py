import sqlite3

def init_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            proveedor TEXT NOT NULL,
            precio REAL NOT NULL,
            costo REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factura INTEGER NOT NULL,
            nombre_articulo TEXT NOT NULL,
            valor_articulo REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            subtotal REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Base de datos inicializada correctamente.")