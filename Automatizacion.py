import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess
from getpass import getpass

class RaspberryControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Raspberry")

        # Variables para almacenar el horario de encendido y apagado
        self.encendido_var = tk.StringVar()
        self.apagado_var = tk.StringVar()

        # Inicializar la interfaz gráfica
        self.setup_gui()

    def setup_gui(self):
        # Etiqueta y entrada para el horario de encendido
        ttk.Label(self.root, text="Horario de Encendido:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.encendido_var).grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta y entrada para el horario de apagado
        ttk.Label(self.root, text="Horario de Apagado:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(self.root, textvariable=self.apagado_var).grid(row=1, column=1, padx=10, pady=10)

        # Botón para activar/desactivar
        ttk.Button(self.root, text="Activar", command=self.toggle_raspberry).grid(row=2, column=0, columnspan=2, pady=20)

    def toggle_raspberry(self):
        # Obtener el horario de encendido y apagado
        encendido_time = self.encendido_var.get()
        apagado_time = self.apagado_var.get()

        # Validar el formato del horario
        try:
            datetime.strptime(encendido_time, '%H:%M')
            datetime.strptime(apagado_time, '%H:%M')
        except ValueError:
            self.show_error("Formato de hora incorrecto (HH:MM)")
            return

        # Configurar las tareas programadas usando crontab con sudo
        crontab_command_encendido = f"{encendido_time} /usr/bin/python3 {__file__} encendido"
        crontab_command_apagado = f"{apagado_time} /usr/bin/python3 {__file__} apagado"

        self.execute_with_sudo(["crontab", "-l"])
        self.execute_with_sudo(["echo", f"{crontab_command_encendido}", "|", "crontab", "-"])
        self.execute_with_sudo(["echo", f"{crontab_command_apagado}", "|", "crontab", "-"])

        self.show_message("Tareas programadas correctamente")

    def execute_with_sudo(self, command):
        sudo_password = getpass("Ingrese la contraseña de superusuario: ")
        command = ["sudo", "-S"] + command
        subprocess.run(command, input=sudo_password.encode(), text=True, check=True)

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def show_message(self, message):
        tk.messagebox.showinfo("Mensaje", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = RaspberryControlApp(root)
    root.mainloop()

