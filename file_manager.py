from sched import scheduler
import pandas as pd
import classes as cl
from datetime import datetime

def read_error_filter(path, name):
    df = pd.read_csv(path)
    alert_id = 9
    shape = df.shape

    if (name == 'estudiantes'):
        alert_id = 1 \
            if shape[1]==2 and df.columns.values[0] == 'cve_unica' \
                and df.columns.values[1] == 'id_carrera' else 2
    elif(name == 'grupos'):
        alert_id = 3 \
            if shape[1]==16 and df.columns.values[0] == 'id_materia' and df.columns.values[1] == 'grupo' \
                and df.columns.values[2] == 'maestro' and df.columns.values[3] == 'cupo' else 4# falta validar todas las columnas
    elif(name == 'carreras'):
        alert_id = 5 \
            if shape[1]==2 and df.columns.values[0] == 'id_carrera' and df.columns.values[1] == 'nombre' else 6
    elif(name == 'materias'):
        alert_id = 7 if shape[1]==3 and df.columns.values[0] == 'id_materia' \
            and df.columns.values[1] == 'id_carrera' and df.columns.values[2] == 'nombre' else 8

    return kind_of_alert(alert_id), df

def kind_of_alert(id):
    alert_txt = ''
    if id == 1:
        alert_txt = 'El archivo de los estudiantes fue cargado correctamente'
    elif  id == 2:
        alert_txt = 'El archivo  debe tener dos columnas con encabecados: cve_unica, id_carrera'
    elif  id == 3:
        alert_txt = 'El archivo de los grupos fue cargado correctamente'
    elif  id == 4:
        alert_txt = 'El archivo debe tener 16 columnas con encabecados: id_materia, grupo, maestro, cupo y los campos de los dias'
    elif  id == 5:
        alert_txt = 'El archivo de las carreras fue cargado correctamente'
    elif  id == 6:
        alert_txt = 'El archivo  debe tener dos columnas con encabecados: id_carrera, nombre'
    elif  id == 7:
        alert_txt = 'El archivo de las materias fue cargado correctamente'
    elif  id == 8:
        alert_txt = 'El archivo  debe tener tres columnas con encabecados: id_materia, id_carrera, nombre'
    
    return alert_txt

def instant_classes(s):
    
    schedule_manager = cl.ScheduleManager()

    for i in s.df_groups.index:
        group = cl.Group(
            s.df_groups["id_materia"][i],
            s.df_groups["grupo"][i],
            s.df_groups["maestro"][i],
            s.df_groups["cupo"][i],
            s.df_groups["lunes_inicio"][i],
            s.df_groups["lunes_final"][i],
            s.df_groups["martes_inicio"][i],
            s.df_groups["martes_final"][i],
            s.df_groups["miercoles_inicio"][i],
            s.df_groups["miercoles_final"][i],
            s.df_groups["jueves_inicio"][i],
            s.df_groups["jueves_final"][i],
            s.df_groups["viernes_inicio"][i],
            s.df_groups["viernes_final"][i],
            s.df_groups["sabado_inicio"][i],
            s.df_groups["sabado_final"][i],
        )
        schedule_manager.insert_group(group)

    for i in s.df_subjects.index:
        subject = cl.Subject(
            s.df_subjects["id_materia"][i],
            s.df_subjects["id_carrera"][i],
            s.df_subjects["nombre"][i]
        )
        schedule_manager.insert_subject(subject)

    for i in s.df_majors.index: 
        major = cl.Major(
            s.df_majors["id_carrera"][i],
            s.df_majors["nombre"][i]
            )
        schedule_manager.insert_major(major)

    for i in s.df_students.index:
        student = cl.Student(
            s.df_students["cve_unica"][i],
            s.df_students["id_carrera"][i]
            )
        schedule_manager.insert_student(student)

    return schedule_manager


def class_to_excel(schedules, path):
    date = datetime.now()
    file = path + "/horariosUaslp-" + str(date.strftime("%m-%d-%Y-%H-%M-%S")) +  ".csv"
    csv = open(file,"w")
    csv.write("cve_alumno,cve_materia,grupo\n")
    for student in schedules:
        for group in student.suscribed_groups.values():
            schedule = str(student.id_student) + "," + str(group.id_subject) + "," + str(group.id_group) + "\n"
            csv.write(schedule)

def reports_list_to_excel(reports, path):
    date = datetime.now()
    file = path + "/ReportesHorarios-" + str(date.strftime("%m-%d-%Y-%H-%M-%S")) +  ".csv"
    csv = open(file,"w")
    csv.write("id_reporte,id_materia,id_usuario,fecha,hora,comentario\n")
    for report in reports:
        csv.write(report.get_string() + "\n")




