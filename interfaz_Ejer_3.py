import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import urllib.request
import json
import os
import io
import base64

DB_NAME = "usuarios.db"

#  Crear la base de datos
def crear_base_datos():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ("admin", "1234"))
        conn.commit()
        conn.close()

#  Verificar login
def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        abrir_dashboard()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

#  Mostrar ventana de registro
def abrir_ventana_registro():
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registrar nuevo usuario")
    ventana_registro.geometry("300x200")
    ventana_registro.configure(bg="#1e1e1e")

    tk.Label(ventana_registro, text="Nuevo usuario:", fg="white", bg="#1e1e1e").pack(pady=(10,0))
    nuevo_usuario = tk.Entry(ventana_registro)
    nuevo_usuario.pack()

    tk.Label(ventana_registro, text="Nueva contraseña:", fg="white", bg="#1e1e1e").pack(pady=(10,0))
    nueva_contrasena = tk.Entry(ventana_registro, show="*")
    nueva_contrasena.pack()

    def registrar():
        usuario = nuevo_usuario.get()
        contrasena = nueva_contrasena.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor llena ambos campos.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username=?", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Este usuario ya existe.")
        else:
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (usuario, contrasena))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana_registro.destroy()
        conn.close()

    tk.Button(ventana_registro, text="Registrar", command=registrar, bg="#2196F3", fg="white").pack(pady=15)

#  Descargar imagen y convertir a formato que Tkinter pueda mostrar
def obtener_imagen_desde_url(url):
    try:
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image_data = base64.b64encode(raw_data)
        return tk.PhotoImage(data=image_data)
    except:
        return None

#  Cargar personajes y mostrar en ventana
def abrir_dashboard():
    ventana_dashboard = tk.Toplevel(ventana)
    ventana_dashboard.title("Rick and Morty Dashboard")
    ventana_dashboard.configure(bg="#1e1e1e")
    ventana_dashboard.geometry("600x400")

    tk.Label(ventana_dashboard, text="Personajes Populares", font=("Arial", 16, "bold"),
             fg="white", bg="#1e1e1e").pack(pady=10)

    contenedor = tk.Frame(ventana_dashboard, bg="#1e1e1e")
    contenedor.pack(fill="both", expand=True)

    canvas = tk.Canvas(contenedor, bg="#1e1e1e")
    scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    frame_personajes = tk.Frame(canvas, bg="#1e1e1e")

    frame_personajes.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_personajes, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    try:
        url = "https://rickandmortyapi.com/api/character"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        personajes = data["results"][:5]
        for p in personajes:
            frame = tk.Frame(frame_personajes, bg="#2e2e2e", pady=10, padx=10)
            frame.pack(pady=5, padx=10, fill="x")

            img = obtener_imagen_desde_url(p["image"])
            if img:
                label_img = tk.Label(frame, image=img, bg="#2e2e2e")
                label_img.image = img  # Necesario para que no lo borre el recolector
                label_img.pack(side="left", padx=10)

            texto = f"Nombre: {p['name']}\nEspecie: {p['species']}\nEstado: {p['status']}"
            tk.Label(frame, text=texto, font=("Arial", 12), justify="left", fg="white", bg="#2e2e2e").pack(side="left")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener personajes.\n{e}")

#  Interfaz principal
crear_base_datos()

ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("300x260")
ventana.configure(bg="#1e1e1e")

tk.Label(ventana, text="Usuario:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack(pady=(20,0))
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

tk.Label(ventana, text="Contraseña:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack(pady=(10,0))
entry_contrasena = tk.Entry(ventana, show="*")
entry_contrasena.pack()

tk.Button(ventana, text="Iniciar sesión", command=verificar_login,
          bg="#4CAF50", fg="white", width=20).pack(pady=15)

tk.Button(ventana, text="Registrarse", command=abrir_ventana_registro,
          bg="#FF9800", fg="white", width=20).pack()

ventana.mainloop()
