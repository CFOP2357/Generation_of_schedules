from sched import scheduler
import pandas as pd
import classes as cl

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

def instant_classes(df_students, df_groups, df_subjects, df_majors):
    
    schedule_manager = cl.ScheduleManager()

    for i in df_groups.index:
        group = cl.Group(
            df_groups["id_materia"][i],
            df_groups["grupo"][i],
            df_groups["maestro"][i],
            df_groups["cupo"][i],
            df_groups["lunes_inicio"][i],
            df_groups["lunes_final"][i],
            df_groups["martes_inicio"][i],
            df_groups["martes_final"][i],
            df_groups["miercoles_inicio"][i],
            df_groups["miercoles_final"][i],
            df_groups["jueves_inicio"][i],
            df_groups["jueves_final"][i],
            df_groups["viernes_inicio"][i],
            df_groups["viernes_final"][i],
            df_groups["sabado_inicio"][i],
            df_groups["sabado_final"][i],
        )
        schedule_manager.insert_group(group)

    for i in df_subjects.index:
        subject = cl.Subject(
            df_subjects["id_carrera"][i],
            df_subjects["id_materia"][i],
            df_subjects["nombre"][i]
        )
        schedule_manager.insert_subject(subject)

    for i in df_majors.index: 
        major = cl.Major(
            df_majors["id_carrera"][i],
            df_majors["nombre"][i]
            )
        schedule_manager.insert_major(major)

    for i in df_students.index:
        student = cl.Student(
            df_students["cve_unica"][i],
            df_students["id_carrera"][i]
            )
        schedule_manager.insert_student(student)

    return schedule_manager


    


