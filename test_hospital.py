import unittest
from HospitalRegistrationSystem import (
    Patient, CriticalPatient, ChildPatient,
    AdultPatient, UrgentPatient, PlannedPatient, 
    TherapyPatient, SurgeryPatient, DiagnosticsPatient, 
    Doctor, create_patient
)


class TestPatient (unittest.TestCase):
    def test_patient_attributes(self):
        p = Patient(1, "John", 25)
        self.assertEqual(p.patient_id, 1)
        self.assertEqual(p.name, "John")
        self.assertEqual(p.age, 25)

    def test_is_child_true(self):
        p = Patient(2, "Jack", 10)
        self.assertTrue(p.is_child())
    
    def test_is_child_false(self):
        p = Patient(3, "Jerry", 25)
        self.assertFalse(p.is_child())
    
    def test_age_setter_invalid(self):
        p = Patient(1, "John", 25)
        with self.assertRaises(ValueError):
            p.age = -1


class TestCreatePatient(unittest.TestCase):

    def test_create_critical_patient(self):
        p = create_patient(1, "John", 30, is_critical=True)
        self.assertIsInstance(p, CriticalPatient)

    def test_create_child_patient(self):
        p = create_patient(2, "Jack", 10)
        self.assertIsInstance(p, ChildPatient)

    def test_create_urgent_patient(self):
        p = create_patient(3, "Jerry", 30, visit_type="Urgent")
        self.assertIsInstance(p, UrgentPatient)

    def test_create_diagnostics_patient(self):
        p = create_patient(4, "Anna", 30, profile="Diagnostics", specialty="CT")
        self.assertIsInstance(p, DiagnosticsPatient)

        
if __name__ == '__main__':
    unittest.main()