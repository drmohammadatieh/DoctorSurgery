import unittest
import clinic
from clinic import * 
from clinic import DuplicateRecord




class TestClinic(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
    
        print('\033[38;5;15;48;5;20m Running Self Tests!:\033[0m')

     
        cls.users_list = []
        cls.patient_1 = clinic.Patient('1','Rolland', 'Manassa','3844 Yeager St','712-235-9932')
        cls.patient_2 = clinic.Patient('2','Jude','Basin','8069 Florian St','275-850-5092')
        cls.patient_info = ['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932']
        cls.patients_list_1 =[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932']]
        cls.patients_list_2=[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932'],
        ['2','Jude', 'Basin','8069 Florian St','275-850-5092']]
       

        cls.healthcare_professional_info= ['1','David' ,'Miller']


    def test_register_patient(self):
        '''Tests the process of registering a patient'''

        Patient.patients_obj_list.clear()
        new_patient_1 = self.patient_1
        new_patient_1.register(False)
        new_patient_2 = self.patient_2
        new_patient_2.register(False)
        self.assertEqual(Patient.patients_obj_list, [new_patient_1,new_patient_2])


    def test_register_duplicate_patient(self):
        '''Tests the process of registering a patient'''

        Patient.patients_obj_list.clear()
        new_patient_1 = self.patient_1
        new_patient_1.register(False)
        new_patient_2 = self.patient_1
        with self.assertRaises(DuplicateFileNumber):
            self.patient_2.register(True)
        
              

    def test_save_data_to_list(self):
        '''Tests saving object data to a list'''

        saved_data = objects_to_list([self.patient_1])
        self.assertEqual(saved_data,self.patients_list_1)

        saved_data = objects_to_list([self.patient_1,self.patient_2])
        self.assertEqual(saved_data,self.patients_list_2)


    def test_list_to_object(self):
        '''Tests creating objects from list data'''

        # Test converting patient info to an object
        patient = list_to_object(Patient,self.patient_info)
        self.assertIsInstance(patient,Patient)
        self.assertEqual(patient.first_name,'Rolland')
        self.assertEqual(patient.last_name,'Manassa')
        self.assertEqual(patient.address,'3844 Yeager St')
        self.assertEqual(patient.phone,'712-235-9932')
        self.assertEqual(patient.file_no,'1')

        # Test converting healthcare professional info to an object
        healthcare_professional = list_to_object(Doctor,self.healthcare_professional_info)
        self.assertIsInstance(healthcare_professional,HealthCareProfessional)


    def test_save_to_csv(self):
        '''Tests saving users list to csv file and loading form the file back to the list'''

        file = list_to_csv(self.patients_list_2,'patients_list_test')
        patients_list = []
        csv_to_list(patients_list,file)
        self.assertEqual(patients_list,self.patients_list_2)




# receptionist_1 = Receptionist('Susan','1')

# doctor_1 = Doctor("Mohammad Atieh",1)

# patient_tuple = 'Rami','Atieh','Amman','5232208','1'
# patient_1 = Patient(*patient_tuple)

# appointment_1 = patient_1.request_appointment(receptionist_1,doctor_1)

# print(vars(patient_1).values())









