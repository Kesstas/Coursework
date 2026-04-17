class Patient:
    def __init__(self, patient_id, name, age, is_critical = False):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age
        self.__is_critical = is_critical

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

class EmergencyPatient(Patient):
    def __init__(self, patient_id, name, age):
        super().__init__(patient_id, name, age, is_critical = True)
    
    def get_department(self):
        return "Intensive Care Unit"        


class ChildPatient(Patient):
    def __init__(self, patient_id, name, age, is_critical = False):
        super().__init__(patient_id, name, age, is_critical)
    
    def get_department(self):
        return "Pediatric care"

class AdultPatient(Patient):
    def __init__(self, patient_id, name, age, is_critical = False):
        super().__init__(patient_id, name, age, is_critical)
    
    def get_department(self):
        return "Continuing registration..."


#Testavimas

def create_patient(patient_id, name, age, is_critical = False):
    patient = Patient(patient_id, name, age)

    if is_critical:
        return EmergencyPatient(patient_id, name, age)
    if patient.is_child():
        return ChildPatient(patient_id, name, age)
    else:
        return AdultPatient(patient_id, name, age)
    
p1 = create_patient(1, "John", 10, False)
p2 = create_patient(2, "Peter", 30, True)
p3 = create_patient(3, "Anna", 25, False)

print(p1.get_department())
print(p2.get_department())
print(p3.get_department())