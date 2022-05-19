import schedule_manager as s_m

def schedule_generator(schedule_manager, s):
    schedule_manager.bind_data()
    total = len(schedule_manager.students)
    contador = 0
    for student in schedule_manager.students:
        progreso = 95*contador/total
        s.progreso.set(progreso)
        contador += 1
        s.root.update_idletasks()
        for subject in student.major.subjects.values():
            group = subject.get_earliest_compatible_group(student)
            group = subject.get_compatible_group_with_more_space(student)\
                if group is None else group
            if group:
                student.suscribe_subject_group(group)
    
    return schedule_manager
        
        



    