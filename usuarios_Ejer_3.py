import sqlite3

def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    
    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT,
            password TEXT
        )
    ''')

    # Insertar un usuario de prueba
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ("admin", "1234"))

    conn.commit()
    conn.close()

crear_base_datos()
print("Base de datos creada con usuario: admin / 1234")
