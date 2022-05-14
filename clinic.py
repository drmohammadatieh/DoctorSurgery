from copy import deepcopy
from dataclasses import dataclass
import datetime
import os
import csv
from this import d
from typing import Type
import test_clinic
from test_clinic import *
import glob


### Global Variables ###


patients_list = [] # Stores patients data in a list format
doctors_list = [] # Stores doctors data in a list format
nurses_list = [] # Stores nurses data in a list format
receptionist = None # Stores the default receptionist that is initialized when the application runs
prescriptions_list = []
doctors_appointments = {}
nurses_appointments = {}
today = datetime.datetime.today()

patients_headers = ['File No','First Name','Last Name','Address','Phone']
doctors_headers =['Employee Number','Fist Name','Last Name']
nurses_headers =['Employee Number','Fist Name','Last Name']

test_patients = [
    ['John', 'Campbell', '01-12-2021', '12', '2'],
    ['Merry', 'Barnett', '01-12-2021', '3', '1'],
    ['Jordan', 'Frost', '01-12-2021', '3', '2'],
    ['Linda', 'Wright', '01-12-2019', '24', '2'],
    ['Angela', 'Rogers', '01-12-2018', '0', '1'],
    ['Sarah', 'Mcnaught', '01-12-2018', '0', '1'],]


class DuplicateRecord(Exception):

    pass

class Employee():

    obj_list = [] # Stores employees as objects

    def __init__(self,employee_no,first_name,last_name) -> None:
        self.employee_no= employee_no
        self.first_name = first_name
        self.last_name = last_name


class HealthCareProfessional(Employee):

    def consultation(self):
        pass

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Doctor(HealthCareProfessional):

    
    def issue_prescription(self):
        pass


class Nurse(HealthCareProfessional):

    pass


class Patient():

    global patients_list # access the global patients_list that conain all patients in list format
    obj_list = [] # Stores patients as objects

    def __init__(self,file_no,first_name,last_name, address='',phone='',doctor='') -> None:

        self.file_no = file_no
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.doctor = doctor
       
    def __str__(self):

        return self.first_name + ' ' + self.last_name

    def request_repeat(self):

        refill = Prescription("Amoxicillin",self,self.available_doctor,1,"500 mg 1 x 2 x 7")

        return refill
        

    def request_appointment(self,receptionist):

        request = receptionist.make_appointment(self)

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

    def __init__(self, urgent, staff, patient, date, time) -> None:

        self.urgent = urgent
        self.staff = staff
        self.patient = patient
        self.date = date
        self.time = time

    def __str__(self) -> str:
        return f'(Urgent = {self.urgent}) appointment for {self.patient.__str__()} on {self.date} at {self.time} (provider = {self.staff.__str__()})'


class Receptionist(Employee):

    def make_appointment(self,patient,nurse = False,urgent = False):
        if urgent:
            urgent_appointment = AppointmentSchedule.make_urgent_appointment(patient)
            return  urgent_appointment
        else:
            first_available = AppointmentSchedule.find_next_available(patient,nurse = False)
            return first_available


    def cancel_appointment(self):
        pass


