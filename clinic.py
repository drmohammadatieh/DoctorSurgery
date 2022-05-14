from copy import deepcopy
import datetime
import os
import csv
from this import d
import test_clinic
from test_clinic import *


### Global Variables ###


patients_list = [] # Stores patients data in a list format
doctors_list = []
selected_doctor = None
nurses_list = []
receptionists_list = []

prescriptions_list = []
appointments_schedule = []
today = datetime.datetime.today()

patients_headers = ['File No','First','last','Address','Phone']
doctors_headers =['Employee Number','Name']

test_patients = [
    ['John', 'Campbell', '01-12-2021', '12', '2'],
    ['Merry', 'Barnett', '01-12-2021', '3', '1'],
    ['Jordan', 'Frost', '01-12-2021', '3', '2'],
    ['Linda', 'Wright', '01-12-2019', '24', '2'],
    ['Angela', 'Rogers', '01-12-2018', '0', '1'],
    ['Sarah', 'Mcnaught', '01-12-2018', '0', '1'],]


class DuplicateRecord(Exception):
    pass


class HealthCareProfessional():

    obj_list = [] # Stores healthcare professionals as objects
    
    def __init__(self,employee_no,first_name,last_name) -> None:
        self.employee_no= employee_no
        self.first_name = first_name
        self.last_name = last_name
       

    def consultation(self):
        pass


class Doctor(HealthCareProfessional):

    
    def issue_prescription(self):
        pass


class Nurse(HealthCareProfessional):

    pass


class Patient():

    global patients_list # access the global patients_list that conain all patients in list format
    obj_list = [] # Stores patients as objects
    # available_doctor = Doctor('Mohammad','001') # Review

    def __init__(self,file_no,first_name,last_name, address='',phone='') -> None:
        self.file_no = file_no
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
       

   

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

    global today

    master_appointments_schedule = {} # Stores appointments schedules of all providers.

    def __init__(self,provider:HealthCareProfessional,no_of_months:int,hours_per_day:int) -> None:
        self.provider = provider
        self.no_of_months = no_of_months
        self.hours_per_day = hours_per_day

    def generate_slots(self):
        '''Generates 30-minute appointments slots according to 
        the no_of_months and the hours_per_day attributes
        '''
        schedule = [] 
        start_date = start_time = today.replace(second=0,microsecond=0)
        end_time = start_time + datetime.timedelta(hours =8)
        end_date = start_date + datetime.timedelta(days = self.no_of_months * 1)

        while start_date < end_date:
            if start_date.weekday() not in [5,6]:
                while start_time < end_time:
                    schedule.append([start_time.date(),start_time.time()])
                    start_time += datetime.timedelta(minutes=30)
           
            start_date += datetime.timedelta(days=1)
            start_time = datetime.datetime(start_date.year,start_date.month,start_date.day,8,0,0)
            end_time = start_time + datetime.timedelta(hours =8)
                 
        self.master_appointments_schedule[self.provider.name] = schedule
        for provider in self.master_appointments_schedule.keys():
            list_to_csv(self.master_appointments_schedule[provider],f'appointments_schedule - Dr. {provider}')


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

def print_list(headers, list = patients_list,):
    '''Prints a list or a schedule in a table format.'''

    # Print the list headers
    padding = ' ' * 8
    for header in headers:
        print(f'\033[38;5;15;48;5;20m{header}{padding}\033[0m', end='')

    print('') # A new line

    # Print dashed line (---) separating the headers from the rows
    print('-' * (sum([len(header)
          for header in headers]) + 8 * len(headers)))

    # Print the follow up schedule rows
    for j in range(len(list)):
        for i in range(len(headers)):
            i_padding = ' ' * \
                ((len(headers[i]) + 8) -
                 len(str(list[j][i])))
            print(
                f'\033[38;5;15;48;5;12m{list[j][i]}{i_padding}\033[0m', end='')

        print('') # A new line


