import unittest
import clinic
from clinic import * 
from clinic import DuplicateRecord




class TestClinic(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
    
        print('\033[38;5;15;48;5;20m Running Self Tests!:\033[0m')

        cls.users_list = []
        cls.patient_1_info = ['1','Rolland', 'Manassa','3844 Yeager St','712-235-9932','Doctor Name']
        cls.patient_2_info = ['2','Jude','Basin','8069 Florian St','275-850-5092','Doctor Name']
        cls.patient_1 = clinic.Patient('','Rolland', 'Manassa','3844 Yeager St','712-235-9932','Doctor Name')
        cls.patient_2 = clinic.Patient('','Jude','Basin','8069 Florian St','275-850-5092','Doctor Name')
        cls.patients_list_1 =[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','Doctor Name']]
        cls.patients_list_2 =[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','Doctor Name'],
        ['2','Jude','Basin','8069 Florian St','275-850-5092','Doctor Name']]
        cls.healthcare_professional_info= ['1','David' ,'Miller']


    def test_register_patient(self):
        '''Tests the process of registering a patient'''

        register(self.patient_1)
        patients_list.append (object_to_list(self.patient_1))
        register(self.patient_2)
        patients_list.append (object_to_list(self.patient_1))
        # Check if the patient object attributes matches the given patient information
        self.assertEqual(self.patient_1_info, list(vars(self.patient_1).values()))
        self.assertEqual(self.patient_2_info, list(vars(self.patient_2).values()))
        patients_list.clear()
    

        
    def test_check_duplicate(self):
        '''Tests the process of detecting duplicate patient information'''

        register(self.patient_1)
        patients_list.append (object_to_list(self.patient_1))
        self.assertTrue(check_duplicate(self.patient_1,patients_list)[0])
        patients_list.clear()
      
          

    def test_save_data_to_list(self):
        '''Tests saving object data to a list'''

        register(self.patient_1)
        saved_data = [object_to_list(self.patient_1)]
        self.assertEqual(saved_data,self.patients_list_1)
  

    def test_list_to_object(self):
        '''Tests creating objects from list data'''

        # Test converting patient info to an object
        patient = list_to_object(Patient,self.patient_1_info)
        self.assertIsInstance(patient,Patient)
        self.assertEqual(patient.first_name,'Rolland')
        self.assertEqual(patient.last_name,'Manassa')
        self.assertEqual(patient.address,'3844 Yeager St')
        self.assertEqual(patient.phone,'712-235-9932')
        self.assertEqual(patient.file_no,'1')

        # Test converting healthcare professional info to an object
        healthcare_professional = list_to_object(Doctor,self.healthcare_professional_info)
        self.assertIsInstance(healthcare_professional,HealthCareProfessional)


    def test_save_load_csv(self):
        '''Tests saving users list to csv file and loading from the file back to the list'''

        file = list_to_csv(self.patients_list_1,'patients_list_test')
        patients_list = []
        csv_to_list(patients_list,file)
        self.assertEqual(patients_list,self.patients_list_1)










