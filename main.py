# imports
from asyncio import selector_events
import copy
from curses import erasechar
import datetime
from email.headerregistry import DateHeader
import os
import csv
from xmlrpc.client import DateTime


import test_main
from test_main import *
import glob


### Global Variables ###

patients_list = [] # Stores patients data in a list format
doctors_list = [] # Stores doctors data in a list format
nurses_list = [] # Stores nurses data in a list format
receptionist = None # Stores the default receptionist that is initialized when the application runs
prescriptions_list = [] # Stores al the prescription details
consultations_list = [] # Stores all the consultation details
doctors_appointments = {} # Stores doctors appointments
nurses_appointments = {} # Stores nurses appointments

skip_index = None # Stores the index of the next available appointment to enable finding the following one
today = datetime.datetime.today().date()
now = datetime.datetime.now().time().replace(second=0,microsecond=0)
  

# Headers to be used for printing tables
patients_headers = ['File No.','First Name','Last Name','Address                ','Phone    ','Doctor     ']
doctors_headers =['Employee Number','Fist Name','Last Name']
nurses_headers =['Employee Number','Fist Name','Last Name']
appointments_headers = ['Appointment No.','Date','Time','File No.',"Patient's Name","(Urgent) File No.",'(Urgent) Name']
prescription_headers = ['Prescription No.','Date','Time',"Patient's Name",'Type','Quantity','Dosage',"Doctor's Name"]
consultations_headers = ['Consultation No.','Date','Time','File No.',"Patient's Name",'Consultation Details                    ']

### End of Global Variables ###

class RegisteredPatientsLimit(Exception):
    
    pass

class Employee():
    '''Creates an Employee that is a superclass for HealthCareProfessional and Receptionist
    Attributes: employee_no: str,first_name: str,last_name:str
    '''
    obj_list = [] # Stores employees as objects

    def __init__(self,employee_no: str,first_name: str,last_name:str) -> None:
        self.employee_no= employee_no
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):    
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return self.first_name + ' ' + self.last_name


class HealthCareProfessional(Employee):
    '''Creates a HealthCareProfessional that inherits from Employee
    Inherited attributes: employee_no: str,first_name: str,last_name:str
    Methods: consultation()
    '''
    
    def consultation(self):

        global consultations_list
        # Show only patients registered with the selected_provider
        own_patients = [patient for patient in patients_list if patient[-1]==str(self)]  
        print_list(patients_headers, own_patients)
        # Select patient by searching the name then selecting file no  
        search_result = search_record_by_name(Patient,own_patients)
        selected_patient = select_record(Patient,search_result)
        
        consult_details = message('blue','Write your consultation details',space_before = True)
        consultation_details = [today,now,selected_patient.file_no,str(selected_patient),str(self),consult_details]

        if not consult_details:
            consultation_details = ['1'] + consultation_details

        else:
            consultation_details = [len(consultations_list)] + consultation_details
            
        consultations_list.append(consultation_details)
        list_to_csv(consultations_list,'consultations_list')
        clear_screen()

        return consultation_details

   
class Doctor(HealthCareProfessional):    
    '''Creates a Doctor that inherits from HealthCareProfessional
    Inherited attributes: employee_no: str,first_name: str,last_name:str
    Inherited Methods: consultation()
    Methods: issue_prescription()
    '''
    
    def issue_prescription(self, prescription = None):
        '''Issues a new prescription or a repeat prescription after being
        forwarded by a receptionist
        '''

        global prescriptions_list

        # If the prescription argument == None, this means it is a new prescription 
        if not prescription:

            # Show only patients registered with the selected_provider
            own_patients = [patient for patient in patients_list if patient[-1]==str(self)]  
            print_list(patients_headers, own_patients)
            # Select patient by searching the name then selecting file no  
            search_result = search_record_by_name(Patient,own_patients)
            selected_patient = select_record(Patient,search_result)

            # Get the prescription details from the doctor
            add_another = None
            while True:
                if add_another == '':
                    break

                type = message('white','Drug name').capitalize()
                quantity = message('white','Quantity')
                dosage = message('white','Dosage')
                new_prescription = Prescription(today,now,selected_patient,type,quantity,dosage,self)
                new_prescription_info = object_to_list(new_prescription)

                # Append the prescription to the prescriptions_list
                if not prescriptions_list:
                    new_prescription_info = ['1'] + object_to_list(new_prescription)

                else:
                    new_prescription_info = [len(prescriptions_list)+1] + object_to_list(new_prescription)
                    prescriptions_list.append(new_prescription_info)

                add_another = message('blue',"Hit enter to save or enter 'a' to add another prescription")

        # If the prescription argument != None, this means it is a repeat prescription
        else:
            new_prescription = Prescription(today,now,prescription.patient,prescription.type,prescription.quantity,prescription.dosage,self)
            new_prescription_info = [len(prescriptions_list)+1] + object_to_list(new_prescription)
            prescriptions_list.append(new_prescription_info)
            
        # Save prescriptions to a csv file 
        list_to_csv(prescriptions_list,'prescriptions_list')
        clear_screen()
        
        return new_prescription