class AppointmentSchedule():

    global today
    global doctors_appointments
    obj_list = [] # Stores appointments as objects

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
        end_date = start_date + datetime.timedelta(days = self.no_of_months * 30)

        while start_date < end_date:
            if start_date.weekday() not in [5,6]:
                while start_time < end_time:
                    schedule.append([start_time.date(),start_time.time(),''])
                    start_time += datetime.timedelta(minutes=30)
           
            start_date += datetime.timedelta(days=1)
            start_time = datetime.datetime(start_date.year,start_date.month,start_date.day,8,0,0)
            end_time = start_time + datetime.timedelta(hours =8)
                 
        doctors_appointments[f'{self.provider.__str__()}'] = schedule

        for provider in doctors_appointments.keys():
            list_to_csv(doctors_appointments[provider],f'appointments_schedule - Dr. {provider}')
  

    def add_appointment(cls,patient,doctor,date_time):
        pass

    def cancel_appointment(cls,patient,doctor,datetime):
        pass

    @classmethod
    def find_next_available(cls,selected_patient,nurse = False):

        appointment = None
        found = False
        selected_doctor = get_doctor(selected_patient)
        index = 0

        if nurse:
            for nurse in nurses_list:
                for appointment in nurses_appointments[nurse]:
                            if appointment[2]=='':
                                appointment = appointment[0],appointment[1]
                                found = True
                                selected_nurse = objects_to_list(Nurse,nurse)
                                return Appointment(selected_nurse,selected_patient,appointment[0],appointment[1],urgent= False), index

                            index += 1    
                    # If the appointment requested with any provider        
                
            if found == False:
                return None, selected_nurse

        else:

            for doctor in doctors_appointments:
                # If the appointment requested with a specific provider
            
                if doctor == selected_doctor.__str__():
                        for appointment in doctors_appointments[doctor]:
                            if appointment[2]=='':
                                appointment = appointment[0],appointment[1]
                                found = True
                                return Appointment(False, selected_doctor,selected_patient,appointment[0],appointment[1]), index
                            index += 1 
                    # If the appointment requested with any provider        
                
        if found == False:
            return None, selected_doctor

    @classmethod
    def make_urgent_appointment(cls,selected_patient):

        selected_doctor = get_doctor(selected_patient)
        date = today.replace(second=0,microsecond=0)
        time = doctors_appointments[selected_doctor.__str__()][0][1]

        
        if today.weekday() == 5:
            date = today + datetime.timedelta(days=2)
        elif today.weekday() == 6:
            date = today + datetime.timedelta(days=1)
            
        date = date.date()
        urgent_appointment = Appointment(True,selected_doctor,selected_patient,date, time)

        # Find the index of the urgent_appointment
        index = 0
        for appointment in doctors_appointments[selected_doctor.__str__()]:
            if appointment[0] == date.__str__() and appointment[1] == time.__str__():
                break
            index +=1
      

        return urgent_appointment, index

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
    
    options_string += "\033[93m-1:\033[0m To return to the previous menu \n\
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
    parameters:
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

    elif type(registree).__name__ =='Doctor':
        if not registree.employee_no:
            if not doctors_list:
                registree.employee_no ='1' 
            else:
                registree.employee_no = str(max(int(doctor[0]) for doctor in doctors_list) + 1)

    else:
        if not registree.employee_no:
            if not nurses_list:
                registree.employee_no ='1' 
            else:
                registree.employee_no = str(max(int(nurse[0]) for nurse in nurses_list) + 1)


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
                new_registree = Patient('','','','') # Registers a new patient
                registrees_list = patients_list

        registation_fields = get_registration_fields(new_registree)

        registreeType= registree_type.lower()
        print(f'Registering a new {registree_type}...\n')

        previous_menu = False
        # Each header will be used as a key for the user input during adding patient information
        headers_list  = [field for field in registation_fields if field not in ['file_no','employee_no']]
        for header in headers_list:
            header = header.replace('_', ' ').capitalize()
            if header in ['First name' ,'Last name']:
                input_item = input(f'{header}: ').strip()
                while not input_item.replace(' ','').isalpha() and input_item != '-1':
                    input_item = input(
                        f'\033[91mplease enter a valid {header} or enter -1 to go to previous menu: \033[0m').strip()

            elif header == 'Phone':
                # Make sure the entered phone number contains only digits
                input_item = input(f'{header}: ').strip()
                while not input_item.replace(' ','').isdigit() and input_item != '-1':
                    input_item = input(
                        f'\033[91mplease enter a valid {header} or enter -1 to go to previous menu: \033[0m').strip()

            elif header == 'Doctor':
                print('\nSelecting the doctor to register the patient with...\n')
                print_list(doctors_headers,doctors_list)
                print('') # A new line
                selected_provider = select_record(Doctor,doctors_list)
                print('') # A new line
                print(f'Dr. {selected_provider} was chosen')
                input_item = selected_provider.__str__()

            # If header == 'Address':
            else:
                input_item = input(f'{header}: ')
                
            input_item.strip()

            if input_item == "-1":
                previous_menu = True
                break
            else:
                input_dict[header] =(input_item.lower().title())

        # Check if there is duplicate name with the same first and last name
            if header == 'Last name':
                new_registree.first_name = input_dict['First name']
                new_registree.last_name = input_dict['Last name']
                duplicate, key = check_duplicate(new_registree,registrees_list)
              
                if duplicate:
                    print('') # A new line
                    print(f'\033[91mThis {registreeType} is already registered with a record no {key}\033[0m')
                    new_registree = None
                    break
        
        # If not duplicate, register that registree and add to the appropriate list
        if not duplicate and not previous_menu:
            print('') # A new line
            add_confirmation = input(
                '\033[96mSave the information above (Y/N)?: \033[0m')
            print('') # A new line

            if add_confirmation.lower() == 'y':
    
                if registree_type == 'Patient':
                    new_registree.address, new_registree.phone, new_registree.doctor =\
                         input_dict['Address'],input_dict['Phone'],input_dict['Doctor']

                register(new_registree)
                registrees_list.append((objects_to_list(new_registree)))
                new_registree = None    
                print('\033[92mThe record was saved successfully\033[0m')
                print('') # A new line
                input_item = input(
                    f'\033[96mHit enter to add {registreeType} patient or enter -1 to go to previous menu: \033[0m')
    
    # Save all objects data in the registree.obj_list to a csv file
    file_name = registree_type.lower() + 's_list'
    list_to_csv(registrees_list,file_name)


