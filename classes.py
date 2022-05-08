from dataclasses import asdict
from os import major
from sys import flags
from tokenize import group

from matplotlib.pyplot import get
from matplotlib.style import available
from numpy import full
from sqlalchemy import false, true

import numpy as np

"""
    Notas

    Falta agregar los slots del horario de estudiante 
"""

class Group:
    def __init__(self, id_subject, group, teacher, available_spaces,  
                monday_start, monday_end, tuesday_start, tuesday_end, 
                wednesday_start, wednesday_end, thursday_start, thursday_end, 
                friday_start, friday_end, saturday_start, saturday_end):

        self.id_subject = id_subject
        self.group = group
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
        if(self.available_spaces>0):
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
        self.id_major = id_major
        #Name of the subject
        self.name = name
        #The groups collection will be made with a dictionary
        self.groups = {}
        
    #This function will return all the groups for the subject
    def get_all_groups(self):
        return self.groups

    #This function will return a specific group given an id
    def get_group(self, id_group):
        return self.groups[id_group]

    #This function will return all the groups that have at least 1 space available
    def get_not_full_grups(self):
        not_full_groups = []

        for group in self.groups.values():
            if(group.is_not_full()):
                not_full_groups.append(group)
        
        return not_full_groups

    #this funtion is used at the moment of binding data
    def insert_group(self, new_group):
        self.groups[new_group.group] = new_group


    def compatible_group_with_more_space(self,student):
        more_space_group = None

        for group in self.groups.values():
            if(group.available_spaces > more_space_group.available_spaces and not student.is_busy(group)):
                more_space_group = group

        return more_space_group

    def group_earliest_hour(group):
        earliest_hour = 500000

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

    def earliest_compatible_group(self,student):
        earliest_group = None
        earliest_hour = 30
        for group in self.groups.values():
            if group.available_space > 0 and self.group_earliest_hour(group)<earliest_hour and not student.is_busy(group):
                earliest_hour = self.group_earliest_hour(group)
                earliest_group = group

        return earliest_group

        


class Major:
    def __init__(self, id_major, name):
        self.id_major = id_major
        self.name = name
        self.subjects = {}

    def count_subjects(self):
        return len(self.subjects)
    
    def get_subjects(self):
        return self.subjects

    def insert_subject(self, new_subject):
        self.subjects[new_subject.id_subject] = new_subject

    
    



class Student:
    def __init__(self, id_student, id_major):
        self.id_student = id_student
        self.id_major = id_major
        self.major 
        #The schedule is a dictionary of groups, the key will be the id of the subject
        self.suscribed_groups = {}
        self.schedule = np.zeros((14,6))

        
    def enrolled_subjects(self):
        return self.suscribed_groups

    def get_major_subjects(self):
        major_subjects = self.major.get_subjects()
        return major_subjects

    def unsuscribe_subjects_group(self, id_subject):
        self.suscribed_groups[id_subject].unsuscribe_student()
        self.suscribed_groups.pop(id_subject)
        ################################################ void the schedule

    def is_slot_busy(self, startTime,endTime,day):
        flag = False
        #If the student is busy at some hour between the range of hours for the group
        for i in range(startTime-7,endTime-7):
            if(self.schedule[i,day]==1):
                flag=True
            break

        return flag

    #This function checks if the student is busy given the slots of hours of any group
    def is_busy(self,group):
        flag = True
        #If the student is not busy all days then its true that he es not busy
        if  (not self.is_slot_busy(group.monday_start,group.monday_end,0)
        and not self.is_slot_busy(group.tuesday_start,group.tuesday_end,1)
        and not self.is_slot_busy(group.wednesday_start,group.wednesday_end,2)
        and not self.is_slot_busy(group.thursday_start,group.thursday_end,3)
        and not self.is_slot_busy(group.friday_start,group.friday_end,4)
        and not self.is_slot_busy(group.saturday_start,group.saturday_end,5)):
            flag = False

        return flag

    
   


        

    #def suscribe_subjects_group(id_subject, id_group):
    def suscribe_subjects_group(self, group):
        self.suscribed_groups[group.id_subject] = group
    
    #def delete_shedule(id_subject, id_group):   

    def insert_major(self, major):
        self.major = major





class ScheduleManager:
    def __init__(self):
        self.students = []
        #self.students = {}
        #self.majors = []
        self.majors = {}
        #self.subjects = []
        self.subjects = {}
        self.groups = []

        #self.schedule =


        #def group_order_by_available_space():

    def bind_data(self):
        #Binding all groups with their corresponding subject
        for group in self.groups:
            self.subjects[group.id_subject].insert_group(group)
        
        #Binding all subjects with their corresponding major
        for subject in self.subjects.values():
            self.majors[subject.id_major].insert_subject(subject)

        #Binding all students with their major
        for student in self.students:
            student.major = self.majors[student.id_major]

    #def get_students_ids(self):
    
    def get_students(self):
        return self.students
    
    def get_students_count(self):
        count = len(self.students)
        return count
    
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


    

