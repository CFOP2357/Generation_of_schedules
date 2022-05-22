from hashlib import new
from dataclasses import asdict
import numbers
# from os import major
from sys import flags
from tokenize import group

# from matplotlib.pyplot import get
# from matplotlib.style import available
from numpy import full
from sqlalchemy import false, true
from datetime import datetime
import numpy as np

"""
    Notas

    Falta agregar los slots del horario de estudiante 
"""

class Group:
    def __init__(self, id_subject, id_group, teacher, available_spaces,  
                monday_start, monday_end, tuesday_start, tuesday_end, 
                wednesday_start, wednesday_end, thursday_start, thursday_end, 
                friday_start, friday_end, saturday_start, saturday_end):

        self.id_subject = id_subject
        self.id_group = id_group
        self.teacher = teacher
        self.available_spaces = available_spaces
        self.monday_start = monday_start
        self.monday_end = monday_end
        self.tuesday_start = tuesday_start
        self.tuesday_end = tuesday_end
        self.wednesday_start = wednesday_start
        self.wednesday_end = wednesday_end
        self.thursday_start = thursday_start
        self.thursday_end = thursday_end
        self.friday_start = friday_start
        self.friday_end = friday_end
        self.saturday_start = saturday_start
        self.saturday_end = saturday_end


    def is_not_full(self):
        if(self.available_spaces > 0):
            return true
        else:
            return false

    def unsuscribe_student(self):
        self.available_spaces += 1
    
    def suscribe_student(self):
        self.available_spaces -= 1





class Subject:
    def __init__(self, id_subject, id_major, name):
        #Id for each instance
        self.id_subject = id_subject
        #Id for the major it belongs to
        self.id_majors = [id_major,]
        #Name of the subject
        self.name = name
        #The groups collection will be made with a dictionary
        self.groups = {}


    #This function will return all the groups for the subject
    def get_all_groups(self):
        return self.groups

    #This function will return a specific group given an id     ########################  Not necesary ####################
    def get_group(self, id_group):
        return self.groups[self.id_subject + id_group]

    #This function will return all the groups that have at least 1 space available
    def get_not_full_grups(self):
        not_full_groups = []

        for group in self.groups.values():
            if(group.is_not_full()):
                not_full_groups.append(group)
        
        return not_full_groups


    def get_compatible_group_with_more_space(self,student):
        more_space_group = list(self.groups.values())[0]
        for group in self.groups.values():
            if(group.available_spaces > more_space_group.available_spaces and not student.is_group_compatible(group)):
                more_space_group = group

        return more_space_group

    

    def get_earliest_compatible_group(self,student):
        earliest_group = None
        earliest_hour = 30
        for group in self.groups.values():
            if group.available_spaces > 0 and self.get_group_earliest_hour(group) < earliest_hour and student.is_group_compatible(group):
                earliest_hour = self.get_group_earliest_hour(group)
                earliest_group = group

        return earliest_group

    def get_group_earliest_hour(self, group):
        earliest_hour = 500

        if(group.monday_start != 0):
            earliest_hour = group.monday_start
        if(group.tuesday_start != 0 and group.tuesday_start < earliest_hour):
            earliest_hour = group.tuesday_start

        if(group.wednesday_start != 0 and group.wednesday_start < earliest_hour):
            earliest_hour = group.wednesday_start

        if(group.thursday_start != 0 and group.thursday_start < earliest_hour):
            earliest_hour = group.thursday_start

        if(group.friday_start != 0 and group.friday_start < earliest_hour):
            earliest_hour = group.friday_start
                       
        if(group.saturday_start != 0 and group.saturday_start < earliest_hour):
            earliest_hour = group.saturday_start

        return earliest_hour
        

    #this funtion is used at the moment of binding data
    def insert_group(self, new_group):
        self.groups[new_group.id_group] = new_group

    def add_major(self,id_major):
        self.id_majors.append(id_major)





class Major:
    def __init__(self, id_major, name):
        self.id_major = id_major
        self.name = name
        self.subjects = {}

    #####################################################
    #########          Access methods        ############
    #####################################################
    def count_subjects(self):
        return len(self.subjects)
    

    def get_subjects(self):
        return self.subjects

    #####################################################
    #########      Modification methods      ############
    #####################################################
    def insert_subject(self, new_subject):
        self.subjects[new_subject.id_subject] = new_subject

    
    



