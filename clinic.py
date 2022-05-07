import datetime
import os
import csv
import test_clinic
from test_clinic import *


### Global Variables ###

doctors_list = []
nurses_list = []
receptionists_list = []

prescriptions_list = []
appointments_schedule = []


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

    patients_list = []
    available_doctor = Doctor('Mohammad','001') # Review

    def __init__(self,first_name,last_name, address='',phone='',file_no='') -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.file_no = file_no


    def check_duplicate(self):
        '''Checks for duplicate entries
        while adding and editing patients_list.   
        '''
        duplicate = False
        file_no = None

        # If the first and last name are already in the patients_list, duplicate = True:
        for patient in self.patients_list:
            if patient.first_name == self.first_name and patient.last_name == self.last_name:
                duplicate = True
                file_no = patient.file_no
                break

        return [duplicate, file_no]


    def register(self):
        '''Registers patient to the patients_list list.\n
        File_no is optional; it is used for editing.\n
        All new patients_list get autogenerated file_no.
        '''

        # Auto generate a file number based on the maximum available file number
        # in the patients_list list
        if not self.file_no:
            if not self.patients_list:
                self.file_no =1 
               
            else:
                self.file_no = max(int(patient.file_no) for patient in self.patients_list) + 1

            self.patients_list.append(self)


    def request_repeat(self):

        refill = Prescription("Amoxicillin",self,self.available_doctor,1,"500 mg 1 x 2 x 7")
        return refill
        

    def request_appointment(self,receptionist,availabe_doctor):
        
        request = receptionist.make_appointment(self,appointments_schedule,availabe_doctor)

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

def menu(options):
    '''Generates CLI menus'''

    options_string = "\033[96mPlease select one of the options below:\033[0m\n\n"
    choice_number = 1
    for option in options:
        options_string += f"\033[93m {choice_number}:\033[0m {option}\n"
        choice_number +=1
    
    options_string += "\033[93m-1:\033[0m Anywhere to return to the main menu \n\
\033[93m 0:\033[0m Quit\n\n\
> "

    clear_screen()
    menu_selection = input(options_string)

    return menu_selection



def register_test_patients_list():
    '''Adds a group of test patients_list
for testing and trying application feature.
'''
    for patient in test_patients_list:
        duplicate = check_duplicate([patient[0], patient[1]])[0]

        if not duplicate:
            add_patient(patient[0], patient[1],
                        patient[2], patient[3], patient[4])
            print(
                f'\033[92m{patient[0]} {patient[1]} was added successfully \033[0m')
        else:
            print(
                f'\033[91m{patient[0]} {patient[1]} is already on the follow up schedule\033[0m')





def register_patient_interface():
    '''Interface for registering patients_list to the clinic.'''

    new_patient = Patient('','') # Initializes a new patient
    input_item = ''
    while input_item != '-1':

        # clear_screen()
        duplicate = False  # To store the value of the check_duplicate function
        input_dict = {} # Stores patient data from CLI input
        
        # Each header will be used as a key for the user input during adding patient information
        headers_list  = ['first_name','last_name', 'address','phone']
        for header in headers_list:
            header = header.replace('_', ' ').capitalize()
            if header not in ['Address' ,'Phone']:
        
                input_item = input(f'{header}: ').strip()
                while not input_item.replace(' ','').isalpha() and input_item != '-1':
                    input_item = input(
                        f'\033[91mplease enter a valid {header} or enter -1 to go to main menu: \033[0m').strip()

            elif header == 'Phone':

                # Make sure the entered phone number contains only digits
                input_item = input(f'{header}: ').strip()
                while not input_item.replace(' ','').isdigit() and input_item != '-1':
                    input_item = input(
                        f'\033[91mplease enter a valid {header} or enter -1 to go to main menu: \033[0m').strip()
            else:
                input_item = input(f'{header}: ')
                
            input_item.strip()

            if input_item == "-1":
                clear_screen()
                main_screen()
            else:
                input_dict[header] =(input_item.lower().title())

        # Check if there is duplicate name with the same first and last name
            if header == 'Last name':
                new_patient = Patient(*list(input_dict.values()))
                duplicate, file_no = new_patient.check_duplicate()
              
                if duplicate:
                    print('') # A new line
                    what_next = input(f'\033[91mThis patient is already registered with a file no: {file_no}\033[0m')
                    
                    if what_next == '':
                        input_dict.clear()
                        break

        if not duplicate:
            print('') # A new line
            add_confirmation = input(
                '\033[96mSave the information above (Y/N)?: \033[0m')
            print('') # A new line

            if add_confirmation.lower() == 'y':
    
                new_patient.address, new_patient.phone = input_dict['Address'],input_dict['Phone']
                new_patient.register()
                alist=[]
                objects_to_list(Patient.patients_list,alist)
                print(alist)
                # list_to_csv(patients_list,'patients_list')
                print('\033[92mThe record was saved successfully\033[0m')
                print('') # A new line
                input_item = input(
                    '\033[96mHit enter to add another patient or enter -1 to go to main menu: \033[0m')

    clear_screen()
    main_screen()

def receptionist_interface():
    '''Receptionist interface for registering patients_list, assigning them
     to doctors_list, and booking appointments
     '''
    options = ['Register new patient','Book appointment','Request prescription refill']
    menu_selection = menu(options)

    if menu_selection == '1' :
        register_patient_interface()


def main_screen():
    '''Main user interface'''

    options=['Receptions','Nurse','Doctor']
    main_menu = menu(options)

    if main_menu == '1':
        receptionist_interface()
        

    # elif main_menu == '2':
    #     clear_screen()
    #     add_patient_interface()
    #     export_to_cv()
    #     clear_screen()
    #     main_screen()

    # elif main_menu == '3':
    #     clear_screen()
    #     add_test_patients_list()
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



def objects_to_list(objects_list,str_list):
    '''Saves objects data to a string list
    to facilitate saving data to a csv file.
    '''
    for object in objects_list:
        object_info = (list(vars(object).values()))
        str_list.append(object_info)
  
    return str_list


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

    

    