def menu(options):
    '''Generates CLI menus
    parameters:
    options: desired menu options
    '''

    options_string = "\033[96mPlease select one of the options below:\033[0m\n\n"
    choice_number = 1
    for option in options:
        options_string += f"\033[93m {choice_number}:\033[0m {option}\n"
        choice_number +=1
    
    options_string += "\033[93m-1:\033[0m Anywhere to return to the main menu \n\
\033[93m 0:\033[0m Quit\n\n\
> "

    menu_selection = input(options_string)

    return menu_selection


def register_test_patients_list():
    '''Adds a group of test patients
for user testing applicationion features.
'''

    for patient in test_patients:
        duplicate = check_duplicate([patient[0], patient[1]])[0]

        if not duplicate:
            Patient('',patient[0], patient[1],patient[2],patient[3]).register()
          
            print(
                f'\033[92m{patient[0]} {patient[1]} was added successfully \033[0m')
        else:
            print(
                f'\033[91m{patient[0]} {patient[1]} is already on the follow up schedule\033[0m')



def register(registree):
    '''Registers a patient / doctor / nurse to the appropriate list.\n
    All new registrees get autogenerated file_no / employee_no.
    paramenter:
    type:  patient, doctor or nurse
    '''

    # Auto generate a file / employee number based on the maximum available file number
    # in the appropriate list
    
    if type(registree).__name__ =='Patient':
        if not registree.file_no:
            if not patients_list:
                registree.file_no ='1' 
            else:
                registree.file_no = str(max(int(patient[0]) for patient in patients_list) + 1)

        # registree.obj_list.append(registree)

    elif type(registree).__name__ =='Doctor':
        if not registree.employee_no:
            if not doctors_list:
                registree.employee_no ='1' 
            else:
                registree.employee_no = str(max(int(doctor[0]) for doctor in doctors_list) + 1)

        # registree.obj_list.append(registree)

    else:
        if not registree.employee_no:
            if not nurses_list:
                registree.employee_no ='1' 
            else:
                registree.employee_no = str(max(int(nurse[0]) for nurse in nurses_list) + 1)

        # registree.obj_list.append(registree)
        
    

   

# def register(self,duplicate = False):
#     '''Registers a patient / doctor / nurse to the appropriate list.\n
#     All new registrees get autogenerated file_no / employee_no.
#     '''

#     # Auto generate a file / employee number based on the maximum available file number
#     # in the appropriate list
#     if not duplicate:
#         if not self.file_no:
#             if not self.obj_list:
#                 self.file_no =1 
            
#             else:
#                 self.file_no = max(int(patient.file_no) for patient in self.obj_list) + 1

            
#         self.obj_list.append(self)

#     else:
#         raise DuplicateRecord

def check_duplicate(registree,registrees_list):
    '''Checks for duplicate entries
    while adding and editing patients.   
    '''

    global patients_list, doctors_list, nurses_list
    duplicate = False
    key = None 

    # If the first and last name are already in the patients_list, duplicate = True:
    for person in registrees_list:
        if person[1] == registree.first_name and person[2] == registree.last_name:
            duplicate = True
            key = person[0]
            break

    return [duplicate, key]