def edit_delete_interface():
    pass


def search_record_by_name(person_type,persons_list):
    '''Search a record from a list by first and/or last name'''

    def search_name(search_string,persons_list):
        '''Search a list for matching search_string.\n
search can be done by first name and/or last name partial or complete.
    '''

        search_results_list = [] 

        # If more than one search string:
        if len(search_string.split(' ')) > 1:

            first_name, last_name = search_string.split(' ')
            first_name = first_name.strip().lower()
            last_name = last_name.strip().lower()

            for person in persons_list:
                if person[1].lower().find(first_name) != -1 and person[2].lower().find(last_name) != -1:
                    search_results_list.append(person[0])
                else:
                    continue

        else:
            search_string = search_string.strip().lower()

            # loop through the list and append a record number for the records
            # whom first_name or last_name matches the search_string
            for person in persons_list:
                if person[1].lower().find(search_string) != -1 or person[2].lower().find(search_string) != -1:
                    search_results_list.append(person[0])
                else:
                    continue

        return search_results_list

    # Starts by searching a record
    search_string = input(
        "\033[96mSearch by first and/or last name partial/complete or enter -1 to go to main menu: \033[0m")

    if search_string == '-1':
        clear_screen()
        receptionist_interface()

    # If a match/es is/are found, print a filtered list:
    elif search_name(search_string,persons_list):
        search_result = search_name(search_string,persons_list)
        filteredlist = filtered_list(persons_list,search_result)
        clear_screen()
        if person_type == 'Patient':
            print_list(patients_headers,filteredlist)
        elif person_type == 'Doctor':
            print_list(doctors_headers,filteredlist)
        else:
            print_list(nurses_list,filteredlist)

        print('') # A new line

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

    
def select_record(type:Type,persons_list:list):
    '''select record by file/employee number'''
    
    file_no = input(
        '\033[96mPlease select using the record number: \033[0m')
    while not file_no.isdigit():
        try:
            int(file_no)
        except:
            file_no = input('\033[31mPlease enter a valid number: \033[0m')
            
        if file_no == '-1':
            break

        # Get the person_info that has the selected file/employee no.
    person_info = persons_list[
    int([person[0] for person in persons_list
    if person[0] == file_no][0])]

    return list_to_object(type,person_info)
            

def filtered_list(a_list: list,search_result:list):
    '''Filters a list based on the search_name function result '''

    filtered_list = [
            record for record in a_list if record[0] in search_result]

    return filtered_list

def generate_appointments_schedules():
    '''Generates appointments schedules by the receptionist'''
   
    print_list(doctors_headers, doctors_list)


    doctor = Doctor('1','Melanie','Alazzam')
    doctor_2 = Doctor('2','Mohammad','Atieh')
    appointments_schedule = AppointmentSchedule(doctor,1,5)
    appointments_schedule.generate_slots()



def appointments_interface():
    '''Interface for booking appointments for registered patients'''

    global patients_list, selected_doctor

    def select_provider():
        '''Schedule appointment with a doctor or a nurse'''

        # Select appointment with a nurse or a doctor
        options = ['Schedule appointment with a doctor','Schedule appointment with a nurse']
        menu_selection = menu(options)

        provider_type = ''
        if menu_selection == '1' :
            print_list (doctors_headers,doctors_list)
            selected_provider = select_record(Doctor,doctors_list)
                
        elif menu_selection == '2' :
            print_list(nurses_headers, nurses_list)
            selected_provider = select_record(Nurse,nurses_list)
            
        return selected_provider

   
    print_list(patients_headers)
    print('') # A new line

    # Search a record by name
    search_record_by_name('Patient',patients_list)
    # Options after selecting the patient
    mode_selection = menu(['Book Regular Appointment','Book Urgent Appointment','Cancel Appointment'])
    while mode_selection != '-1':
            # If first option is selected:
            if mode_selection == "1":
                selected_patient = select_record(Patient,patients_list)
                selected_provider = select_provider()

                
         # If Book Urgent Appointment is selected:
            elif mode_selection == "2":
                pass

            elif mode_selection == "0":
                quit_application()
            #If cancel appointment is selected:
            # elif mode_selection == "3":
            #     print('') # A new line
                # file_no = input(
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

            

        # clear_screen()
        # main_screen()

 
