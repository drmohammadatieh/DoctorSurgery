import unittest
import clinic
from clinic import *




class TestClinic(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
    
        print('\033[38;5;15;48;5;20m Running Self Tests!:\033[0m')

     
        cls.users_list = []
        cls.patient_1 = Patient('Rolland', 'Manassa','3844 Yeager St','712-235-9932','1')
        cls.patient_info = ['Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','1']
        cls.patients_list_1 =[['Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','1']]
        cls.patients_list_2=[['Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','1'],
        ['Jude', 'Basin','8069 Florian St','275-850-5092','2']]
        cls.patient_2 = Patient('Jude','Basin','8069 Florian St','275-850-5092','2')

        cls.healthcare_professional_info= ['David Miller','1']


    def test_register_patient(self):
        '''Tests the process of registering a patient'''

        new_patient_1 = self.patient_1
        new_patient_1.register()
        new_patient_2 = self.patient_1
        new_patient_2.register()
        print('here',new_patient_1)


        self.assertEqual(Patient.patients_list, [new_patient_1])
        

    def test_save_data_to_list(self):
        '''Test saving object data to a list'''

        saved_data = objects_to_list([self.patient_1])
        self.assertEqual(saved_data,self.patients_list_1)

        saved_data = objects_to_list([self.patient_1,self.patient_2])
        self.assertEqual(saved_data,self.patients_list_2)


    def test_list_to_object(self):
        '''Test converting object data from list to an object'''

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
        '''Test saving users list to csv file and loading form the file back to the list'''

        file = list_to_csv(self.patients_list_2,'patients_list_test')
        patients_list = []
        csv_to_list(patients_list,file)
        self.assertEqual(patients_list,self.patients_list_2)




receptionist_1 = Receptionist('Susan','1')

doctor_1 = Doctor("Mohammad Atieh",1)

patient_tuple = 'Rami','Atieh','Amman','5232208','1'
patient_1 = Patient(*patient_tuple)

appointment_1 = patient_1.request_appointment(receptionist_1,doctor_1)

print(vars(patient_1).values())