class Nurse(HealthCareProfessional):
    '''Creates a Nurse that inherits from HealthCareProfessional
    Inherited attributes: employee_no: str,first_name: str,last_name:str
    Inherited Methods: consultation()
    '''
    pass


class Patient():
    '''Creates a patient object
    Attributes: file_no: str,first_name: str,last_name: str, address: str ='',phone :str ='',doctor: str=''
    methods: request_appointment(), request_repeat()
    '''

    global patients_list # access the global patients_list that contains all patients in list format
    obj_list = [] # Stores patients as objects

    def __init__(self,file_no: str,first_name: str,last_name: str, address: str ='',phone :str ='',doctor: str='') -> None:
        self.file_no = file_no
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.doctor = doctor
       
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return self.first_name + ' ' + self.last_name
        
    def request_appointment(self,nurse = False, urgent = False):
        request = receptionist.make_appointment(self,nurse,urgent)
        return request

    def request_repeat(self):
        prescription_repeat = receptionist.forward_repeat_request(self)
        return prescription_repeat

        
class Prescription():
    '''Creates a Prescription object
Attributes: type: str,patient: Patient,doctor: Doctor,quantity: int,dosage: float
    '''

    global prescriptions_list # access the global prescriptions_list that contains all prescriptions in list format
    obj_list = [] # Stores prescriptions as objects
    def __init__(self,date:datetime.date, time: datetime.time,patient: Patient, type: str,quantity: str,dosage: str,doctor: Doctor) -> None:

        self.date = date
        self.time = time
        self.patient = patient
        self.type = type
        self.quantity = quantity
        self.dosage = dosage
        self.doctor = doctor

    def __str__(self) -> str:

        return f'Patient: {self.patient.name}, Type: {self.type}, Dosage: {self.dosage}, Quantity: {self.quantity}'


class Appointment():
    '''Creates an appointment object
    Attributes: urgent:bool, staff:HealthCareProfessional, patient: Patient, date: datetime.date, time: datetime.time
    '''

    def __init__(self, urgent:bool, staff:HealthCareProfessional, patient: Patient, date: datetime.date, time: datetime.time) -> None:

        self.urgent = urgent
        self.staff = staff
        self.patient = patient
        self.date = date
        self.time = time

    def __repr__(self) -> str:
        return f'(Urgent = {self.urgent}) appointment for {self.patient.__str__()} on {self.date} at {self.time} (provider = {self.staff.__str__()})'


class Receptionist(Employee):
    '''Creates a receptionist object
    Attributes: patient,nurse = False,urgent = False
    Inherited attributes: 
    methods: make_appointment(), cancel_appointment()
    '''

    def make_appointment(self, selected_patient, nurse, urgent):
        '''Schedules patient appointments with doctors and nurses by the receptionist'''

        if urgent:
            urgent_appointment = AppointmentSchedule.make_urgent_appointment(selected_patient)
            return  urgent_appointment
        
        if nurse:
            next_available = AppointmentSchedule.find_next_available(selected_patient,nurse = True)
            return next_available

        else:
            next_available = AppointmentSchedule.find_next_available(selected_patient,nurse = False)
            return next_available


    def cancel_appointment(self,appointment_index = None,provider = None):
        '''Cancels patient appointment by the receptionist'''

        if not provider:
            selected_provider = view_appointments()
            print('') # A new line

        else:
            selected_provider = provider
        
        if not appointment_index:
            selected_appointment_index = select_record(Appointment,doctors_appointments[str(selected_provider)])
            
        else:
            selected_appointment_index = appointment_index


        if selected_appointment_index == None:
            receptionist_interface()

        # Find the selected appointment in the doctors_appointments
        selected_appointment = doctors_appointments[f'{str(selected_provider)}'][selected_appointment_index]
        if selected_appointment[5] != '':
            selected_option = menu(['Regular appointment','Urgent appointment','both'],False)
            if selected_option == '1':
                for index in range(3,5):
                    selected_appointment[index] = selected_appointment[index+2]
                    selected_appointment[index+2] = ''

            elif selected_option =='2':
                for index in range(5,7):
                    selected_appointment[index] = ''

            else:
                for index in range(3,7):
                    selected_appointment[index] = ''
        else:
            for index in range(3,5):
                    selected_appointment[index] = ''

        list_to_csv(doctors_appointments[str(selected_provider)],f'appointments_schedule - Dr. {str(selected_provider)}')

    def forward_repeat_request(self):
        '''Forwards a prescription repeat for the patient to his doctor by the receptionist'''
        
        print_list(patients_headers,patients_list)
        search_result = search_record_by_name(Patient,patients_list)
        selected_patient = select_record(Patient,search_result)

        repeat_another = 'a'
        while repeat_another == 'a':      
            if selected_patient != None:
                selected_doctor_info = [doctor for doctor in doctors_list if (doctor[1] + ' ' + doctor[2]) == selected_patient.doctor][0]
                selected_doctor = list_to_object(Doctor, selected_doctor_info)
                patient_prescriptions = [prescription for prescription in prescriptions_list if prescription[3] == str(selected_patient)]
                print('') # A new line
                print_list(prescription_headers,patient_prescriptions)
                selected_prescription = select_record(Prescription,patient_prescriptions,selected_doctor)
                selected_doctor.issue_prescription(selected_prescription)

            repeat_another = message('blue',"Please enter 'a' to repeat another prescription or hit enter to go to the previous menu",space_before=True)
               