def registration_interface(registree_type,registrees_list):
    '''Interface for registering patients / doctors / nurses to the clinic.
    parameters:

    type: patient / doctor / nurse
    list: list name to be used for saving the registration information
    '''

    global patients_list, doctors_list, nurses_list

    new_registree = None
    
    def get_registration_fields(registree):
        '''Generates fields needed for registration'''

        registration_fields = list(vars(registree).keys())

        return registration_fields
    
    input_item = ''
    while input_item != '-1':

        # clear_screen()
        duplicate = False  # To store the value of the check_duplicate function
        input_dict = {} # Stores patient data from CLI input

        if new_registree is None :
            if registree_type == 'Doctor':
                new_registree = Doctor('','','') # Registers a new doctor  
                registrees_list = doctors_list

            elif registree_type =='Nurse':
                new_registree = Nurse('','','') # Registers a new doctor
                registrees_list = nurses_list
        
            elif registree_type =='Patient':
                new_registree = Patient('','','') # Registers a new patient
                registrees_list = patients_list

        registation_fields = get_registration_fields(new_registree)
        
        # Each header will be used as a key for the user input during adding patient information
        headers_list  = [field for field in registation_fields if field not in ['file_no','employee_no']]
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
                new_registree.first_name = input_dict['First name']
                new_registree.last_name = input_dict['Last name']
                duplicate, key = check_duplicate(new_registree,registrees_list)
              
                if duplicate:
                    print('') # A new line
                    registreeType = registree_type.lower()
                    print(f'\033[91mThis {registreeType} is already registered with a record no {key}\033[0m')
                    new_registree = None
                    break
        
        # If not duplicate, register that regisgree and add to the appropriate list
        if not duplicate:
            print('') # A new line
            add_confirmation = input(
                '\033[96mSave the information above (Y/N)?: \033[0m')
            print('') # A new line

            if add_confirmation.lower() == 'y':
    
                if registree_type == 'Patient':
                    new_registree.address, new_registree.phone = input_dict['Address'],input_dict['Phone']

                register(new_registree)
                registrees_list.append((objects_to_list(new_registree)))
                new_registree = None    
                print('\033[92mThe record was saved successfully\033[0m')
                print('') # A new line
                input_item = input(
                    '\033[96mHit enter to add another patient or enter -1 to go to main menu: \033[0m')
    
    # Save all objects data in the registree.obj_list to a csv file
    file_name = registree_type.lower() + 's_list'
    list_to_csv(registrees_list,file_name)

    clear_screen()
    main_screen()


def edit_delete_interface():
    pass


def search_name(search_string,list):
    '''Search a list for matching search_string.\n
search can be done by first name and/or last name partial or complete.
    '''

    search_results_list = [] 

    # If more than one search string:
    if len(search_string.split(' ')) > 1:

        first_name, last_name = search_string.split(' ')
        first_name = first_name.strip().lower()
        last_name = last_name.strip().lower()

        for patient in list:
            if patient[1].lower().find(first_name) != -1 and patient[2].lower().find(last_name) != -1:
                search_results_list.append(patient[0])
            else:
                continue

    else:
        search_string = search_string.strip().lower()

        # loop through the follow_up_schedule and append file_no of patient records
        # whom first_name or last_name matches the search_string
        for patient in list:
            if patient[1].lower().find(search_string) != -1 or patient[2].lower().find(search_string) != -1:
                search_results_list.append(patient[0])
            else:
                continue

    return search_results_list


def generate_appointments_schedules():
    '''Generates appointments schedules by the receptionist'''
   
    print_list( doctors_headers, doctors_list)



def appointments_interface():
    '''Interface for booking appointments for registered patients'''

    global patients_list, selected_doctor
   
    print_list(patients_headers)
    print('') # A new line

    # Starts by searching a record
    search_string = input(
        "\033[96mSearch by first and/or last name partial/complete or enter -1 to go to main menu: \033[0m")

    if search_string == '-1':
        clear_screen()
        main_screen()

    # If a match/es is/are found, print the filtered_patients_list:
    elif search_name(search_string,patients_list):
        search_result = search_name(search_string,patients_list)
        filtered_patients_list = [
            patient for patient in patients_list if patient[0] in search_result]
        clear_screen()
        print_list(patients_headers,filtered_patients_list)
        print('') # A new line

        mode_selection = menu(['Book Regular Appointment','Book Urgent Appointment','Cancel Appointment'])

        while mode_selection != '-1':

            file_no = ''
            # If Book Appointment is selected:
            if mode_selection == "1":
                file_no = input(
                    '\033[96mPlease select the file number for whom you want to schedule an appointment: \033[0m')
                patient_info = patients_list[
                    int([patient[0] for patient in patients_list 
                    if patient[0] == file_no][0])]

                selected_patient = list_to_object(Patient,patient_info) # The selected patient 
                
                appointment = Appointment('Regular',selected_doctor,selected_patient)
                selected_doctor = Doctor('Mohammad','1')
       
     
            # If Book Urgent Appointment is selected:
            elif mode_selection == "2":
                pass

            #If cancel appointment is selected:
            # elif mode_selection == "3":
            #     print('') # A new line
            #     file_no = input(
            #         '\033[96mPlease enter the number of the file you want to edit: \033[0m')
            #     if file_no == "-1":
            #         break
            #     while (not file_no.strip().isdigit()
            #            or file_no not in search_result):
            #         print('') # A new line
            #         file_no = input(
            #             '\033[91mPlease enter one of the file numbers above or enter -1 to go to main screen\033[0m: ')
            #         if file_no == "-1":
            #             clear_screen()
            #             main_screen()

            #     print('') # A new line
            #     edit_patient(file_no.strip())

            elif mode_selection == '':
                clear_screen()
                print_list(patients_headers)
                print('') # A new line
                appointments_interface()

            else:
                mode_selection = input(
                    '\033[31mPlease enter a valid selection mode: \033[0m')

        clear_screen()
        main_screen()

    # If there is no match found:
    else:
        print('') # A new line
        what_next = input(
            '\033[91mNo match was found hit enter to try again or enter -1 to go to main menu: \033[0m')
        print('') # A new line
        if what_next == '-1':
            clear_screen()
            main_screen()

        else:
            appointments_interface()

