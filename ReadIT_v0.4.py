import tkinter as tk
from tkinter import messagebox
import winsound
import datetime

# Lista de usuarios y contraseñas preguardadas
USUARIOS = {
    "User1": "0000",
    "User2": "0000",
    "User3": "0000",
    "User4": "0000",
    "User5": "0000",
    "user6": "0000",
    "User7": "0000"
}

usuario_actual = None  # Se almacenará el usuario logueado

# Función para registrar en el log
def registrar_log(mensaje):
    with open("log.log", "a") as log_file:
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{fecha_hora} - Usuario: {usuario_actual} - {mensaje}\n")

# Función para reproducir sonido (dos beeps en caso de error)
def reproducir_sonido(error=False):
    frecuencia = 1000  # Hz
    duracion = 300     # ms
    if error:
        winsound.Beep(frecuencia, duracion)
        winsound.Beep(frecuencia, duracion)
    else:
        winsound.Beep(frecuencia, duracion)

# Función para validar el usuario y contraseña
def validar_login(event=None):
    global usuario_actual
    usuario = usuario_var.get()
    password = password_entry.get()

    if usuario in USUARIOS and USUARIOS[usuario] == password:
        usuario_actual = usuario  # Guardar usuario actual
        login_window.destroy()  # Cerrar ventana de login
        iniciar_aplicacion()  # Iniciar la app principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        password_entry.delete(0, tk.END)
        password_entry.focus_set()  # Mantiene el foco en la contraseña

# Función para cerrar sesión y volver al login
def cerrar_sesion(root):
    global usuario_actual
    usuario_actual = None  # Resetear usuario actual
    root.destroy()  # Cerrar ventana principal
    mostrar_login()  # Volver a la pantalla de inicio de sesión

# Pantalla de inicio (Login)
def mostrar_login():
    global login_window
    login_window = tk.Tk()
    login_window.title("Inicio de Sesión")
    login_window.geometry("300x200")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Seleccione usuario:", font=("Arial", 12)).pack(pady=5)
    global usuario_var
    usuario_var = tk.StringVar()
    usuario_var.set("Claudio Pozza")  # Selección por defecto

    usuario_menu = tk.OptionMenu(login_window, usuario_var, *USUARIOS.keys())
    usuario_menu.pack(pady=5)

    tk.Label(login_window, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
    global password_entry
    password_entry = tk.Entry(login_window, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)
    password_entry.focus_set()  # Foco en el campo de contraseña

    tk.Button(login_window, text="Ingresar", font=("Arial", 12), command=validar_login).pack(pady=10)

    password_entry.bind("<Return>", validar_login)  # Enter inicia sesión

    login_window.mainloop()

# --- Aplicación principal ---
def iniciar_aplicacion():
    global lectura_anterior
    lectura_anterior = None

    root = tk.Tk()
    root.title("Pegado de Clisés")
    root.geometry("600x400")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    tk.Label(frame, text=f"Usuario: {usuario_actual}", font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(frame, text="Escanea el código de barras:", font=("Arial", 16)).pack(pady=5)

    entrada_codigo = tk.Entry(frame, font=("Arial", 16), width=40)
    entrada_codigo.pack(pady=5)
    entrada_codigo.focus_set()

    lectura_anterior_label = tk.Label(frame, text="Lectura anterior: Ninguna", font=("Arial", 16))
    lectura_anterior_label.pack(pady=5)

    def mostrar_aviso(color, mensaje):
        aviso = tk.Toplevel(root)
        aviso.title("Aviso")
        aviso.geometry("400x200+100+100")
        aviso.configure(bg=color)
        etiqueta = tk.Label(aviso, text=mensaje, font=("Arial", 20), bg=color, fg="white")
        etiqueta.pack(expand=True, fill="both")
        aviso.after(1500, aviso.destroy)

    def procesar_lectura(event=None):
        global lectura_anterior
        codigo_actual = entrada_codigo.get().strip()

        if codigo_actual:
            if lectura_anterior is not None:
                if codigo_actual == lectura_anterior:
                    mostrar_aviso("green", "Lectura igual a la anterior")
                    registrar_log(f"Lectura: {codigo_actual}")
                else:
                    reproducir_sonido(error=True)
                    mostrar_aviso("red", "¡CAMBIO DE ARTICULO!")
                    registrar_log(f"Cambio de lectura: {lectura_anterior} -> {codigo_actual}")
            else:
                registrar_log(f"Lectura: {codigo_actual}")

            lectura_anterior = codigo_actual
            lectura_anterior_label.config(text=f"Lectura anterior: {lectura_anterior}")

        entrada_codigo.delete(0, tk.END)

    entrada_codigo.bind("<Return>", procesar_lectura)

    try:
        logo_image = tk.PhotoImage(file="logo.png")
        logo_label = tk.Label(root, image=logo_image, bd=0)
        logo_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)
    except Exception as e:
        print("Error al cargar el logo:", e)

    # Botón para cerrar sesión y volver al login
    tk.Button(root, text="Cambiar Usuario", font=("Arial", 12), command=lambda: cerrar_sesion(root)).pack(pady=10)

    root.mainloop()

# Ejecutar pantalla de inicio de sesión
mostrar_login()