class AppointmentSchedule():
    '''Creates an AppointmentSchedule object
    Attributes: provider:HealthCareProfessional,no_of_months:int,hours_per_day:int
    methods: generate_slots(), add_appointment(), find_next_available(), make_urgent_appointment()
    '''
    global today, doctors_appointments
    obj_list = [] # Stores appointments as objects

    def __init__(self,provider:HealthCareProfessional,no_of_months:int,hours_per_day:int) -> None:
        self.provider = provider
        self.no_of_months = no_of_months
        self.hours_per_day = hours_per_day if hours_per_day <= 12 else 12 # Maximum working hours are from 8:00 am to 8:00 pm
    

    def generate_slots(self):
        '''Generates 30-minute appointments slots according to 
        the no_of_months and the hours_per_day attributes
        '''
        schedule = [] 
        start_date = today
        start_time = datetime.datetime.today().replace(hour = 8, minute =0,second=0,microsecond=0)
        health_care_professional = self.provider

        if isinstance(health_care_professional,Doctor):
            appointments_list = doctors_appointments
        else:
            appointments_list = nurses_appointments

        # If there appointment slots already in the doctor_appointments[provider] list 
        # get the last appointment slot and the length of the list to continue the numbering of the slots 
        index = 0
        if appointments_list.get(f'{self.provider}'):
            index = len(appointments_list[f'{self.provider}'])
            last_appointment_slot = appointments_list[f'{self.provider}'][index-1][1] + " " + appointments_list[f'{self.provider}'][index-1][2]
            start_time = datetime.datetime.strptime(last_appointment_slot,'%d-%m-%Y %H:%M') + datetime.timedelta(minutes = 30)
            start_date = datetime.datetime.strptime(last_appointment_slot,'%d-%m-%Y %H:%M').date()
        
        start_time_fixed = str(start_time)[:-3] # Review
        end_time = start_time.replace(hour= 8 + self.hours_per_day)
        end_date = start_date + datetime.timedelta(days = self.no_of_months * 30)

   
        while start_date < end_date:
            if start_date.weekday() not in [5,6]:
                while start_time < end_time:
                    m_d_y_date_format = start_time.strftime('%d-%m-%Y')
                    schedule.append([index,m_d_y_date_format,str(start_time.time())[:-3],'','','',''])
                    start_time += datetime.timedelta(minutes=30)
                    index +=1
           
            start_date += datetime.timedelta(days=1)
            start_time = datetime.datetime(start_date.year,start_date.month,start_date.day,8,0,0)
            end_time = start_time + datetime.timedelta(hours =8)
                 
        try:
            appointments_list[f'{self.provider}'] += schedule
        except:
            appointments_list[f'{self.provider}'] = schedule

        if isinstance(self.provider,Nurse):
            for provider in nurses_appointments.keys():
                if provider == str(self.provider):
                    list_to_csv(appointments_list[provider],f'appointments_schedule - {provider}')   

        else:
            for provider in appointments_list.keys():
                if provider == str(self.provider):
                    list_to_csv(appointments_list[provider],f'appointments_schedule - Dr. {provider}')
            
           
    @classmethod
    def find_next_available(cls,selected_patient,nurse = False):
        '''Finds next available appointment on the doctor's schedule
        with whom the patient is registered.
        Returns
        '''
        appointment = None
        found = False # True means an appointment match was found
        selected_doctor = get_doctor(selected_patient)
        index = 0

        def get_next_appointment(selected_provider,selected_patient,appointment):
            '''A helper function for the find_next_available()'''

            global skip_index
            if skip_index == None:
                if appointment[3]=='':
                    fist_available = appointment[1],appointment[2]
                    skip_index = index      
                    return Appointment(False, selected_provider,selected_patient,fist_available[0],fist_available[1]), index
            else:
                if appointment[3]=='' and int(appointment[0]) > skip_index:
                    fist_available = appointment[1],appointment[2]
                    skip_index = index      
                    return Appointment(False, selected_provider,selected_patient,fist_available[0],fist_available[1]), index
                                  

        # If an appointment with a nurse is chosen
        if nurse:
            for nurse in nurses_list:
                nurse_name = (nurse[1]+ ' ' + nurse[2])
                selected_nurse = list_to_object(Nurse,nurse)  
                # Check if appointments schedule is available first       
                if nurses_appointments.get(nurse_name):
                    for appointment in nurses_appointments[nurse_name]:
                        candidate_time = datetime.datetime.strptime(appointment[2],'%H:%M').time()
                        candidate_date = datetime.datetime.strptime (appointment[1],'%d-%m-%Y').date()
                         # If current time < candidate_time &  current date <= candidate_date, return the first free appointment slot
                        if now < candidate_time:
                            if today <= candidate_date:
                                appointment_match = get_next_appointment(selected_nurse,selected_patient,appointment)
                                if appointment_match:
                                    return appointment_match
                        # If current time > candidate_time &  current date < candidate_date, return the first free appointment slot   
                        # This condition avoids returning appointment at a time that is before the time of request   
                        elif now > candidate_time:
                                if today < candidate_date:
                                    appointment_match = get_next_appointment(selected_nurse,selected_patient,appointment)
                                    if appointment_match:
                                        return appointment_match
                                
                        index += 1
                
                else:
                    print('''Please generate nurse appointments schedules from the reception \n
module before scheduling appointments''')
                            
            if found == False:
                return None
        # If an appointment with a doctor is chosen
        else:
            for doctor in doctors_appointments:
                # Check if appointments schedule is available first
                if doctors_appointments.get(doctor):
                    if doctor == str(selected_doctor):
                        for appointment in doctors_appointments[doctor]:
                            candidate_time = datetime.datetime.strptime(appointment[2],'%H:%M').time()
                            candidate_date = datetime.datetime.strptime (appointment[1],'%d-%m-%Y').date()
                            # If current time < candidate_time &  current date <= candidate_date, reserve the free appointment slot
                            if now < candidate_time:
                                if today <= candidate_date:
                                    appointment_match = get_next_appointment(selected_doctor,selected_patient,appointment)
                                    if appointment_match:
                                        return appointment_match
                             # If current time > candidate_time &  current date < candidate_date, reserve the free appointment slot
                            elif now > candidate_time:
                                if today < candidate_date:
                                    appointment_match = get_next_appointment(selected_doctor,selected_patient,appointment)
                                    if appointment_match:
                                        return appointment_match
                                   
                            index += 1
                
                else:
                    print('''Please generate doctor appointments schedules from the reception \n
module before scheduling appointments''')
                        
            if found == False:
                return None, selected_doctor


    @classmethod
    def add_appointment(cls,appointment: Appointment, index:int):
        '''Adds a confirmed appointment to the doctors_appointments schedule'''

        selected_provider = appointment.staff
        selected_patient = appointment.patient
        urgent_appointment = appointment.urgent # Returns True if urgent appointment

        if isinstance(selected_provider,Doctor):
            schedule = doctors_appointments
        else:
            schedule = nurses_appointments
        
        for provider in schedule:
            if provider == str(selected_provider):
                for appointment_option in schedule[provider]:
                    if int(appointment_option[0]) == index:
                        if urgent_appointment:
                            # If the appointment slot is empty, reserve it:
                            if schedule[provider][index][3] == '':
                                schedule[provider][index][3] = selected_patient.file_no
                                schedule[provider][index][4] = selected_patient
                            # If the appointment slot is not empty, double book because it is urgent 
                            else:
                                schedule[provider][index][5] = selected_patient.file_no
                                schedule[provider][index][6] = selected_patient
                        else:
                            schedule[provider][index][3] = selected_patient.file_no
                            schedule[provider][index][4] = selected_patient

        # Modify the appointments_schedule - <Dr./> <provider>.csv
        if isinstance(selected_provider,Doctor):
            list_to_csv(schedule[str(selected_provider)],f'appointments_schedule - Dr. {str(selected_provider)}')

        else:
            list_to_csv(schedule[str(selected_provider)],f'appointments_schedule - {str(selected_provider)}')

        return appointment


    @classmethod
    def make_urgent_appointment(cls,selected_patient):
        '''Arranges urgent appointment by double booking a maximum of one patient\n
        per each appointment slot that is already booked.
        '''
        selected_doctor = get_doctor(selected_patient)
        date = today
        m_d_y_today_format = date.strftime('%d-%m-%Y')
        found = False
        
        # Urgent appointment day should be on the same day 
        # unless it is a weekend day
        if today.weekday() == 5:
            date = today + datetime.timedelta(days=2)

        elif today.weekday() == 6:
            date = today + datetime.timedelta(days=1)
        

        def time_difference(candidate_time, now):
            '''Returns True if the time difference between the current time and\n
            a candidate appointment time is at least 30 minutes (1800 seconds).\n
            It is used for the purpose of scheduling urgent appointments.
            '''
            temp_candidate_time = datetime.datetime(1900,1,1,candidate_time.hour,candidate_time.minute)
            temp_now = datetime.datetime(1900,1,1,now.hour,now.minute)
            difference = (temp_candidate_time - temp_now).seconds
            if difference > 1800:
                return True
            else:
                return False
            

        # Find the nearest available appointment and return it with it's index in 
        # the doctors_appointments[provider] list
        index = 0
        for appointment in doctors_appointments[str(selected_doctor)]:
            candidate_date = appointment[1]
            candidate_time = datetime.datetime.strptime(appointment[2],'%H:%M').time()
           
            # If the current time is > clinic end time, check next day's nearest available slot
            if candidate_date == m_d_y_today_format and date == today:
                if candidate_time > now and time_difference(candidate_time,now):
                    if appointment[5] != '':
                        index +=1
                        continue

                    # If there is no another urgent appointment at the same slot 
                    # reserve the slot and exit the loop
                    else:
                        found = True
                        break 
            
            elif candidate_date == m_d_y_today_format and date > today:
                # If there is already another urgent appointment at the same time 
                # skip to the next available slot (only one urgent appointment at a time slot is allowed)
                if appointment[5] != '':
                    index +=1
                    continue

                # If there is no another urgent appointment at the same slot 
                # reserve the slot and exit the loop
                else:
                    found = True
                    break

            
        if found:
            urgent_appointment = Appointment(True,selected_doctor,selected_patient,candidate_date, candidate_time)
            return urgent_appointment, index
        else:
            return None

