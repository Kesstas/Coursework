# Hospital Registration System

## Introduction

### What is this application?
The Hospital Registration System is a Python-based application designed to streamline the patient registration process in a clinical environment. The system guides the user through a step-by-step registration process, collecting patient information and automatically routing them to the appropriate department and specialist based on their age, condition, and medical needs.

### How to run the program?
1. Ensure Python 3 is installed on your system.
2. Clone the repository from GitHub.
3. Make sure `doctors.csv` is in the same folder as `HospitalRegistrationSystem.py`.
4. Run the program:
```bash
python HospitalRegistrationSystem.py
```

### How to use the program?
The program will prompt you to enter the following information step by step:
1. Patient name
2. Patient age
3. Whether the patient is in a critical state
4. Visit type (Urgent or Planned)
5. Medical profile (Therapy, Surgery, or Diagnostics)
6. Specialty and doctor selection (where applicable)

Once registration is complete, the patient's details are automatically saved to `patient_reports.txt`. The program runs entirely through the terminal — no graphical interface is required.

## Body/Analysis

### Encapsulation
Encapsulation is the principle of hiding internal data and only exposing what is necessary through controlled access. In this program, all `Patient` attributes are defined as private using double underscores (`__`), preventing direct access from outside the class. Access is provided through `@property` getters, and controlled modification through setters with validation.

```python
class Patient:
    def __init__(self, patient_id, name, age, is_critical=False, ...):
        self.__patient_id = patient_id
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @age.setter
    def age(self, age):
        if age < 0:
            raise ValueError("Age cannot be below zero")
        self.__age = age
```

This ensures that patient data cannot be modified arbitrarily — for example, age can only be changed through the setter, which validates the input.

### Inheritance
Inheritance allows a class to acquire the properties and methods of another class. In this program, a clear hierarchy is built on top of the base `Patient` class.

```python
class Patient:
    ...

class AdultPatient(Patient):
    ...

class PlannedPatient(AdultPatient):
    ...

class TherapyPatient(PlannedPatient):
    ...
```

`TherapyPatient` inherits from `PlannedPatient`, which inherits from `AdultPatient`, which inherits from `Patient`. This means `TherapyPatient` automatically has access to all attributes and methods defined in `Patient` — such as `name`, `age`, `is_child()` — without redefining them.

### Polymorphism
Polymorphism allows different classes to share the same method name, but each implementing it differently. In this program, every patient class implements `get_department()`, but each returns a different result depending on the patient type.

```python
patients = [
    CriticalPatient(1, "John", 30),
    ChildPatient(2, "Jack", 10),
    UrgentPatient(3, "Anna", 25),
]

for patient in patients:
    print(patient.get_department())
```

Output:
```
Intensive Care Unit
Pediatric care
Emergency Room
```

The same method call `get_department()` produces different results depending on the object type. The calling code does not need to know which type it is dealing with — each object handles it internally.

### Abstraction
Abstraction means hiding complex implementation details and exposing only what is necessary. In this program, abstraction is demonstrated in two ways.

First, the `Patient` base class defines `get_department()` as a method that raises `NotImplementedError`, signaling that every subclass must implement it:

```python
def get_department(self):
    raise NotImplementedError("Every patient type must implement get_department()")
```

Second, the `PatientRegistry` class hides all registration complexity behind a simple interface. The user only answers questions — the routing logic, object creation, and file saving happen internally without the user needing to know anything about the underlying structure.

### Design Pattern — Factory Method
The Factory Method pattern is used to create objects without specifying the exact class to instantiate. In this program, the `create_patient()` function acts as a factory — it receives patient data and decides which patient class to instantiate based on the provided parameters.

```python
def create_patient(patient_id, name, age, is_critical=False, visit_type=None, profile=None, specialty=None, doctor=None):
    patient = Patient(patient_id, name, age)

    if is_critical:
        return CriticalPatient(patient_id, name, age)
    elif patient.is_child():
        return ChildPatient(patient_id, name, age)
    elif visit_type == "Urgent":
        return UrgentPatient(patient_id, name, age)
    elif profile == "Therapy":
        return TherapyPatient(patient_id, name, age, specialty, doctor)
    ...
```

This pattern is suitable here because the type of patient object depends on multiple conditions that are only known at runtime. The calling code does not need to know which class is being created — it simply receives the correct object.

### Aggregation
Aggregation is a relationship where one object contains another, but both can exist independently. In this program, `TherapyPatient` and `SurgeryPatient` contain a `Doctor` object.

```python
class TherapyPatient(PlannedPatient):
    def __init__(self, patient_id, name, age, specialty, doctor):
        super().__init__(patient_id, name, age, profile="Therapy", specialty=specialty)
        self.__doctor = doctor

    @property
    def doctor(self):
        return self.__doctor
```

The `Doctor` objects are created independently by `load_doctors()` from `doctors.csv`, and only then passed into the patient object. This means a `Doctor` can exist without a patient — demonstrating aggregation rather than composition.

### File I/O
The program uses two files — `doctors.csv` for reading and `patient_reports.txt` for writing.

**Reading from CSV:**
The `load_doctors()` function reads `doctors.csv` at program startup and creates `Doctor` objects from each row:

```python
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
```

**Writing to TXT:**
After registration, `save_report()` appends the patient's details to `patient_reports.txt`:

```python
def save_report(patient, entry_count):
    with open("patient_reports.txt", "a") as f:
        f.write(f"""==========Entry:{entry_count}==========
        Patient ID: {patient.patient_id}
        ...
===========================\n\n""")
```

Each new registration is appended to the file without overwriting previous entries.

## Results and Summary

### Results
- The Hospital Registration System was successfully implemented, covering all core functional requirements including patient classification, department routing, doctor selection, and report generation.
- All four OOP pillars were applied throughout the program — encapsulation through private attributes and properties, inheritance through the patient class hierarchy, polymorphism through `get_department()`, and abstraction through `PatientRegistry` and the base `Patient` class.
- The Factory Method design pattern was implemented via `create_patient()`, which cleanly separates object creation logic from the rest of the program.
- Input validation was implemented throughout the registration process, ensuring the program handles incorrect user input gracefully by re-prompting the user.
- One challenge faced during implementation was managing data flow through the inheritance hierarchy — passing attributes like `visit_type`, `profile`, and `specialty` through multiple levels of `super().__init__()` calls required careful planning.

### Conclusions
The Hospital Registration System achieves its goal of automating and structuring the patient registration process in a clinical environment. The program demonstrates how OOP principles can be applied to model real-world systems — patients are represented as objects with clear hierarchies, departments are abstracted behind a common interface, and doctor assignment is handled through aggregation.

The result is a functional terminal-based application that routes patients to the correct department, assigns specialists where needed, and saves registration records to a file.

Future prospects for the program include:
- A graphical user interface (GUI) to replace the terminal-based interaction
- The ability to navigate back to previous steps during registration
- A doctor management system allowing administrators to add, remove, or update doctors without editing the CSV file directly
- Database integration to replace file-based storage for better scalability