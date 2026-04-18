class Patient:
    def __init__(self, patient_id, name, age, is_critical = False, visit_type= None, profile = None, specialty = None):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age
        self.__is_critical = is_critical
        self.__visit_type = visit_type
        self.__profile = profile
        self.__specialty = specialty

    @property
    def patient_id(self):
        return self.__patient_id
    
    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age < 0:
            raise ValueError("Age cannot be bellow zero")
        self.__age = age

    @property
    def is_critical(self):
        return self.__is_critical

    def is_child(self):
        return self.__age < 18

class CriticalPatient(Patient):
    def __init__(self, patient_id, name, age):
        super().__init__(patient_id, name, age, is_critical = True)
    
    def get_department(self):
        return "Intensive Care Unit"        


class ChildPatient(Patient):
    def __init__(self, patient_id, name, age):
        super().__init__(patient_id, name, age)
    
    def get_department(self):
        return "Pediatric care"


class AdultPatient(Patient):
    def __init__(self, patient_id, name, age, visit_type = None, profile = None, specialty = None):
        super().__init__(patient_id, name, age, visit_type = visit_type, profile = profile, specialty = specialty)
    
    def get_department(self):
        return "Continuing registration..."


class UrgentPatient(AdultPatient):
    def __init__(self, patient_id, name, age):
        super().__init__(patient_id, name, age, visit_type = "Urgent")
    
    def get_department(self):
        return "Emergency Room"     

class PlannedPatient(AdultPatient):
    def __init__(self, patient_id, name, age, profile = None, specialty = None):      
        super().__init__(patient_id, name, age, visit_type = "Planned", profile = profile, specialty = specialty)
    
    def get_department(self):
        return "Continue registration..."     


class TherapyPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty):
        super().__init__(patient_id, name, age, profile = "Therapy", specialty = specialty)
        self.__specialty = specialty

    @property
    def specialty(self):
        return self.__specialty

    def get_department(self):
        return f"Therapy Department - {self.__specialty}"


class SurgeryPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty):
        super().__init__(patient_id, name, age, profile = "Surgery", specialty = specialty)
        self.__specialty = specialty

    @property
    def specialty(self):
        return self.__specialty

    def get_department(self):
        return f"Surgery Department - {self.__specialty}"


class DiagnosticsPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty):
        super().__init__(patient_id, name, age, profile = "Diagnostics", specialty = specialty)
        self.__specialty = specialty

    @property
    def specialty(self):
        return self.__specialty

    def get_department(self):
        return f"Diagnostic Department - {self.__specialty}"






#Testavimas

def create_patient(patient_id, name, age, is_critical = False, visit_type= None, profile = None, specialty = None):
    patient = Patient(patient_id, name, age)

    if is_critical:
        return CriticalPatient(patient_id, name, age)
    elif patient.is_child():
        return ChildPatient(patient_id, name, age)
    elif visit_type == "Urgent":
        return UrgentPatient(patient_id, name, age)
    elif profile == "Therapy":
        return TherapyPatient(patient_id, name, age, specialty)
    elif profile == "Surgery":
        return SurgeryPatient(patient_id, name, age, specialty)    
    elif profile == "Diagnostics":
        return DiagnosticsPatient(patient_id, name, age, specialty)    
    else:
        raise ValueError("Invalid profile. Choose: Therapy, Surgery or Diagnostics")
    
p1 = create_patient(1, "John", 10, False)
p2 = create_patient(2, "Peter", 30, True)
p3 = create_patient(3, "Anna", 25, False, profile="Therapy", specialty="Cardiology")

print(p1.get_department())
print(p2.get_department())
print(p3.get_department())