from beaupy import prompt, select
from beaupy.spinners import DOTS, Spinner
from rich.console import Console
from src.api import APIClient
import format_data
import os
from dotenv import load_dotenv

load_dotenv()
console = Console()
client = None  # Variable global para almacenar el cliente de la API  

def login():
    """Solicita las credenciales al usuario y devuelve un APIClient autenticado."""

    email = None
    password = None
    
    if (str(os.getenv("DEBUG_MODE")) == "1" ):
        email = os.getenv("MAIL")
        password = os.getenv("PASSWORD")
    else:
        email = prompt("Ingresa tu email")
        password = prompt("Ingresa tu contraseña", secure=True)

    spinner = Spinner(DOTS, "Iniciando sesión...")
    spinner.start()
    try:
        global client
        client = APIClient(email, password)
    except Exception as e:
        console.print(f"[red]Error al iniciar sesión[/red]")
        exit(1)
    finally:
        spinner.stop()

def get_favorite_subjects():
    """Obtiene las materias favoritas del estudiante."""
    spinner = Spinner(DOTS, "Obteniendo materias...")
    spinner.start()
    try:
        subjects = client.fetch_favorite_subjects()
    except Exception as e:
        console.print(f"[red]Error al obtener las materias[/red]")
        exit(1)
    finally:
        spinner.stop()
        return subjects

def show_resume_favorite_subjects():
    """Obtiene y muestra un resumen de las materias ravoritas del estudiante."""
    subjects = get_favorite_subjects()
    table = format_data.format_favorite_subjects(subjects)
    console.print(table)
    console.input("Presiona Enter para continuar...")

def show_homework_data(subject_id, subject_name):
    """Obtiene y muestra los detalles de una materia específica."""

    spinner = Spinner(DOTS, "Obteniendo detalles de la materia...")
    spinner.start()
    try:
        homework = client.fetch_homework_data(subject_id)
    except Exception as e:
        console.print(f"[red]Error al obtener los detalles de la materia[/red]")
        console.input("Presiona Enter para salir...")
        exit(1)
    finally:
        spinner.stop()
        table = format_data.format_homework_data(homework, subject_name)
        console.print(table)
        console.input("Presiona Enter para continuar...")

def show_assistance_data(subject_id, subject_name):
    """Obtiene y muestra los detalles de asistencia de una materia específica."""

    spinner = Spinner(DOTS, "Obteniendo detalles de asistencia...")
    spinner.start()
    try:
        assistance = client.fetch_assistance_data(subject_id)
    except Exception as e:
        console.print(f"[red]Error al obtener los detalles de asistencia[/red]")
        console.input("Presiona Enter para salir...")
        exit(1)
    finally:
        spinner.stop()
        table = format_data.format_assistance_data(assistance, subject_name)
        console.print(table)
        console.input("Presiona Enter para continuar...")

def show_homework_menu():
    """Muestra un menú para seleccionar una materia y ver sus detalles de tareas."""
    subjects = favorite_subjects
    emogi = r"¯\_(ツ)_/¯"
    subjects_names = [f"Mostrar resumen de todas las materias{emogi}"]
    subjects_ids = [0]
    for subject in subjects:
        subjects_names.append(subject.get("materia", "N/A"))
        subjects_ids.append(subject.get("id", "N/A"))

    console.print("[green]Selecciona una opcion:[/green]")
    selected_subject = select(subjects_names, cursor="🢧", cursor_style="cyan")

    selected_index = subjects_names.index(selected_subject)
    selected_subject_id = subjects_ids[selected_index]

    console.clear()
    if selected_subject_id == 0:
        show_resume_favorite_subjects()
    else:
        selected_option = detail_selector_menu()
   
        if selected_option == "Ver detalles de tareas":
            show_homework_data(selected_subject_id, selected_subject)
        elif selected_option == "Ver detalles de asistencia":
            show_assistance_data(selected_subject_id, selected_subject)

def detail_selector_menu():
    """Muestra un menú para seleccionar entre ver detalles de tareas o asistencia."""
    options = ["Ver detalles de tareas", "Ver detalles de asistencia"]
    console.print("[green]Selecciona una opcion:[/green]")
    selected_option = select(options, cursor="🢧", cursor_style="cyan")
    return selected_option

# Variable global para almacenar las materias favoritas
# quiero cachearla para el menu principal asi no tengo
# que hacer la llamada a la api cada vez que quiero 
# mostrar el menu
favorite_subjects = None
                          
def menu():
    """Muestra el menú principal de la aplicación."""
    console.clear()
    login()

    global favorite_subjects
    favorite_subjects = get_favorite_subjects()
    
    while True:
        console.clear()
        show_homework_menu()

menu()