def receptionist_interface():
    '''Receptionist interface for registering patients_list, assigning them
     to doctors_list, and booking appointments
     '''
    options = ['Register Patients','Book Appointment / Request Repeat','Edit/Delete Patients','Generate Appointments Schedules']
    menu_selection = menu(options)

    if menu_selection == '1' :
        registration_interface('Patient',patients_list)

    if menu_selection == '2' :
        appointments_interface()

    if menu_selection == '3' :
        edit_delete_interface()

    if menu_selection == '4' :
        generate_appointments_schedules()
    
    elif  menu_selection == '-1' :
        clear_screen()
        main_screen()

def register_doctors():
    pass


def register_nurses():
    pass

def administration_interface():
    '''Administration interface for adding healthcare providers to the clinic'''

    options = ['Add doctors to the clinic','Add nurses to the clinic']
    menu_selection = menu(options)

    if menu_selection == '1' :
        registration_interface('Doctor',doctors_list)

    if menu_selection == '2' :
        registration_interface('Nurse',doctors_list)


def objects_to_list(object):
    '''Saves object data to a string list
    to facilitate exporting to a csv file.
    '''
    
    object_info = (list(vars(object).values()))
  
    return object_info


def list_to_csv(list,file):
    '''Converts list data to a csv file'''

    file = os.getcwd() + f'/{file}.csv'

    with open(file, 'w') as f:
        writer = csv.writer(f)
        for row in list:
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


def list_to_object(type, attributes):
    '''Converts one user data from a list to an object'''
    
    object = type(*attributes)
    return object


def import_from_cv():
    '''Imports saved data to the application'''

    file_names = ['patients_list','doctors_list','nurses_list','appointments_schedule']
    registrees_lists = [patients_list,doctors_list,nurses_list,appointments_schedule]
    classes = [Patient,Doctor,Nurse]

    for file, registree_list,class_type in zip(file_names,registrees_lists,classes):
        
        file = os.getcwd() + f'/{file}.csv'
        registree_list.clear()
        class_type.obj_list.clear()
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    registree_list.append(row)    


def clear_screen():
    '''Clears the command line interface.'''

    return os.system(
        'cls' if os.name in ('nt', 'dos') else 'clear')

def main_screen():
    '''Main user interface'''

    options=['Print','Receptionist','Nurse','Doctor','Administration']
    main_menu = menu(options)

    if main_menu == '1':
       clear_screen()
       import_from_cv()
       print_list(patients_headers)
       print('') # A new line
       main_screen()
   
    elif main_menu == '2':
        clear_screen()
        receptionist_interface()

    elif main_menu == '5':
        clear_screen()
        administration_interface()
        

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

    elif main_menu in ['0', '-1']:
        clear_screen()
        print('\033[92mGood Bye!\033[0m')
        quit()

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




##### User Interface #####

if __name__ == '__main__':

    test_clinic.unittest.main(exit=False)

    what_next = input('\033[96mPlease hit enter to start the application\033[0m ')

    if what_next == '':
        import_from_cv()
        main_screen()
       
    

    