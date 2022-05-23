from calendar import calendar
from email import generator
from schedule_manager import *

# El metodo schedule_generator recibe 2 parametros:
# 1. schedule_manger: es una instancia de la clase ScheduleManager la cual ya 
# contiene los archivos cargados para que sea posible realizar el proceso de generar 
# los horarios.
# 2. s: es una instancia de user_interface permite acceder a la barra de progreso
# y mostrarle al usuario como va el algoritmo con base en la creacion de horarios

# 1er metodo.- bind_data(): liga todos los grupos a cada materia, cada materia a calendar
# carrera y cada carrera a cada alumno, es un metodo que le pertenece a la clase ScheduleManager
# y utiliza los datos previamente cargados.

# 2do metodo.- get_students_count(): Obtiene la cantidad de alumnos cargados al programa

# 3er metodo.- set(progress): recibe como parametro un entero del avance que se quiere mostrar en
# pantalla del progreso que se tiene al crear un horario.

# 4to metodo.- update_idletasts(): este metodo permite refrescar la pantalla que se muestra al usuario   
# y asi actualizar la barra de progreso

# 5to metodo.- get_earliest_compatible_group(student): Recibe como parametro un objeto de tipo Student
# el cual le sirve para buscar un grupo entre su materia, este grupo debe de cumplir con que sea el mas
# cercano a la siguiente hora disponible.
# Regresa un objeto de tipo Group 

# 6to metodo.- get_compatible_group_with_more_space(student): Recibe como parametro un objeto de tipo Student
# el cual le sirve para buscar un grupo entre su materia, este grupo debe de cumplir con que sea el que tiene 
# mas cupo y sea posible de inscribir al estudiante evaluado.
# Regresa un objeto de tipo Group 

# 7mo metodo.- suscribe_subject_group(group): recibe como parametro un objeto tipo Group , procesa las horas
# y las inscribe en el horario del alumno, se usa como mapa de horas inscritas una matriz de unos y ceros

def schedule_generator(schedule_manager, s):
    schedule_manager.bind_data()
    total = schedule_manager.get_students_count()
    count = 0
    id_report = 0
    for student in schedule_manager.students:
        progress = 95 * count / total
        s.progreso.set(progress)
        count += 1
        s.root.update_idletasks()
        for subject in student.major.subjects.values():
            group = subject.get_earliest_compatible_group(student)
            group = subject.get_compatible_group_with_more_space(student)\
                if group is None else group
            if group:
                student.suscribe_subject_group(group)
            else:
                id_report += 1
                comment = "No se encontró un grupo disponible de esta materia"
                report = Report(id_report, subject.id_subject, student.id_student, comment)
                schedule_manager.insert_report(report)
    
    return schedule_manager

def schedule_generator_2(schedule_manager, s):
    schedule_manager.bind_data()
    total = schedule_manager.get_students_count()
    count = 0
    id_report = 0
    for student in schedule_manager.students:
        progress = 95 * count / total
        s.progreso.set(progress)
        count += 1
        s.root.update_idletasks()
        for subject in student.major.subjects.values():
            group = subject.get_compatible_group_with_more_space(student)
            group = subject.get_earliest_compatible_group(student)\
                if group is None else group
            if group:
                student.suscribe_subject_group(group)
            else:
                id_report += 1
                comment = "No se encontró un grupo disponible de esta materia"
                report = Report(id_report, subject.id_subject, student.id_student, comment)
                schedule_manager.insert_report(report)
    
    return schedule_manager
        
def schedule_generator_3(schedule_manager, s):
    schedule_manager.bind_data()
    total = schedule_manager.get_students_count()
    count = 0
    id_report = 0
    for student in schedule_manager.students:
        progress = 95 * count / total
        s.progreso.set(progress)
        count += 1
        s.root.update_idletasks()
        count = 0
        while count != 2:
            for subject in student.major.subjects.values():
                if subject.get_days_per_week() > 2:
                    if count == 0:
                        group = subject.get_earliest_compatible_group(student)
                        group = subject.get_compatible_group_with_more_space(student)\
                            if group is None else group
                        if group:
                            student.suscribe_subject_group(group)
                        else:
                            id_report += 1
                            comment = "No se encontró un grupo disponible de esta materia"
                            report = Report(id_report, subject.id_subject, student.id_student, comment)
                            schedule_manager.insert_report(report)
                elif count == 1:
                    group = subject.get_earliest_compatible_group(student)
                    group = subject.get_compatible_group_with_more_space(student)\
                        if group is None else group
                    if group:
                        student.suscribe_subject_group(group)
                    else:
                        id_report += 1
                        comment = "No se encontró un grupo disponible de esta materia"
                        report = Report(id_report, subject.id_subject, student.id_student, comment)
                        schedule_manager.insert_report(report)
            count += 1


            
    
    return schedule_manager



    