### Functions ###

def print_list(headers, list = patients_list):
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

def message(color,message,space_before = False, space_after = False):
    '''Prints a custom message and returns user's input'''

    if color == 'red':
        foreground = '91'

    elif color == 'blue':
        foreground = '96'

    elif color == 'green':
        foreground = '92'

    else:
        foreground = '0' # White


    if space_before:
        print('')
    response = input(f'\033[{foreground}m{message}: \033[0m')
    if space_after:
        print('')
    return response

def menu(options,last_two = True):
    '''Generates CLI menus
    parameters:
    options: desired menu options
    '''
    print('') # A new line
    options_string = "\033[96mPlease select one of the options below:\033[0m\n\n"
    choice_number = 1
    for option in options:
        options_string += f"\033[93m {choice_number}:\033[0m {option}\n"
        choice_number +=1
    
    if last_two:
        options_string += "\033[93m-1:\033[0m To return to the previous menu \n\
\033[93m 0:\033[0m Quit\n\n\
 > "

    menu_selection = input(options_string)

    return menu_selection



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
                file_no = str(max(int(patient[0]) for patient in patients_list) + 1)
                if int(file_no) <= 500:
                    registree.file_no = file_no
                else:
                    raise RegisteredPatientsLimit
                
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


def registration_interface(registree_type: object,registrees_list: list):
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
            if registree_type == Doctor:
                new_registree = Doctor('','','') # Registers a new doctor  
                registrees_list = doctors_list

            elif registree_type == Nurse:
                new_registree = Nurse('','','') # Registers a new doctor
                registrees_list = nurses_list
        
            elif registree_type == Patient:
                new_registree = Patient('','','','') # Registers a new patient
                registrees_list = patients_list

        registration_fields = get_registration_fields(new_registree)

        registreeType= registree_type.lower()
        print(f'Registering a new {registree_type}...\n')

        previous_menu = False
        # Each header will be used as a key for the user input during adding patient information
        headers_list  = [field for field in registration_fields if field not in ['file_no','employee_no']]
        for header in headers_list:
            header = header.replace('_', ' ').capitalize()
            if header in ['First name' ,'Last name']:
                input_item = message('white',f'{header}: ').strip()
                while not input_item.replace(' ','').isalpha() and input_item != '-1':
                    input_item = message(
                        'red',f'please enter a valid {header} or enter -1 to go to previous menu: ').strip()

            elif header == 'Phone':
                # Make sure the entered phone number contains only digits
                input_item = message('white',f'{header}: ').strip()
                while not input_item.replace(' ','').isdigit() and input_item != '-1':
                    input_item = message(
                        'red',f'please enter a valid {header} or enter -1 to go to previous menu: ').strip()

            elif header == 'Doctor':
                print('\nSelecting the doctor to register the patient with...\n')
                print_list(doctors_headers,doctors_list)
                print('') # A new line
                selected_provider = select_record(Doctor,doctors_list)
                print('') # A new line
                print(f'Dr. {selected_provider} was chosen')
                input_item = str(selected_provider)

            # If header == 'Address':
            else:
                input_item = message('white',f'{header}: ')
                
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
            add_confirmation = message(
                'green','Save the information above (Y/N)?: ',space_after=True,space_before=True)
         
            if add_confirmation.lower() == 'y':
    
                if registree_type == 'Patient':
                    new_registree.address, new_registree.phone, new_registree.doctor =\
                         input_dict['Address'],input_dict['Phone'],input_dict['Doctor']

                try:
                    register(new_registree)
                    registrees_list.append((object_to_list(new_registree)))
                    new_registree = None    
                    print('\033[92mThe record was saved successfully\033[0m')
                    input_item = message(
                    'blue', f'Hit enter to add {registreeType} patient or enter -1 to go to previous menu: ')

                except RegisteredPatientsLimit:
                    print('\033[91mA maximum number of 500 patients can be registered for each doctor\033[0m')
    
    # Save objects data to a csv file
    file_name = registree_type.lower() + 's_list'
    list_to_csv(registrees_list,file_name)


