import datetime
import test_clinic

### Global Variables ###

patients = []
doctors = []
nurses = []
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




    
test_clinic.unittest.main()

   

    