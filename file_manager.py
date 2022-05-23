from sched import scheduler
import pandas as pd
from datetime import datetime

from schedule_manager import *

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
                and df.columns.values[2] == 'maestro' and df.columns.values[3] == 'cupo' and df.columns.values[4] == 'lunes_inicio'\
                    and df.columns.values[5] == 'lunes_final' and df.columns.values[6] == 'martes_inicio' and df.columns.values[7] == 'martes_final'\
                        and df.columns.values[8] == 'miercoles_inicio' and df.columns.values[9] == 'miercoles_final' and df.columns.values[10] == 'jueves_inicio'\
                            and df.columns.values[11] == 'jueves_final' and df.columns.values[12] == 'viernes_inicio' and df.columns.values[13] == 'viernes_final'\
                                and df.columns.values[14] == 'sabado_inicio' and df.columns.values[15] == 'sabado_final' else 4
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
    
    schedule_manager = ScheduleManager()

    for i in s.df_groups.index:
        group = Group(
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
        subject = Subject(
            s.df_subjects["id_materia"][i],
            s.df_subjects["id_carrera"][i],
            s.df_subjects["nombre"][i]
        )
        schedule_manager.insert_subject(subject)

    for i in s.df_majors.index: 
        major = Major(
            s.df_majors["id_carrera"][i],
            s.df_majors["nombre"][i]
            )
        schedule_manager.insert_major(major)

    for i in s.df_students.index:
        student = Student(
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
    csv.write("id_reporte,id_materia,id_estudiante,fecha,hora,comentario\n")
    for report in reports:
        csv.write(report.get_string() + "\n")

def format_schedule_to_excel(student, path):
    date = datetime.now()
    file = path + "/Horario "+str(student.id_student)+" -" + str(date.strftime("%m-%d-%Y-%H-%M-%S")) +  ".csv"
    csv = open(file,"w")
    csv.write("Hora,lunes,martes,miercoles,jueves,viernes,sabado\n")

    for i in range(14):
        map_schedule = str(i+7)+" a "+ str(i+8) + ","
        for j in range(6):
            map_schedule += str(student.schedule[i,j]) + ","
        if map_schedule != "":
            map_schedule = map_schedule[:-1]
            map_schedule += "\n"
            csv.write(map_schedule)
        
def groups_to_excel(groups, path):
    date = datetime.now()
    file = path + "/Grupos-" + str(date.strftime("%m-%d-%Y-%H-%M-%S")) +  ".csv"
    csv = open(file,"w")
    csv.write("id_materia,grupo,cupo\n")
    for group in groups:
        csv.write(group.get_string())




   