class Student:
    def __init__(self, id_student, id_major):
        self.id_student = id_student
        self.id_major = id_major
        self.major = None
        #The schedule is a dictionary of groups, the key will be the id of the subject
        self.suscribed_groups = {}
        self.schedule = np.zeros((14, 6))

    #####################################################
    #########          Access methods        ############
    #####################################################
    def get_enrolled_subjects(self):
        return self.suscribed_groups

    def get_major_subjects(self):
        major_subjects = self.major.get_subjects()
        return major_subjects

    #This function checks if the student is busy given the slots of hours of any group
    def is_group_compatible(self,group):
        flag = False
        #If the student is not busy all days then its true that he es not busy
        if  (self.is_slot_compatible(group.monday_start,group.monday_end, 0)
        and self.is_slot_compatible(group.tuesday_start,group.tuesday_end, 1)
        and self.is_slot_compatible(group.wednesday_start,group.wednesday_end, 2)
        and self.is_slot_compatible(group.thursday_start,group.thursday_end, 3)
        and self.is_slot_compatible(group.friday_start,group.friday_end, 4)
        and self.is_slot_compatible(group.saturday_start,group.saturday_end, 5)):
            flag = True

        return flag

    #This functions checks if the student is busy given a group range of hours and a specific day
    def is_slot_compatible(self, startTime,endTime,day_index):
        flag = True
        #If the student is busy at some hour between the range of hours for the group
        for i in range(startTime-7, endTime-7):
            if(self.schedule[i,day_index] == 1):
                flag = False
                break

        return flag
    
    #####################################################
    #########      Modification methods      ############
    #####################################################
    def suscribe_subject_group(self, group):
        self.suscribed_groups[group.id_subject] = group
        group.suscribe_student()
        self.fill_schedule(group, True)


    def unsuscribe_subject_group(self, id_subject):
        self.suscribed_groups[id_subject].unsuscribe_student()
        self.suscribed_groups.pop(id_subject)
        group.unsuscribe_student()
        self.fill_schedule(group, False)


    def fill_schedule(self, group,suscribe_bool):
        if(suscribe_bool):
            number = 1
        else:
            number = 0

        if(group.monday_start != 0):
            self.fill_day(number,group.monday_start,group.monday_end,0)
        if(group.tuesday_start != 0):
            self.fill_day(number,group.tuesday_start,group.tuesday_end,1)
        if(group.wednesday_start != 0):
            self.fill_day(number,group.wednesday_start,group.wednesday_end,2)
        if(group.thursday_start != 0):
            self.fill_day(number,group.thursday_start,group.thursday_end,3)
        if(group.friday_start != 0):
            self.fill_day(number,group.friday_start,group.friday_end,4)
        if(group.saturday_start != 0):
            self.fill_day(number,group.saturday_start,group.saturday_end,5)


    def fill_day(self, number, startTime, endTime,day_index):
        for i in range(startTime-7, endTime-7):
            self.schedule[i,day_index]=number
    

    def insert_major(self, major):
        self.major = major


class Report:
    def __init__(self, id_report, id_subject, id_student, comment):
        self.id_report = id_report
        self.id_subject = id_subject
        self.id_student = id_student
        self.comment = comment
        date = datetime.now()
        self.date = str(date.strftime("%m-%d-%Y"))
        self.time = str(date.strftime("%H:%M:%S"))

    def get_string(self):
        report_text = str(self.id_report) + ',' + str(self.id_subject) + ',' + str(self.id_student)\
            + str(self.date) + ',' + str(self.time) + ',' + str(self.comment) 
        return report_text



class ScheduleManager:
    def __init__(self):
        self.students = []
        self.majors = {}
        self.subjects = {}
        self.groups = []
        self.reports = []


    def insert_student(self, new_student):
        self.students.append(new_student) 

    def insert_major(self, new_major):
        self.majors[new_major.id_major] = new_major

    def insert_subject(self, new_subject):
        if(self.exist_subject(new_subject.id_subject)):
            self.subjects[new_subject.id_subject].add_major(new_subject.id_majors[0])
        else:
            self.subjects[new_subject.id_subject] = new_subject

    def insert_group(self, new_group):
        self.groups.append(new_group)
    
    def insert_report(self, new_report):
        self.reports.append(new_report)
    

    def bind_data(self):
        #Binding all groups with their corresponding subject
        for group in self.groups:
            self.subjects[group.id_subject].insert_group(group)

        #Binding all subjects with their corresponding major
        for subject in self.subjects.values():
            for id_major in subject.id_majors:
                self.majors[id_major].insert_subject(subject)

        #Binding all students with their major
        for student in self.students:
            student.major = self.majors[student.id_major]

        #def get_students_ids(self):
    
    def get_students(self):
        return self.students
    
    def get_students_count(self):
        count = len(self.students)
        return count
    
    def exist_subject(self,id_subject):
        return id_subject in self.subjects
    #def get_subjects_ids(self):

    def get_group(self, id_subject, id_group):
        group = self.subjects[id_subject].get_group(id_group)
        return group
    
    def get_not_full_groups(self, id_subject):
        groups = self.subjects[id_subject].get_not_full_groups()
        return groups

    #def get_not_full_groups_ordered(self,id_subject):
    #    groups = self.get_not_full_groups()

    
    #def get_list():
    #def delete_subject():
    #def insert_subject():


    

