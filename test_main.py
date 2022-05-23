import unittest
import os
import csv
import main
from main import RegisteredPatientsLimit # Review
from main import * 





class TestClinic(unittest.TestCase):


    @classmethod
    def setUpClass(cls) -> None:
    
        print('\033[38;5;15;48;5;20m Running Self Tests!:\033[0m')

        cls.users_list = []
        cls.patient_1_info = ['1','Rolland', 'Manassa','3844 Yeager St','712-235-9932','David Miller']
        cls.patient_2_info = ['2','Jude','Basin','8069 Florian St','275-850-5092','David Miller']
        cls.patient_1 = main.Patient('','Rolland', 'Manassa','3844 Yeager St','712-235-9932','David Miller')
        cls.patient_2 = main.Patient('','Jude','Basin','8069 Florian St','275-850-5092','David Miller')
        cls.patients_list_1 =[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','David Miller']]
        cls.patients_list_2 =[['1','Rolland', 'Manassa', '3844 Yeager St', '712-235-9932','David Miller'],
        ['2','Jude','Basin','8069 Florian St','275-850-5092','David Miller']]
        cls.doctor_1_info= ['999','David' ,'Miller']
        cls.doctor_1 = Doctor(*cls.doctor_1_info)


    def test_register_patient(self):
        '''Tests the process of registering a patient'''

        patients_list.clear()
        register(self.patient_1)
        patients_list.append (object_to_list(self.patient_1))
        register(self.patient_2)
        patients_list.append (object_to_list(self.patient_1))
        # Check if the patient object attributes matches the given patient information
        self.assertEqual(self.patient_1_info, list(vars(self.patient_1).values()))
        self.assertEqual(self.patient_2_info, list(vars(self.patient_2).values()))
        patients_list.clear()


    def test_register_patient_limit(self):
        '''Tests of the 500 patients registration limit'''

        patients_list.clear()
        # Save dummy 500 patients information to the patients_list
        for n in range(0,501):
            patients_list.append([n] + self.patient_1_info[1:])

        # Try to add another patient; a RegisteredPatientsLimit Exception is expected
        with self.assertRaises(RegisteredPatientsLimit):
            register(self.patient_2)


        
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
        healthcare_professional = list_to_object(Doctor,self.doctor_1_info)
        self.assertIsInstance(healthcare_professional,HealthCareProfessional)


    def test_save_load_csv(self):
        '''Tests saving users list to csv file and loading from the file back to the list'''

        file = list_to_csv(self.patients_list_1,'patients_list_test')
        patients_list = []
        csv_to_list(patients_list,file)
        self.assertEqual(patients_list,self.patients_list_1)


    def test_find_next_available(self):
        '''Tests the function of finding next available appointment'''

        # Register a test doctor
        register(self.doctor_1)
        doctors_list= []
        # Add the test doctor to the doctors_list.csv
        file = os.getcwd() + '/doctors_list.csv'
        with open(file,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                doctors_list.append(row)

        doctors_list.append(self.doctor_1_info)
        list_to_csv(doctors_list,'doctors_list')

        # Create an AppointmentSchedule object
        appointment_schedule = AppointmentSchedule(self.doctor_1,1,3)
        appointment_schedule.generate_slots()

        # Import the generated appointment schedule from csv file
        import_from_cv()

        # Find first available appointment
        appoinment_match = AppointmentSchedule.find_next_available(self.patient_1,False)
        AppointmentSchedule.add_appointment(*appoinment_match)


        def test_cancel_appointment(self):

            receptionist.cancel_appointment(appoinment_match[1],)



        # Test the Class of the generated appointment
        self.assertIsInstance(appoinment_match[0],Appointment)

        # Verify that the first available appointment for Dr. David Miller was chosen
        self.assertEqual(appoinment_match[0].date,doctors_appointments['David Miller'][0][1])

        # Delete the test doctor from the doctors_list.csv
        doctors_list.pop()
        list_to_csv(doctors_list,'doctors_list')
        os.remove(os.getcwd() + '/appointments_schedule - Dr. David Miller.csv')


            


    



    




        










