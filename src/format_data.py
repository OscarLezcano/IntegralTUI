from datetime import datetime

from rich.table import Table

def format_favorite_subjects(subjects):
    table = Table(title="Materias Favoritas")
    table.add_column("Nombre", justify="left")
    table.add_column("Asistencia", justify="center")
    table.add_column("PP", justify="center")
    for subject in subjects:
        table.add_row(
            subject.get("materia", "N/A"),
            str(subject.get("porcentajeAsistencia", "N/A")),
            str(subject.get("porcentajePP", "N/A")),
        )
    return table

def format_homework_data(homework_data, subject_name):
    table = Table(title=f"Tareas de la Materia: [yellow]{subject_name}[/yellow]")
    table.add_column("Nombre")
    table.add_column("Tipo", justify="center")
    table.add_column("Puntaje Obtenido", justify="center")
    table.add_column("Puntaje Total", justify="center")
    table.add_column("Peso (%)", justify="center")
    for detail in homework_data.get("items", []):
        table.add_row(
                str(detail.get("tarea", "N/A")),
                str((detail.get("tipoTarea")).get("label", "N/A")),
                str(detail.get("puntajeObtenido", "N/A")),
                str(detail.get("puntajeTotal", "N/A")),
                str(detail.get("porcentajePesoMateria", "N/A"))
        )
    return table

# Auxiliary functions ---------------------------------------------------------------------------------

def _format_date(date_str):
    if not date_str:
        return "N/A"
    return datetime.fromisoformat(date_str).strftime("%d/%m/%Y")

def _is_present(present):
    return present is True or present == "Sí"

def format_assistance_data(assistance_data, subject_name):
    table = Table(title=f"Asistencias de la Materia: [yellow]{subject_name}[/yellow]")
    table.add_column("Fecha", justify="center")
    table.add_column("Presente", justify="center")

    student_assists = {
        item["assistanceId"]: item["present"]
        for item in assistance_data["studentAssists"]
    }

    assistances = [
        {"date": assist["date"], "present": student_assists.get(assist["id"])}
        for assist in assistance_data["assists"]
    ][::-1]

    total_assistances = len(assistances)
    present_count = sum(1 for assist in assistances if _is_present(assist["present"]))
    absent_count = total_assistances - present_count

    for assist in assistances:
        present = _is_present(assist["present"])
        label = "Sí" if present else "No"
        color = "green" if present else "red"
        table.add_row(
            _format_date(assist["date"]),
            f"[{color}]{label}[/{color}]",
        )

    table.add_section()
    table.add_row("Total de Asistencias", str(total_assistances))
    table.add_row("Cantidad de Presentes", f"[green]{present_count}[/green]")
    table.add_row("Cantidad de Ausentes", f"[red]{absent_count}[/red]")
    return table