def edit_delete_interface():
    pass


def search_record_by_name(person_type: object,persons_list:list):
    '''Searches records from a list by first and/or last name, and prints
    and returns filtered list
    '''

    def search_name(search_string,persons_list):
        '''A helper function for search_record_by_name(). It searches a list for matching \n
         search_string. search can be done by first name and/or last name partial or complete.
    '''

        search_result = [] 

        # If more than one search string:
        if len(search_string.split(' ')) > 1:
            search_string = search_string.strip()
            first_name, last_name = search_string.split(' ')
            first_name = first_name.strip().lower()
            last_name = last_name.strip().lower()

            for person in persons_list:
                if person[1].lower().find(first_name) != -1 and person[2].lower().find(last_name) != -1:
                    search_result.append(person[0])
                else:
                    continue

        else:
            search_string = search_string.strip().lower()

            # loop through the list and append a record number for the records
            # whom first_name or last_name matches the search_string
            for person in persons_list:
                if person[1].lower().find(search_string) != -1 or person[2].lower().find(search_string) != -1:
                    search_result.append(person[0])
                else:
                    continue

        return search_result


    def filtered_list(a_list: list,search_result:list):
        '''A helper function for Search_record_by_name().\n
         It filters a list based on the search_name function result
         '''

        filtered_list = [
                record for record in a_list if record[0] in search_result]

        return filtered_list
  
    # Starts by searching a record
    search_string = message(
     'blue', "Search by first and/or last name partial/complete or enter -1 to go to main menu: ",space_before=True)

    if search_string == '-1':
        clear_screen()
        receptionist_interface()

    # If a match/es is/are found, print a filtered list:
    elif search_name(search_string,persons_list):
        search_result = search_name(search_string,persons_list)
        filteredlist = filtered_list(persons_list,search_result)
        clear_screen()
        if person_type == Patient:
            print_list(patients_headers,filteredlist)
        elif person_type == Doctor:
            print_list(doctors_headers,filteredlist)
        else:
            print_list(nurses_list,filteredlist)

        return filteredlist

     # If there is no match found:
    else:
        what_next = message(
            'red','No match was found hit enter to try again or enter -1 to go to main menu: ',space_after=True,space_before=True)
        if what_next == '-1':
            clear_screen()
            main_screen()

        else:
            appointments_interface()

    
