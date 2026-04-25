import csv

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

    @property
    def visit_type(self):
        return self.__visit_type
    
    @property
    def profile(self):
        return self.__profile
    
    @property
    def specialty(self):
        return self.__specialty

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
    def __init__(self, patient_id, name, age, specialty, doctor):
        super().__init__(patient_id, name, age, profile = "Therapy", specialty = specialty)
        self.__specialty = specialty
        self.__doctor = doctor

    @property
    def specialty(self):
        return self.__specialty
    
    @property
    def doctor(self):
        return self.__doctor

    def get_department(self):
        return f"Therapy Department - {self.__specialty}| Doctor: {self.__doctor.name}"


class SurgeryPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty, doctor):
        super().__init__(patient_id, name, age, profile = "Surgery", specialty = specialty)
        self.__specialty = specialty
        self.__doctor = doctor

    @property
    def specialty(self):
        return self.__specialty

    @property
    def doctor(self):
        return self.__doctor

    def get_department(self):
        return f"Surgery Department - {self.__specialty}| Doctor: {self.__doctor.name}"


class DiagnosticsPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty):
        super().__init__(patient_id, name, age, profile = "Diagnostics", specialty = specialty)
        self.__specialty = specialty

    @property
    def specialty(self):
        return self.__specialty

    def get_department(self):
        return f"Diagnostics Department - {self.__specialty}"


class Doctor():
    def __init__(self, doctor_id, name, specialty):
        self.__name = name
        self.__doctor_id = doctor_id
        self.__specialty = specialty
    
    @property
    def name(self):
        return self.__name
    
    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def specialty(self):
        return self.__specialty


def load_doctors(filename):
    doctors = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            doctor = Doctor(row["doctor_id"], row["name"], row["specialty"])
            if row["specialty"] not in doctors:
                doctors[row["specialty"]] = []
            doctors[row["specialty"]].append(doctor)
    return doctors


doctors = load_doctors("doctors.csv")










#Testavimas

def create_patient(patient_id, name, age, is_critical = False, visit_type= None, profile = None, specialty = None, doctor = None):
    patient = Patient(patient_id, name, age)

    if is_critical:
        return CriticalPatient(patient_id, name, age)
    elif patient.is_child():
        return ChildPatient(patient_id, name, age)
    elif visit_type == "Urgent":
        return UrgentPatient(patient_id, name, age)
    elif profile == "Therapy":
        return TherapyPatient(patient_id, name, age, specialty, doctor)
    elif profile == "Surgery":
        return SurgeryPatient(patient_id, name, age, specialty, doctor)    
    elif profile == "Diagnostics":
        return DiagnosticsPatient(patient_id, name, age, specialty)    
    else:
        raise ValueError("Invalid profile. Choose: Therapy, Surgery or Diagnostics")

class PatientRegistry:
    def __init__(self):
        self.__counter = 0

    def register_patient(self):
        self.__counter += 1
        patient_id = self.__counter
       
        name = input("Patient name: ")
        
        age = int(input("Patient age: "))
        is_critical = input("Is the patient in a critical state? (yes/no): ")
        if is_critical == "yes":
            return create_patient(patient_id, name, age, is_critical = True)
        if age < 18:
            return create_patient(patient_id, name, age)
        
        visit_type = input("Is the patient Urgent/Planned: ")
        if visit_type == "Urgent":
            return create_patient(patient_id, name, age, visit_type="Urgent")
        
        profile = input("Choose profile (Therapy/Surgery/Diagnostics): ")
        
        if profile == "Therapy":
            specialty = input("Choose the requested specialty from the Therapy Department (Neurology/Pulmonology/Cardiology/Hematology/Endokrinology/Gastroenterology): ")
            available_doctors = doctors[specialty]
            for i, doc in enumerate(available_doctors):
                print(f"{i+1}. {doc.name}")
            doctor_choice = int(input("Choose a doctor (1/2/3): ")) - 1
            doctor = available_doctors[doctor_choice]
            return create_patient(patient_id, name, age, visit_type=visit_type, profile=profile, specialty=specialty, doctor=doctor)
        
        if profile == "Surgery":
            specialty = input("Choose the requested specialty from the Sugery Department (Stomach/Chest/Eye/ENT): ")
            available_doctors = doctors[specialty]
            for i, doc in enumerate(available_doctors):
                print(f"{i+1}. {doc.name}")
            doctor_choice = int(input("Choose a doctor (1/2/3): ")) - 1
            doctor = available_doctors[doctor_choice]
            return create_patient(patient_id, name, age, visit_type=visit_type, profile=profile, specialty=specialty, doctor=doctor)
            
        if profile == "Diagnostics":
            specialty = input("Choose the requested specialty from the Diagnostics Department (KT/MRT/X-Ray/Lab): ")
            return create_patient(patient_id, name, age, visit_type=visit_type, profile=profile, specialty=specialty)
    


registry = PatientRegistry()
patient = registry.register_patient()
print(patient.get_department())

















# p1 = create_patient(1, "John", 10, False)
# p2 = create_patient(2, "Peter", 30, True)

# d1 = doctors["Cardiology"][0]
# p3 = create_patient(3, "Anna", 25, False, profile="Therapy", specialty="Cardiology", doctor=d1)

# print(p1.get_department())
# print(p2.get_department())
# print(p3.get_department())