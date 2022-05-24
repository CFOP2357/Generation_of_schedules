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

def schedule_generator_prioritize_compact(schedule_manager, s):
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

def schedule_generator_prioritize_equitable(schedule_manager, s):
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
        
def schedule_generator_improved(schedule_manager, s):
    schedule_manager.bind_data()
    total = schedule_manager.get_students_count()
    count = 0 # contador para llevar avanzar el progress bar
    id_report = 0
    for student in schedule_manager.students:

        # logica de Progress bar no importante para el algoritmo
        progress = 95 * count / total
        s.progreso.set(progress)
        count += 1
        s.root.update_idletasks()
        # ------------------------------------------------------ #
         
        count2 = 0 # contador auxiliar para mejora de algoritmo
        while count2 != 2: # while para pasar dos veces sobre las materias del alumno 
            # una es para inscribir todas las materias con mayor a 2 dias a la semana
            # la segunda pasada es para inscribir las materias con menos a 3 dias a la semana 
            # (laboratorios y seminarios) regularmente. 

            for subject in student.major.subjects.values(): # por cada alumno hacer
                if subject.get_days_per_week() > 2: # si la materia se da mas de dos veces al dia 
                    if count2 == 0: # si es la primera pasada 

                        ## Obtener grupos con prioridad de horario compacto, si no encuentra se va a obtener el 
                        ## grupo con mas espacios (prioridad equitativa en segunda opcion)
                        group = subject.get_earliest_compatible_group(student)
                        group = subject.get_compatible_group_with_more_space(student)\
                            if group is None else group
                        ## ---------------------------------------------------------------- ##

                        ## Si encuentra un grupo entonces lo inscribe, si no levanta un reporte de error en la materia
                        ## e indicando el alumno con el cual ocurrio la incidencia
                        if group:
                            student.suscribe_subject_group(group)
                        else:
                            id_report += 1
                            comment = "No se encontró un grupo disponible de esta materia"
                            report = Report(id_report, subject.id_subject, student.id_student, comment)
                            schedule_manager.insert_report(report)
                        ## ------------------------------------------------------------------- ##

                elif count2 == 1: ## si no significa que el grupo es menor a 2 materias y solo pasa si es la segunda pasada (count2 == 1)
                    
                    ## misma logica de obtencion de grupo e inscripcion de materia
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
                    ## ------------------------------------------------------------- ##
            count2 += 1 ## avanza contador (cuando llegue a 2 osea la tercera pasada el while se rompe)

            
    return schedule_manager



    