def select_record(type: object, objects_list:list,doctor=None):
    '''select record by file/employee number'''

    file_no = message(
        'blue','Select a record number or enter -1 to go to the previous menu: ',space_before=True).strip()
    while not file_no.isdigit() and file_no != '-1':
        try:
            int(file_no)
        except:
            file_no = message('red''Please enter a valid number: ')
        
    while file_no not in [item[0] for item in objects_list]:
        if file_no == '-1':
            return None
        else:
            file_no = message('red','Please enter one of the record numbers above: ').strip()

    object_info = [item for item in objects_list
    if item[0] == file_no][0]

    if type == Appointment :
        object_index = objects_list.index(object_info)
        return object_index

    elif type == Prescription:
        object_info = object_info[1:]
        return Prescription(*object_info)

    else:
        return list_to_object(type,object_info) 
            

def generate_appointments_schedules():
    '''Generates appointments schedules by the receptionist'''
   
    selected_option = menu(['Generate Schedules for Doctors','Generate Schedules for Nurses'])
    if selected_option == "1":

        print_list(doctors_headers, doctors_list)
        selected_provider = select_record(Doctor,doctors_list)
    
    else :
        print_list(nurses_headers, nurses_list)
        selected_provider = select_record(Nurse,nurses_list)


    no_of_months = message(
        'blue','Select enter the length of the schedule in months: ')

    while not no_of_months.isdigit():
        no_of_months = message(
       'red','Please enter a whole number: ')

    hour_per_day = message(
        'blue','Select enter the number of daily working hours / day of the schedule in months: ')

    
    while not hour_per_day.isdigit():
        hour_per_day = message(
        'red','\033[96mPlease enter a whole number: ')
        

    appointments_schedule = AppointmentSchedule(selected_provider,int(no_of_months),int(hour_per_day))
    appointments_schedule.generate_slots()
   

