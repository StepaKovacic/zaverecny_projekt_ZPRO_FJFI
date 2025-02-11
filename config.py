import os 

GLOBAL_LOCATION = os.path.split(os.path.abspath(__file__))[0] + "/tridni_knihy/"


GLOBAL_STUDENT_JSON_STRUCTURE = {"student_first_name":None, 
                                 "student_last_name":None, 
                                 "username":None, 
                                 "date_of_birth":None, 
                                 "class_name":None}

GLOBAL_JSON_STRUCTURE = {"class_name":None, 
                         "name_of_teacher":None, 
                         "students":{}, 
                         "marks":{}}

