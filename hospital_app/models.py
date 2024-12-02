from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Receptionist', 'Receptionist'),
        ('Pharmacist', 'Pharmacist'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    soft_deletion = models.BooleanField(default=False)

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return now() < self.expires_at

class Department(models.Model):
    name = models.CharField(max_length=100)

class Prescription(models.Model):
    medicine = models.CharField(max_length=20, null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)
    rate = models.PositiveIntegerField(default=0)
    alert = models.BooleanField(default=False)

class DoctorNotification(models.Model):
    fname=models.CharField(max_length=35, null=True)
    lname=models.CharField(max_length=35, null=True)
    uname=models.CharField(max_length=35, null=True)
    email=models.CharField(max_length=55, null=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)


class ReceptionistNotification(models.Model):
    fname=models.CharField(max_length=35, null=True)
    lname=models.CharField(max_length=35, null=True)
    uname=models.CharField(max_length=35, null=True)
    email=models.CharField(max_length=55, null=True)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class Receptionist(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class PharmacistNotification(models.Model):
    fname=models.CharField(max_length=35, null=True)
    lname=models.CharField(max_length=35, null=True)
    uname=models.CharField(max_length=35, null=True)
    email=models.CharField(max_length=55, null=True)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class Pharmacist(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    address=models.CharField(max_length=22225,null=True)
    image=models.ImageField(upload_to='Image/',null=True)
    resume=models.FileField (upload_to='Resume/',null=True)

class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    address=models.CharField(max_length=22225,null=True)
    gender = models.CharField(max_length=5,null=True) 
    is_inpatient = models.BooleanField(default=False)  # Categorize as inpatient or outpatient
    patient_id = models.CharField(max_length=15, unique=True, null=True, blank=True) 



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ], default='Scheduled')
    reason = models.TextField(null=True, blank=True)

    @classmethod
    def auto_cancel_past_appointments(cls):
        today_date = now().date()
        appointments_to_update = cls.objects.filter( appointment_date__date__lt=today_date,  status__in=['Scheduled', 'Rescheduled'])
        appointments_to_update.update(status='Cancelled')

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    prescriptions = models.ManyToManyField(Prescription, through='MedicalHistoryPrescription', blank=True)
    lab_reports = models.FileField(upload_to='LabReports/', null=True, blank=True)
    lab_report_cost = models.PositiveIntegerField(default=0)
    is_dispatched = models.BooleanField(default=False)
    is_inpatient = models.BooleanField(default=False)

class MedicalHistoryPrescription(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

class RoomType(models.Model):
    room_type = models.CharField(max_length=20, null=True,blank=True)
    total_rooms = models.PositiveIntegerField(default=0)
    available_rooms = models.PositiveIntegerField(default=0)
    rate_per_day = models.PositiveIntegerField(default=0)


class BedAllocation(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE,null=True,blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    allocated_date = models.DateTimeField(auto_now_add=True)
    discharged_date = models.DateTimeField(null=True, blank=True)

class Discharge(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, null=True, blank=True, on_delete=models.SET_NULL)
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    total_days = models.PositiveIntegerField(default=0)
    total_medicine_cost = models.PositiveIntegerField(default=0)
    consultation_fee = models.PositiveIntegerField(default=200)
    room_charge = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    discharge_date = models.DateTimeField(null=True, blank=True)
    bill_generated = models.BooleanField(default=False)
    bill_payed = models.BooleanField(default=False)   
    insurance_applied = models.BooleanField(default=False)

class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

class HospitalReview(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    
class Insurance(models.Model):
    discharge = models.ForeignKey(Discharge, on_delete=models.CASCADE)
    insurance_company = models.CharField(max_length=20, null=True,blank=True)
    insurance_number = models.CharField(max_length=20, null=True,blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
   




    