def appointments_interface():
    '''Interface for booking appointments for registered patients'''

    global patients_list, skip_index
    next_available = None
    confirm_appointment = None

    clear_screen() 
    print_list(patients_headers)
    print('') # A new line

    # Search a record by name
    search_result = search_record_by_name(Patient,patients_list)
    selected_patient = select_record(Patient,search_result)
    # Options after selecting the patient
    while selected_patient != None:
        mode_selection = menu(['Book Regular Appointment','Book Urgent Appointment','Book Appointment with a Nurse'])
        while mode_selection != '-1':
            # To book regular appointment (first available):
            if mode_selection == "1":
                while confirm_appointment in ['n',None]:  
                    next_available = selected_patient.request_appointment()
                    if next_available[0] == None:
                        what_next = message('red','''Please generate appointments schedule from the administration module first.
Hit enter to go there:''')
                        if what_next == '':
                            clear_screen()
                            administration_interface()

                    print(f'Next available appointment is on {next_available[0].date} at {next_available[0].time}')
                    confirm_appointment = message('blue',"Please hit enter to select this appointment or \
'n' for another alternative: ")

                message('blue',"Please hit enter to confirm: ")
                AppointmentSchedule.add_appointment(*next_available)
                what_next = message('green','''The appointment was added successfully, hit enter to schedule for another patient
or -1 to go back to the receptionist menu: ''')
                if what_next == '-1':
                    receptionist_interface()
                skip_index = None
                appointments_interface()
            
            # To book ugent Appointment (same day or earliest even
            # if no space is available on the regular schedule):
            elif mode_selection == "2":
                    urgent_appointment = selected_patient.request_appointment(urgent=True)
                    if urgent_appointment:
                        print(f'First urgent appointment is on {urgent_appointment[0].date} at {urgent_appointment[0].time}')
                        confirm_appointment = message('blue','Hit enter if you want to confirm the appointment: ')
                        if confirm_appointment == '':
                            AppointmentSchedule.add_appointment(*urgent_appointment)
                        what_next = message('green','''The appointment was added successfully, hit enter to schedule for another patient
or -1 to go back to the receptionist menu: ''')
                        if what_next == '-1':
                            receptionist_interface()
                    else:
                        message('red','''No appointments are available, please generate appointment slots\n
using the receptionist menu. Hit enter to go there: ''')
                    receptionist_interface()

            # To book appointment with a nurse
            elif mode_selection == "3":
                while confirm_appointment in ['n',None]:
                    next_available = selected_patient.request_appointment(nurse=True)
                    if next_available == None:
                        what_next = message('red','''Please generate appointments schedule from the receptionist module first.
Hit enter to go there:''')

                        if what_next == '':
                            clear_screen()
                            administration_interface()
                    
                    print(f'Next available appointment is on {next_available[0].date} at {next_available[0].time}')
                    confirm_appointment = message('blue',"Please hit enter to select this appointment or \
'n' for another alternative: ")
                    if confirm_appointment == '':
                        AppointmentSchedule.add_appointment(*next_available)
                        what_next = message('green','''The appointment was added successfully, hit enter to schedule for another patient
or -1 to go back to the receptionist menu: ''')
                        if what_next == '-1':
                            receptionist_interface()

                skip_index = None
                appointments_interface()
                        

            elif mode_selection == "0":
                quit_application()

            elif mode_selection == '':
                clear_screen()
                print_list(patients_headers)
                print('') # A new line
                appointments_interface()

            else:
                mode_selection = message(
                    'red','Please enter a valid selection mode: ')

        appointments_interface()
        
def view_appointments(preselected_provider = None):

    if not preselected_provider:
        print_list(doctors_headers,doctors_list)
        print('') # A new line
        selected_provider = select_record(Doctor,doctors_list)

    else:
        selected_provider = preselected_provider

    if selected_provider != None:
        appointments = [appointment for appointment in doctors_appointments[str(selected_provider)]if
        appointment[3] != '' ]
        print('') # A new line
        print(f"Dr. {str(selected_provider)}'s Appointments")
        print('') # A new line
        print_list(appointments_headers,appointments)
        what_next = message('blue','Hit enter to return to the previous menu',True)
        if what_next == '':
            receptionist_interface()

    else:
        receptionist_interface()
    
    return selected_provider
    
   
def view_consulations(preselected_provider):
    
    if not preselected_provider:
        print_list(doctors_headers,doctors_list)
        print('') # A new line
        selected_provider = select_record(Doctor,doctors_list)

    else:
        selected_provider = preselected_provider

    if selected_provider != None:
        consultations = [consulation for consulation in consultations_list if
        consulation[5] == str(selected_provider) ]
        print('') # A new line
        print_list(consultations_headers,consultations)

        what_next = message('blue','Hit enter to return to the previous menu',True)
        if what_next == '':
            if isinstance(preselected_provider,Doctor):
                doctor_interface()

            else:
                nurse_interface()

    else:
        receptionist_interface()
    
    return selected_provider


