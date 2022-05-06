import datetime
import os
import csv
import test_clinic
from test_clinic import *


### Global Variables ###

patients = []
doctors = []
nurses = []
receptionists = []

prescriptions = []
appointments = []


class HealthCareProfessional():
    def __init__(self,name, employee_no) -> None:
        self.name = name
        self.employee_no= employee_no

    def consultation(self):
        pass


class Doctor(HealthCareProfessional):
    
    def issue_prescription(self):
        pass


class Nurse(HealthCareProfessional):
    pass


class Patient():


    available_doctor = Doctor('Mohammad','001')    

    def __init__(self, name, address,phone) -> None:
        self.name = name
        self.address = address
        self.phone = phone
        patients.append(self)

    def request_repeat(self):

        refill = Prescription("Amoxicillin",self,self.available_doctor,1,"500 mg 1 x 2 x 7")
        return refill

    def request_appointment(self,receptionist,availabe_doctor):
        
        request = receptionist.make_appointment(self,appointments,availabe_doctor)

        return request


class Prescription():

    def __init__(self,type,patient,doctor,quantity,dosage) -> None:
        self.type = type
        self.patient = patient
        self.doctor = doctor
        self.quantity = quantity
        self.dosage = dosage

    def __str__(self) -> str:
        return f'Patient: {self.patient.name}, Type: {self.type}, Dosage: {self.dosage}, Quantity: {self.quantity}'

class Appointment():

    def __init__(self, type, staff, patient, date, time) -> None:
        self.patient = patient
        self.type = type
        self.staff = staff
        self.date = date
        self.time = time

    def __str__(self) -> str:
        return f'{self.date} {self.time} {self.patient.name} {self.staff.name} {self.type}'


        

class Receptionist():

    def __init__(self, name,employee_no) -> None:
        pass

    def make_appointment(self,patient,appointment_schedule,staff):
        first_available = AppointmentSchedule.find_next_available(staff,appointment_schedule)
        new_appointment = Appointment("Regular",staff,patient,first_available,"12:00")

        return new_appointment


    def cancel_appointment(self):
        pass


class AppointmentSchedule():


    def add_appointment(cls,patient,doctor,date, time):
        pass

    def cancel_appointment(self,patient,doctor,date, time):
        pass

    @classmethod
    def find_next_available(cls,doctor,appointments):
        return datetime.date.today()



# selected_receptionist = None
# selected_nurse = None
# selected_doctor= None


### Functions ###

def main_screen():
    '''Main user interface'''

    main_menu = input("\033[96mPlease select user:\033[0m\n\n\
        \033[93m 1:\033[0m Receptionist\n\
        \033[93m 2:\033[0m Nurse \n\
        \033[93m 3:\033[0m Doctor\n\
        \033[93m-1:\033[0m Anywhere to return to the main menu \n\
        \033[93m 0:\033[0m Quit\n\n\
        > ")

    if main_menu == '1':
                
        pass

       
       
    # elif main_menu == '2':
    #     clear_screen()
    #     add_patient_interface()
    #     export_to_cv()
    #     clear_screen()
    #     main_screen()

    # elif main_menu == '3':
    #     clear_screen()
    #     add_test_patients()
    #     export_to_cv() 
    #     print('') # A new line
    #     go_to_main_screen = input(
    #         '\033[96mHit enter to view schedule or enter -1 to go to main menu\033[0m: ')

    #     if go_to_main_screen == '':
    #         clear_screen()
    #         print_follow_up_schedule()
    #         print('') # A new line
    #         go_to_main_screen = input(
    #             '\033[96mHit enter to return to main screen\033[0m: ')
    #         if go_to_main_screen.isascii():
    #             clear_screen()
    #             main_screen()
    #     else:
    #         clear_screen()
    #         main_screen()

    # elif main_menu == '4':
    #     edit_delete_interface()
    #     export_to_cv()
    #     clear_screen()
    #     main_screen()

    # elif main_menu == '5':
    #     clear_screen()
    #     print_follow_up_schedule()
    #     print('') # A new line
    #     sort_interface()

    # elif main_menu in ['0', '-1']:
    #     clear_screen()
    #     print('\033[92mGood Bye!\033[0m')
    #     quit()

    # elif main_menu == '6':
    #     clear_screen()
    #     print_follow_up_schedule()
    #     print('') # A new line
    #     check_out_and_follow_interface()

    else:
        
        go_to_main_screen = input('\033[96mPlease enter one of the mentioned options only. Hit enter to try again, otherwise the application will quit\033[0m ')

        if go_to_main_screen == "":
        
            clear_screen()
            main_menu = ''
            main_screen()

        else:
            quit()


def add_object_to_list(user,users_list):
    '''Saves user data to a users list.
    for example, saves a doctor information to doctors list
    '''
    if not users_list:
        user_list_header = (list(vars(user).keys()))
        users_list.append(user_list_header)
        user_info = (list(vars(user).values()))
        users_list.append(user_info)

    else:
        user_info = (list(vars(user).values()))
        users_list.append(user_info)
  
    return users_list


def list_to_csv(users_list,file):
    '''Converts users data from a list to a csv file'''

    file = os.getcwd() + f'/{file}.csv'

    with open(file, 'w') as f:
        writer = csv.writer(f)
        for row in users_list:
            writer.writerow(row)

    return os.path.basename(file)[:-4]


def csv_to_list(users_list,file):
    '''Converts users data from a csv file to a list'''

    file = os.getcwd() + f'/{file}.csv'
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                users_list.append(row)


def list_to_object(user_type, user_info):
    '''Converts one user data from a list to an object'''
    
    user_object = user_type(*user_info)
    return user_object


def clear_screen():
    '''Clears the command line interface.'''

    return os.system(
        'cls' if os.name in ('nt', 'dos') else 'clear')




##### DATA IMPORT & CLEAR SCREEN #####

# import_from_cv()





##### User Interface #####

if __name__ == '__main__':
    test_clinic.unittest.main(exit=False)
    
    main_screen()

    

    