import unittest
from clinic import *

class TestClinic(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
       
    #     print('''\n\033[38;5;15;48;5;20mTesting\033[0m

    #     --------------------------------------------

    #     ''')

    # @classmethod
    # def tearDownClass(cls) -> None:
    #    pass


    def test_first(self):
        print('First false test has passed')

        self.assertEqual(1,1)


receptionist_1 = Receptionist('Susan','1')
 
doctor_1 = Doctor("Mohammad Atieh",1)

patient_1 = Patient('Rami','Amman','5232208')

appointment_1 = patient_1.request_appointment(receptionist_1,doctor_1)

print(appointment_1)