def view_consulations(selected_doctor):
    pass


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
        options = [
            'Register Patients','View Appointments',
            'Book Appointment / Request Repeat','Cancel Appointments',
            'Prescription Repeat Request','Generate Appointments Schedules']
        menu_selection = menu(options)

        if menu_selection == '1' :
            clear_screen()
            registration_interface(Patient,patients_list)

        if menu_selection == '2' :
            view_appointments()

        if menu_selection == '3' :
            appointments_interface()

        if menu_selection == '4' :
            receptionist.cancel_appointment()

        if menu_selection == '5' :
            receptionist.forward_repeat_request()

        if menu_selection == '6' :
            generate_appointments_schedules()

        elif  menu_selection == '-1' :
            break

    clear_screen()
    main_screen()


def nurse_interface():
    '''Nurse interface for viewing appointments and writing consultations'''

    options = ['View Appointments','Write Consultation','Write Prescription']
    menu_selection = menu(options)


def doctor_interface():
    '''Doctor interface for viewing appointments, writing consultations and writing prescriptions'''
     
    print_list(doctors_headers,doctors_list)
    selected_doctor = select_record(Doctor,doctors_list)
   
    while True:

        options = ['View Appointments','Write Consultation','Write Prescription','View Consultations','View Prescriptions']
        menu_selection = menu(options)

        if menu_selection == '1':
            view_appointments(selected_doctor)

        if menu_selection == '2':
            selected_doctor.consultation()

        if menu_selection == '3':
            selected_doctor.issue_prescription()

        if menu_selection == '4':
            view_consulations()

        if menu_selection == '5':
            view_prescriptions()

        if menu_selection == '-1':
            clear_screen()
            main_screen()

    

def administration_interface():
    '''Administration interface for adding healthcare providers to the clinic'''

    while True:

        options = ['View Registered Doctors / Nurses','Add doctors to the clinic','Add nurses to the clinic']
        menu_selection = menu(options)

        if menu_selection == '1':
            print('Registered Doctors\n')
            print_list(doctors_headers,doctors_list)
            print('\nRegistered Nurses\n')
            print_list(nurses_headers,nurses_list)
            administration_interface()
                
        elif menu_selection == '2' :
            clear_screen()
            registration_interface(Doctor,doctors_list)

        elif menu_selection == '3' :
            clear_screen()
            registration_interface(Nurse,nurses_list)

        elif menu_selection == '-1':
            break

        else:
            quit_application()

    clear_screen()
    main_screen()


def object_to_list(object):
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

    file_names = ['patients_list','doctors_list','nurses_list','consultations_list','prescriptions_list']
    list_types = [patients_list,doctors_list,nurses_list,consultations_list,prescriptions_list]
   
    for file, list_type in zip(file_names,list_types):
        
        file = os.getcwd() + f'/{file}.csv'
        list_type.clear()
   
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    list_type.append(row) 


def import_schedules_from_cv():
    '''Imports appointment schedules from csv files'''
    os.getcwd()
    doctors_files = []
    nurses_files = []
    temp_schedule = []
    
    # try:
    for file in list(glob.glob('appointments_schedule*')):
        if 'Dr.' not in file:
            nurses_files.append(file)
        else:
            doctors_files.append(file)

    doctors_appointments.clear()
    for file in doctors_files:    
        file = os.getcwd() + f'/{file}'   
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    temp_schedule.append(row)

        provider_name = os.path.basename(file).replace('.csv','').replace('appointments_schedule - Dr. ','')
        doctors_appointments[provider_name] = temp_schedule
        temp_schedule = []

    nurses_appointments.clear()
    for file in nurses_files:    
        file = os.getcwd() + f'/{file}'   
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    temp_schedule.append(row)

            provider_name = os.path.basename(file).replace('.csv','').replace('appointments_schedule - ','')
            nurses_appointments[provider_name] = temp_schedule
            temp_schedule = []


    # except FileNotFoundError:
    #     pass

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

    elif main_menu == '3':
        nurse_interface()

    elif main_menu == '4':
        doctor_interface()

    elif main_menu == '5':
        clear_screen()
        administration_interface()

    elif main_menu in ['0', '-1']:
        quit_application()

    else:
        
        go_to_main_screen = message('red','Please enter one of the mentioned options only. Hit enter to try again, otherwise the application will quit: ')

        if go_to_main_screen == "":
        
            clear_screen()
            main_menu = ''
            main_screen()

        else:
            quit()




##### User Interface #####

if __name__ == '__main__':

    test_main.unittest.main(exit=False)

    what_next = message('blue','Please hit enter to start the application...')

    if what_next == '':
        clear_screen()
        import_from_cv() # Import saved Patients, Doctors and Nurses
        import_schedules_from_cv() # Import saved AppointmentSchedules
        receptionist = Receptionist(1,'Veronica','Reborts')
        main_screen()
       
    

    