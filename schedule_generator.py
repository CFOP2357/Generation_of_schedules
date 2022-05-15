import schedule_manager as s_m

def schedule_generator(schedule_manager):
    schedule_manager.bind_data()

    for student in schedule_manager.students:
        for subject in student.major.subjects:
            group = subject.get_earliest_compatible_group(student)
            group = subject.get_compatible_group_with_more_space(student)\
                if group is None else group
            if group:
                student.suscribe_subject_group(group)


    