def get_doctor(selected_patient):
    '''Gets doctor object from patient information'''

    provider_first_name, provider_last_name = selected_patient.doctor.split(' ')
    provider_index = [doctors_list.index(doctor) for doctor in doctors_list if doctor[1] == provider_first_name and doctor[2] == provider_last_name][0]
    selected_doctor = list_to_object(Doctor,doctors_list[provider_index])

    return selected_doctor

    
def receptionist_interface():
    '''Receptionist interface for registering patients_list, assigning them
     to doctors_list, and booking appointments
     '''
   
    while True:

        clear_screen()
        options = ['Register Patients','Book Appointment / Request Repeat','Edit/Delete Patients','Generate Appointments Schedules','TEST APPOINTMENT']
        menu_selection = menu(options)

        if menu_selection == '1' :
            clear_screen()
            registration_interface('Patient',patients_list)

        if menu_selection == '2' :
            appointments_interface()

        if menu_selection == '3' :
            edit_delete_interface()

        if menu_selection == '4' :
            generate_appointments_schedules()

        if menu_selection == '5' :
            selected_patient = Patient('1','Mohammad','Atieh','','','Melanie Alazzam')
            selected_patient.request_appointment(receptionist)
            print(AppointmentSchedule.find_next_available(selected_patient)[0].__str__(),AppointmentSchedule.find_next_available(selected_patient)[1])
            print(AppointmentSchedule.make_urgent_appointment(selected_patient)[0].__str__(),AppointmentSchedule.make_urgent_appointment(selected_patient)[1])
            input('Test checkpoint')
        
        elif  menu_selection == '-1' :
            break

    clear_screen()
    main_screen()


def register_doctors():
    pass


def register_nurses():
    pass

def administration_interface():
    '''Administration interface for adding healthcare providers to the clinic'''

    while True:

        options = ['View Registered Doctors/Nurses','Add doctors to the clinic','Add nurses to the clinic']
        menu_selection = menu(options)

        if menu_selection == '1':
            
            print('Registered Doctors\n')
            print_list(doctors_headers,doctors_list)
            print('\nRegistered Nurses\n')
            print_list(doctors_headers,doctors_list)
            administration_interface()
                
        elif menu_selection == '2' :
            clear_screen()
            registration_interface('Doctor',doctors_list)

        elif menu_selection == '3' :
            clear_screen()
            registration_interface('Nurse',doctors_list)

        elif menu_selection == '-1':
            break

        else:
            quit_application()

    clear_screen()
    main_screen()


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

    file_names = ['patients_list','doctors_list','nurses_list']
    registrees_lists = [patients_list,doctors_list,nurses_list]
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

def import_schedules_from_cv():
    '''Imports appointment schedules from csv files'''

    os.getcwd()
    file_names = []
    temp_schedule = []
    appointment_schedule = [doctors_appointments,nurses_appointments]

    for schedule in appointment_schedule:

        for file in list(glob.glob('appointments_schedule*')):
            file_names.append(file)

        schedule.clear()

        for file in file_names:
            
            file = os.getcwd() + f'/{file}'   
            with open(file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        temp_schedule.append(row)
            provder_name = os.path.basename(file).replace('.csv','').replace('appointments_schedule - Dr. ','')
            schedule[provder_name] = temp_schedule
            temp_schedule = []
       

def quit_application():
    '''Clears screen, print Good Bye!
    and quit the application
    '''
    clear_screen()
    print('\033[92mGood Bye!\033[0m')
    quit()

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
       import_schedules_from_cv()
       main_screen()
   
    elif main_menu == '2':
        receptionist_interface()

    elif main_menu == '5':
        clear_screen()
        administration_interface()

    elif main_menu in ['0', '-1']:
        quit_application()

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
        import_from_cv() # Import saved Patients, Doctors and Nurses
        import_schedules_from_cv() # Import saved AppointmentSchedules
        receptionist = Receptionist(1,'Veronica','Reborts')
        main_screen()
       
    

    