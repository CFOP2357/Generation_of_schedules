import classes as cl

def schedule_generator(schedule_manager, s):
    schedule_manager.bind_data()
    total = len(schedule_manager.students)
    count = 0
    id_report = 0
    for student in schedule_manager.students:
        progress = 95*count/total
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
                report = cl.Report(id_report, subject.id_subject, student.id_student, comment)
                schedule_manager.insert_group(report)
    
    return schedule_manager
        
        



    