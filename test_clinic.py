from pydoc import doc
import unittest
import clinic
from clinic import *




class TestClinic(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
    
        print('\033[38;5;15;48;5;20m Running Self Tests!:\033[0m')

     
        cls.users_list = []
        cls.patient_1 = Patient('Rolland Manassa','3844 Yeager St','712-235-9932')
        cls.patient_info = ['Rolland Manassa', '3844 Yeager St', '712-235-9932']
        cls.users_list_1 =[['name', 'address', 'phone'], ['Rolland Manassa', '3844 Yeager St', '712-235-9932']]
        cls.users_list_2=[['name', 'address', 'phone'], ['Rolland Manassa', '3844 Yeager St', '712-235-9932'],
        ['Jude Basin','8069 Florian St','275-850-5092']]
        cls.patient_2 = Patient('Jude Basin','8069 Florian St','275-850-5092')

        cls.healthcare_professional_info= ['David Miller','1']

        

    def test_save_data_to_list(self):
        '''Test saving user data to a list'''

       

        # Test if the first user information is appended to the list correctly
    
        saved_data = add_object_to_list(self.patient_1,self.users_list)
        self.assertEqual(saved_data,self.users_list_1)


        # Test if subsequent users are added to the list correctly without duplicating the header
        
        saved_data = add_object_to_list(self.patient_2,self.users_list)
        self.assertEqual(saved_data,self.users_list_2)


    def test_list_to_object(self):
        '''Test converting user info to an object'''


        # Test converting patient info to an object
        patient = list_to_object(Patient,self.patient_info)
        self.assertIsInstance(patient,Patient)

        # Test converting healthcare professional info to an object
        healthcare_professional = list_to_object(Doctor,self.healthcare_professional_info)
        self.assertIsInstance(healthcare_professional,HealthCareProfessional)



    def test_save_to_csv(self):
        '''Test saving users list to csv file and loading form the file back to the list'''

        file = list_to_csv(self.users_list_2,'patients')
        users_list=[]
        csv_to_list(users_list,file)
        self.assertEqual(users_list,self.users_list_2)





receptionist_1 = Receptionist('Susan','1')

doctor_1 = Doctor("Mohammad Atieh",1)

patient_tuple = 'Rami','Amman','5232208'
patient_1 = Patient(*patient_tuple)

appointment_1 = patient_1.request_appointment(receptionist_1,doctor_1)

print(vars(patient_1).values())









