from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login
from . models import  (UserProfile, DoctorNotification, Department, Doctor, ReceptionistNotification, Receptionist,
PharmacistNotification, Pharmacist, Patient, MedicalHistory, Appointment,RoomType,BedAllocation,Prescription,MedicalHistoryPrescription,
Discharge,DoctorReview,HospitalReview,Insurance,OTP)
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.utils.timezone import now , make_naive, is_naive,timedelta
from datetime import datetime
import razorpay
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.


# <--------------------------------------- Home page login and signup functions ------------------------------------------>
    
def hospital_homepage(request):
    """ home page views """

    return render(request,'home/hospital_homepage.html')



def hospital_loginpage(request):
    """ loginpage views """

    return render(request,'home/loginpage.html')



def log(request):
    """ loginpage views """

    if request.method=='POST':
        uname=request.POST['user']
        password=request.POST['password']
        user=auth.authenticate(username=uname,password=password)

        if user is not None:
            login(request,user)
            
            if user.is_staff:    
                return redirect('admin_homepage')
            
            user_profile = UserProfile.objects.get(user=user)

            if user_profile:

                if not user_profile.soft_deletion:

                    if user_profile.role == 'Doctor':
                        messages.success(request, f"Welcome Dr {user_profile.user.username}")
                        return redirect('doctor_home') 
                    elif user_profile.role == 'Receptionist':
                        messages.success(request, f"Welcome {user_profile.user.username}")
                        return redirect('receptionist_home')
                    elif user_profile.role == 'Pharmacist':
                        messages.success(request, f"Welcome {user_profile.user.username}")
                        return redirect('pharmacist_home')  
                        
                    elif user_profile.role == 'Patient':
                        messages.success(request, f"Welcome {user_profile.user.username}")
                        return redirect('patient_home') 
                    
                else:
                   
                    messages.error(request, 'Your account has been deactivated. Please contact the administrator.')
                    return redirect('hospital_loginpage')
                
        else:
            messages.error(request,'Invalid Username or password')
            return redirect('hospital_loginpage')



def send_otp(request):
    """
    Password reset views
    """
    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)  
            expires_at = now() + timedelta(minutes=5)  

            OTP.objects.create(email=email, otp=otp, expires_at=expires_at)

            send_mail(
                "Starlight Hospital - OTP for Password Reset",
                f"Your OTP is: {otp}. It will expire in 5 minutes.",
                settings.EMAIL_HOST_USER,
                [email],
            )
            messages.success(request, "OTP sent to your email.")
            return render(request, "home/enter_otp.html", {"email": email})
        
        except User.DoesNotExist:

            messages.error(request, "No user found with this email.")
            return redirect("hospital_loginpage")
          
    return redirect("hospital_loginpage")



def verify_otp(request):
    """
    Password reset
    """
    if request.method == "POST":

        email = request.POST.get("email")  
        entered_otp = request.POST.get("otp")

        try:
            
            otp_instance = OTP.objects.filter(email=email).order_by('-created_at').first()

            if otp_instance:
              
                if otp_instance.is_valid() and otp_instance.otp == entered_otp:
                    
                    otp_instance.delete()  
                    return render(request, "home/reset_password.html", {"email": email}) 
                
                else:
                    messages.error(request, "Invalid or expired OTP.")

            else:
                messages.error(request, "OTP not found or expired.")

        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP request.")
        
        return render(request, "home/enter_otp.html", {"email": email})  

    return redirect("hospital_loginpage")



def reset_password(request):
    """
    Reset pass word views
    """
    if request.method == "POST":
        email = request.POST.get("email")  
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "home/reset_password.html", {"email": email})

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)  
            user.save()
            messages.success(request, "Password reset successful. You can now log in.")
            return redirect("hospital_loginpage")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("hospital_loginpage")
    return redirect("hospital_loginpage")




def doctor_signup(request):
    """ doctor registration views """

    departments = Department.objects.all()
    return render(request,'home/doctor_reg.html',{'departments': departments})



def doctor_register(request):
    """ doctor registration views """

    if request.method=='POST':

        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        department_id=request.POST['department']
        address=request.POST['address']
        image = request.FILES.get('image')
        resume = request.FILES.get('cv')

        if User.objects.filter(username=uname).exists():
                messages.info(request,'Username exists')
                return redirect('doctor_signup')
        
        elif User.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('doctor_signup')
        
        else :
            department=Department.objects.get(id=department_id)
            user=DoctorNotification(fname=fname,lname=lname,uname=uname,email=email,department=department,address=address,image=image,resume=resume)
            user.save()
            messages.success(request,'Registration Successfull,Waiting for admin approval')
            return redirect('hospital_loginpage')




def receptionist_signup(request):
    """ Receptionist registration views """

    return render(request,'home/receptionist_reg.html')




def receptionist_register(request):
    """ Reception registration views """

    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        address=request.POST['address']
        image = request.FILES.get('image')
        resume = request.FILES.get('cv')

        
        if User.objects.filter(username=uname).exists():
                messages.info(request,'Username exists')
                return redirect('receptionist_signup')
        
        elif User.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('receptionist_signup')
        
        else : 
            user=ReceptionistNotification(fname=fname,lname=lname,uname=uname,email=email,address=address,image=image,resume=resume)
            user.save()
            messages.success(request,'Registration Successfull,Waiting for admin approval')
            return redirect('hospital_loginpage')




def pharmacist_signup(request):
    """Pharmacist Registration"""

    return render(request,'home/pharmacist_reg.html')




def pharmacist_register(request):
    """Pharmacist Registration"""

    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        address=request.POST['address']
        image = request.FILES.get('image')
        resume = request.FILES.get('cv')

        
        if User.objects.filter(username=uname).exists():
                messages.info(request,'Username exists')
                return redirect('pharmacist_signup')
        
        elif User.objects.filter(email=email).exists():
                messages.info(request,'Email exists')
                return redirect('pharmacist_signup')
        
        else : 
            user=PharmacistNotification(fname=fname,lname=lname,uname=uname,email=email,address=address,image=image,resume=resume)
            user.save()
            messages.success(request,'Registration Successfull,Waiting for admin approval')
            return redirect('hospital_loginpage')
        


def patient_signup(request):
    """Patient Registration"""
    return render(request,'home/patient_reg.html')



def generate_unique_patient_id():
    """Pharmacist ID generation"""

    last_patient = Patient.objects.order_by('patient_id').last()
    if not last_patient:
        
        return "A0001"

    last_id = last_patient.patient_id
    prefix = last_id[0]  
    number = int(last_id[1:])  
    number += 1

    if number > 9999:  

        next_prefix_index = string.ascii_uppercase.index(prefix) + 1

        if next_prefix_index < len(string.ascii_uppercase):
            prefix = string.ascii_uppercase[next_prefix_index]
            number = 1

        else:
            raise ValueError("Exhausted all patient_id combinations.")

    return f"{prefix}{number:04d}"



def patient_register(request):
    """Patient Registration"""

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password = generate_random_password()

        
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please try another one.")
            return redirect('patient_reg') 
        
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists. Please try another one.')
            return redirect('patient_reg') 
        
        else:
            user = User.objects.create_user(username=uname, email=email, first_name=fname, last_name=lname, password=password)
            user.save()
            user_profile = UserProfile.objects.create(user=user, role='Patient')
            patient_id = generate_unique_patient_id()
            Patient.objects.create(
                user_profile=user_profile,
                gender=gender,
                address=address,
                patient_id=patient_id 
            )
            subject = "Starlight Hospital"
            message = f"Thank you for registering. Your username is: {user.username}, Your patient ID is: {patient_id} and your password is: {password}."
            recipient = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            messages.success(request, "Patient registered successfully. Please check your email for login credentials.")
            return redirect('hospital_loginpage')




def log_out(request):
    """log out """

    auth.logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('hospital_loginpage')


#      <---------------------------------------------- Admin functions ---------------------------------------------------->

@login_required(login_url='hospital_loginpage')  
def admin_homepage(request):
    """admin homepage """

    Appointment.auto_cancel_past_appointments()
    low_stock_medicines = Prescription.objects.filter(alert=True)
    doctors = DoctorNotification.objects.all()
    doctors_count = DoctorNotification.objects.all().count()
    receptionists = ReceptionistNotification.objects.all()
    receptionists_count = ReceptionistNotification.objects.all().count()
    pharmacists = PharmacistNotification.objects.all()
    pharmacists_count = PharmacistNotification.objects.all().count()
    hospital_reviews = HospitalReview.objects.all()
    return render(request,'admin/adminhome.html',{'doctors': doctors ,'receptionists':receptionists ,'pharmacists':pharmacists,'doctors_count':doctors_count,'receptionists_count':receptionists_count,'pharmacists_count':pharmacists_count,'low_stock_medicines':low_stock_medicines,'hospital_reviews':hospital_reviews})



@login_required(login_url='hospital_loginpage') 
def generate_random_password():
    """Random password generation """

    return ''.join(random.choices(string.digits, k=6))



@login_required(login_url='hospital_loginpage') 
def approve_doctor(request, id):
    """Doctor approval """
    notification = DoctorNotification.objects.get(id=id)
    password = generate_random_password()
    user = User.objects.create_user(
        username=notification.uname,
        email=notification.email,
        first_name=notification.fname,
        last_name=notification.lname,
        password=password  
    )
    user_profile = UserProfile.objects.create(user=user, role='Doctor')
    
    Doctor.objects.create(
        user_profile=user_profile,
        department=notification.department,
        address=notification.address,
        image=notification.image,
        resume=notification.resume,
    )
    subject="Starlight Hospital"
    message= f'Your application is approved, your user name is: {user.username} and your password is: {password}'
    recepient=user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    notification.delete()

    messages.success(request, "Doctor approved successfully.")
  
    return redirect('admin_homepage') 



@login_required(login_url='hospital_loginpage') 
def reject_doctor(request, id):
    """Doctor rejection """

    doctor = DoctorNotification.objects.get(id=id)
    subject="Starlight Hospital"
    message= f'We appreciate your interest in Starlight and the time you’ve invested in applying for Doctor opening. Unfortunately we will not be moving forward with your application,'
    recepient=doctor.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    doctor.delete() 
    return redirect('admin_homepage')



@login_required(login_url='hospital_loginpage') 
def approve_receptionist(request, id):
    """Receptionist approval """

    notification = ReceptionistNotification.objects.get(id=id)
    password = generate_random_password()
    user = User.objects.create_user(
        username=notification.uname,
        email=notification.email,
        first_name=notification.fname,
        last_name=notification.lname,
        password=password  
    )
    user_profile = UserProfile.objects.create(user=user, role='Receptionist')
    
    Receptionist.objects.create(
        user_profile=user_profile,
        address=notification.address,
        image=notification.image,
        resume=notification.resume,
    )
    subject="Starlight Hospital"
    message= f'Your application is approved, your user name is: {user.username} and your password is: {password}'
    recepient=user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    notification.delete()
    messages.success(request, "Receptionist approved successfully.")
    return redirect('admin_homepage') 



@login_required(login_url='hospital_loginpage') 
def reject_receptionist(request, id):
    """Receptionist rejection """

    receptionist = ReceptionistNotification.objects.get(id=id)
    subject="Starlight Hospital"
    message= f'We appreciate your interest in Starlight and the time you’ve invested in applying for Receptionist opening. Unfortunately we will not be moving forward with your application,'
    recepient=receptionist.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    receptionist.delete() 
    messages.info(request, "Receptionist rejected successfully.")
    return redirect('admin_homepage')




@login_required(login_url='hospital_loginpage') 
def approve_pharmacist(request, id):
    """Pharmacist approval """

    notification = PharmacistNotification.objects.get(id=id)
    password = generate_random_password()
    user = User.objects.create_user(
        username=notification.uname,
        email=notification.email,
        first_name=notification.fname,
        last_name=notification.lname,
        password=password  
    )
    user_profile = UserProfile.objects.create(user=user, role='Pharmacist')
    
    Pharmacist.objects.create(
        user_profile=user_profile,
        address=notification.address,
        image=notification.image,
        resume=notification.resume,
    )

    subject="Starlight Hospital"
    message= f'Your application is approved, your user name is: {user.username} and your password is: {password}'
    recepient=user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    notification.delete()

    messages.success(request, "Pharmacist approved successfully.")
    return redirect('admin_homepage') 



@login_required(login_url='hospital_loginpage') 
def reject_pharmacist(request, id):
    """pharmacist rejection """

    pharmacist = PharmacistNotification.objects.get(id=id)
    subject="Starlight Hospital"
    message= f'We appreciate your interest in Starlight and the time you’ve invested in applying for Pharmacist opening. Unfortunately we will not be moving forward with your application,'
    recepient=pharmacist.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    pharmacist.delete() 
    messages.info(request, "Pharmacist rejected successfully.")
    return redirect('admin_homepage')



@login_required(login_url='hospital_loginpage') 
def admin_manage(request):
    """Admin manage views"""

    rooms = RoomType.objects.all()
    medicines = Prescription.objects.all()
    return render(request,'admin/admin_manage.html',{'rooms':rooms,'medicines':medicines})



@login_required(login_url='hospital_loginpage') 
def admin_add_department(request):
    """admin department adding """

    if request.method == "POST":
        name = request.POST.get('department')
        Department.objects.create(name=name)
        messages.success(request, "New department added successfully.")
        return redirect('admin_manage')
    


@login_required(login_url='hospital_loginpage')     
def admin_add_rooms(request):
    """admin rooms adding """
    if request.method == "POST":
        room_type = request.POST.get('room_name')
        RoomType.objects.create(room_type=room_type)
        messages.success(request, "New room added successfully.")
        return redirect('admin_manage')
    


@login_required(login_url='hospital_loginpage') 
def admin_add_room_count(request):
    """admin rooms adding """
    if request.method == "POST":
        room_type = request.POST.get('room_type')
        room_rate = request.POST.get('room_rate')
        count = request.POST.get('room_count')
        room = RoomType.objects.get(id=room_type)
     
        if room_rate:
            room.rate_per_day = room_rate
 
        if count:
            room.available_rooms += int(count)
            room.total_rooms += int(count)

        room.save()
        messages.success(request, "Rooms updated successfully.")
        return redirect('admin_manage')




@login_required(login_url='hospital_loginpage') 
def admin_add_medicine(request):
    """admin medicine adding """

    if request.method == "POST":
        medicine = request.POST.get('medicine_name')
        Prescription.objects.create(medicine=medicine)
        messages.success(request, "New Medicine added successfully.")
        return redirect('admin_manage')
    



@login_required(login_url='hospital_loginpage') 
def admin_add_medicine_price(request):
    """admin medicine price adding """

    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name')
        medicine_price = request.POST.get('medicine_price')
        medicine_count = request.POST.get('medicine_stock')
        medicine = Prescription.objects.get(id=medicine_name)

        if medicine_price:
            medicine.rate = medicine_price

        if medicine_count:
            medicine.stock += int(medicine_count)

        medicine.save()
        messages.success(request, "Medicine updated successfully.")
        return redirect('admin_manage')
    


@login_required(login_url='hospital_loginpage') 
def admin_doctor(request):
    """doctor details view for admin """

    doctors = Doctor.objects.all()
    return render(request,'admin/admin_doctor.html',{'doctors':doctors})



@login_required(login_url='hospital_loginpage') 
def admin_doctor_reviews(request, id):
    """doctor review details view for admin """

    doctor = Doctor.objects.get(id=id)
    rating = DoctorReview.objects.filter(doctor=doctor)
    average_rating = rating.aggregate(models.Avg('rating'))['rating__avg'] or 0 
    star_range = range(1, 6)
    return render(request, 'admin/admin_doctor_reviews.html', {
        'rating': rating,
        'average_rating': average_rating,
        'star_range': star_range
    })




@login_required(login_url='hospital_loginpage') 
def admin_restrict_doctor(request,id):
    """soft deltion for doctor """

    doctor = Doctor.objects.get(id=id)
    userprofile = doctor.user_profile
    userprofile.soft_deletion = True
    userprofile.save()
    messages.info(request, "User restricted.")
    return redirect('admin_doctor')



@login_required(login_url='hospital_loginpage') 
def admin_access_doctor(request,id):
    doctor = Doctor.objects.get(id=id)
    userprofile = doctor.user_profile
    userprofile.soft_deletion = False
    userprofile.save()
    messages.success(request, "Access granted.")
    return redirect('admin_doctor')



@login_required(login_url='hospital_loginpage') 
def admin_receptionist(request):
    """receptionist details view for admin """

    receptionists = Receptionist.objects.all()
    return render(request,'admin/admin_receptionist.html',{'receptionists':receptionists})


@login_required(login_url='hospital_loginpage') 
def admin_restrict_receptionist(request,id):
    """soft deletion for receptionist """

    receptionist = Receptionist.objects.get(id=id)
    userprofile = receptionist.user_profile
    userprofile.soft_deletion = True
    userprofile.save()
    messages.info(request, "User restricted.")
    return redirect('admin_receptionist')



@login_required(login_url='hospital_loginpage') 
def admin_access_receptionist(request,id):
    receptionist = Receptionist.objects.get(id=id)
    userprofile = receptionist.user_profile
    userprofile.soft_deletion = False
    userprofile.save()
    messages.success(request, "Access granted.")
    return redirect('admin_receptionist')
    


@login_required(login_url='hospital_loginpage') 
def admin_pharmacist(request):
    """pharmacist details view for admin """

    pharmacists = Pharmacist.objects.all()
    return render(request,'admin/admin_pharmacist.html',{'pharmacists':pharmacists})



@login_required(login_url='hospital_loginpage') 
def admin_restrict_pharmacist(request,id):
    """soft deletion for pharmacist """

    pharmacist = Pharmacist.objects.get(id=id)
    userprofile = pharmacist.user_profile
    userprofile.soft_deletion = True
    userprofile.save()
    messages.info(request, "User restricted.")
    return redirect('admin_pharmacist')



@login_required(login_url='hospital_loginpage') 
def admin_access_pharmacist(request,id):

    pharmacist = Pharmacist.objects.get(id=id)
    userprofile = pharmacist.user_profile
    userprofile.soft_deletion = False
    userprofile.save()
    messages.success(request, "Access granted.")
    return redirect('admin_pharmacist')




@login_required(login_url='hospital_loginpage') 
def admin_patient(request):
    """patient details view for admin """
    patients = Patient.objects.all()
    return render(request,'admin/admin_patient.html',{'patients':patients})




@login_required(login_url='hospital_loginpage') 
def admin_restrict_patient(request,id):
    """soft deletion for patient """

    patient = Patient.objects.get(id=id)
    userprofile = patient.user_profile
    userprofile.soft_deletion = True
    userprofile.save()
    messages.info(request, "User restricted.")
    return redirect('admin_patient')




@login_required(login_url='hospital_loginpage') 
def admin_access_patient(request,id):

    patient = Patient.objects.get(id=id)
    userprofile = patient.user_profile
    userprofile.soft_deletion = False
    userprofile.save()
    messages.success(request, "Access granted.")
    return redirect('admin_patient')




@login_required(login_url='hospital_loginpage') 
def admin_patient_medical_history(request,id):
    """Patient medical history access for admin"""
    patient = Patient.objects.get(id=id)

    medical_history = MedicalHistory.objects.filter(patient=patient).order_by('-visit_date')

    for history in medical_history:
       
        medicines = MedicalHistoryPrescription.objects.filter(medical_history=history).select_related('prescription')
        history.medicine_details = [
            {'medicine': item.prescription.medicine, 'quantity': item.quantity}
            for item in medicines
        ]
    
    return render(request, 'admin/admin_patient_medical_history.html', {
        'medical_history': medical_history,
    })




@login_required(login_url='hospital_loginpage') 
def admin_patient_bill_history(request, id):
    """Patient bill history access for admin"""

    patient = Patient.objects.get(id=id)
    discharges = Discharge.objects.filter(patient=patient).order_by('-discharge_date')
    
    discharge_data = []
    for discharge in discharges:
        medicines = MedicalHistoryPrescription.objects.filter(
            medical_history=discharge.medical_history
        ).select_related('prescription')
        
        medicine_details = []
        for item in medicines:
            medicine_details.append({
                'medicine': item.prescription.medicine,
                'rate': item.prescription.rate,
                'quantity': item.quantity,
                'total_cost': item.prescription.rate * item.quantity,
            })
        
        discharge_data.append({
            'discharge': discharge,
            'medicine_details': medicine_details,
        })
    
    context = {
        'discharge_data': discharge_data,
    }
    return render(request, 'admin/admin_patient_bill_history.html', context)




@login_required(login_url='hospital_loginpage') 
def admin_patient_statistics(request, id):
    """patient statistic view for admin"""
   
    patient = Patient.objects.get(id=id)

    discharges = Discharge.objects.filter(patient=patient)

    total_visits = discharges.count()
    total_consultation_fees = discharges.aggregate(total=Sum('consultation_fee'))['total'] or 0
    total_medicine_costs = discharges.aggregate(total=Sum('total_medicine_cost'))['total'] or 0
    total_room_charges = discharges.aggregate(total=Sum('room_charge'))['total'] or 0
    total_amount_paid = discharges.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'patient': patient,
        'total_visits': total_visits,
        'total_consultation_fees': total_consultation_fees,
        'total_medicine_costs': total_medicine_costs,
        'total_room_charges': total_room_charges,
        'total_amount_paid': total_amount_paid,
    }
    return render(request, 'admin/admin_patient_statistics.html', context)




@login_required(login_url='hospital_loginpage') 
def admin_inventory(request):
    """Medicine inventory for admin"""

    medicines = Prescription.objects.all()
    low_stock_medicines = medicines.filter(alert=True)
    return render(request,'admin/admin_inventory.html',{'medicines':medicines,'low_stock_medicines':low_stock_medicines})



@login_required(login_url='hospital_loginpage') 
def admin_update_stock(request):
    """admin add stock"""

    if request.method == "POST":
        medicine_id = request.POST.get("medicine_id")
        stock_amount = request.POST.get("stock_amount")
        medicine = Prescription.objects.get(id=medicine_id)
        medicine.stock += int(stock_amount)

        if medicine.stock > 50:
            medicine.alert = False
        medicine.save()

        messages.success(request, f"Stock updated for {medicine.medicine}. New stock: {medicine.stock}")
    return redirect("admin_inventory")




@login_required(login_url='hospital_loginpage') 
def admin_reports(request):
    """reports and analytics views for admin"""

    today = now().date()
    first_day_of_month = today.replace(day=1)

    daily_date = request.GET.get("daily_date")

    if daily_date:
        try:
            daily_date = datetime.strptime(daily_date, "%Y-%m-%d").date()
        except ValueError:
            daily_date = today
    else:
        daily_date = today

    start_date = request.GET.get("start_date", first_day_of_month)
    end_date = request.GET.get("end_date", today)

    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            start_date = first_day_of_month
    if isinstance(end_date, str):
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            end_date = today
  
    daily_report = Discharge.objects.filter(discharge_date__date=daily_date).aggregate(
        total_patients=Count('id'),
        total_revenue=Sum('total_amount'),
        total_medicine_cost=Sum('total_medicine_cost'),
        total_consultation_fee=Sum('consultation_fee'),
        total_room_charges=Sum('room_charge'),
    )

   
    monthly_report = Discharge.objects.filter(discharge_date__date__gte=start_date, discharge_date__date__lte=end_date).aggregate(
        total_patients=Count('id'),
        total_revenue=Sum('total_amount'),
        total_medicine_cost=Sum('total_medicine_cost'),
        total_consultation_fee=Sum('consultation_fee'),
        total_room_charges=Sum('room_charge'),
    )

    context = {
        'daily_report': daily_report,
        'monthly_report': monthly_report,
        'daily_date': daily_date,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'admin/admin_reports.html', context)


        
#      <---------------------------------------------- Doctor functions ---------------------------------------------------->


@login_required(login_url='hospital_loginpage') 
def doctor_home(request):
    """doctor homepage"""

    user = request.user.id
    Appointment.auto_cancel_past_appointments()
    doctor = Doctor.objects.get(user_profile__user_id=user)
    total_appointments = Appointment.objects.filter(doctor=doctor, status__in=['Scheduled', 'Rescheduled']).count()
    consulted_count = Appointment.objects.filter(doctor=doctor, status='Completed').count()
    return render(request,'doctor/doctor_home.html',{'doctor':doctor,'total_appointments':total_appointments,'consulted_count':consulted_count})




@login_required(login_url='hospital_loginpage') 
def doctor_appointments(request):
    """doctor appointment page"""

    user = request.user.id
    today = now().date()
    doctor = Doctor.objects.get(user_profile__user_id=user)
    today_appointments = Appointment.objects.filter(doctor=doctor,appointment_date__date=today, status__in=['Scheduled', 'Rescheduled','Completed'])
    upcoming_appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date__gt=today,status__in=['Scheduled', 'Rescheduled'])
    room_types = RoomType.objects.all()
    prescriptions = Prescription.objects.all()
    return render(request,'doctor/doctor_appointments.html',{'doctor':doctor,'today_appointments':today_appointments,'upcoming_appointments':upcoming_appointments,'room_types':room_types,'prescriptions':prescriptions})




@login_required(login_url='hospital_loginpage') 
def doctor_view_medical_history(request, id):
    """doctor access to patient medical history"""

    appointments = Appointment.objects.get(id=id)
    patient_id = appointments.patient
    medical_history = MedicalHistory.objects.filter(patient=patient_id).order_by('-visit_date')
    
  
    for history in medical_history:
       
        medicines = MedicalHistoryPrescription.objects.filter(medical_history=history).select_related('prescription')
        history.medicine_details = [
            {'medicine': item.prescription.medicine, 'quantity': item.quantity}
            for item in medicines
        ]
    
    return render(request, 'doctor/doctor_view_medical_history.html', {
        'medical_history': medical_history,
    })




@login_required(login_url='hospital_loginpage') 
def start_consultation(request):
    """doctor consultation"""

    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        diagnosis = request.POST.get("diagnosis")
        admit = request.POST.get("admit")
        room_type_id = request.POST.get("room_type")
        medicines = request.POST.getlist("medicine")
        quantities = request.POST.getlist("quantity")

        appointment = Appointment.objects.filter(id=appointment_id, status__in=['Scheduled', 'Rescheduled']).first()

        if appointment:
            
            medical_history = MedicalHistory.objects.create(
                patient=appointment.patient,
                doctor=appointment.doctor,
                appointment=appointment,
                diagnosis=diagnosis
            )
            
            for medicine_id, quantity in zip(medicines, quantities):
                prescription = Prescription.objects.filter(id=medicine_id).first()
                if prescription:
                    MedicalHistoryPrescription.objects.create(
                        medical_history=medical_history,
                        prescription=prescription,
                        quantity=quantity
                    )
                    
            appointment.status = "Completed"
            appointment.save()

            if admit == "true":

                room_type = RoomType.objects.filter(id=room_type_id, available_rooms__gt=0).first()

                if room_type:

                    BedAllocation.objects.create(
                        medical_history=medical_history,
                        patient=appointment.patient,
                        room_type=room_type
                    )
                    medical_history.is_inpatient = True
                    medical_history.save()
                    room_type.available_rooms -= 1
                    room_type.save()

            messages.success(request, "Consultation completed successfully!")

        else:

            messages.error(request, "Invalid appointment ID or status!")

    return redirect("doctor_appointments")




@login_required(login_url='hospital_loginpage') 
def doctor_inpatients(request):
    """admitted patient views"""
   
    medical_histories = MedicalHistory.objects.filter(is_inpatient=True)
    
    prescriptions = Prescription.objects.all()
    
    for history in medical_histories:
        bed_allocation = BedAllocation.objects.filter(medical_history=history).first()
        if bed_allocation:
            history.room_type = bed_allocation.room_type.room_type
        else:
            history.room_type = "No room allocated"

    
    return render(request, 'doctor/doctor_inpatients.html', {
        'medical_histories': medical_histories,
        'prescriptions': prescriptions,
    })



@login_required(login_url='hospital_loginpage') 
def start_inpatient_consultation(request):
    """admitted patient consulting views"""

    if request.method == "POST":
        history_id = request.POST.get("history_id") 
        diagnosis = request.POST.get("diagnosis")
        medicines = request.POST.getlist("medicine")
        quantities = request.POST.getlist("quantity")

        medical_history = MedicalHistory.objects.filter(id=history_id).first()

        if medical_history:
            
            medical_history.diagnosis += "\n" + diagnosis  

            for medicine_id, quantity in zip(medicines, quantities):
                prescription = Prescription.objects.filter(id=medicine_id).first()
                if prescription:
                    
                    if prescription.stock >= int(quantity):
                      
                        prescription.stock -= int(quantity)
                        prescription.save()

                        MedicalHistoryPrescription.objects.create(
                            medical_history=medical_history,
                            prescription=prescription,
                            quantity=quantity
                        )
                    else:
                        messages.error(request, f"Not enough stock for {prescription.medicine}.")
                        return redirect("doctor_inpatients")
                    
            medical_history.save()

            messages.success(request, "Consultation updated successfully!")
        else:
            messages.error(request, "Invalid medical history ID!")

    return redirect("doctor_inpatients")




@login_required(login_url='hospital_loginpage') 
def doctor_discharge(request,id):
    """doctor discharge admitted patient"""

    medical_history =MedicalHistory.objects.get(id=id)
    medical_history.is_inpatient = False
    medical_history.save()
    messages.success(request, "Room vacated successfully")
    return redirect('doctor_inpatients')



@login_required(login_url='hospital_loginpage') 
def doctor_profile(request):
    """doctor profile page"""

    user = request.user.id
    doctor = Doctor.objects.get(user_profile__user_id=user)
    return render(request,'doctor/doctor_profile.html',{'doctor':doctor})



@login_required(login_url='hospital_loginpage') 
def update_doctor(request):
    """doctor edit view"""

    if request.method == 'POST':
        user = request.user
        doctor = Doctor.objects.get(user_profile__user_id=user.id)
        doctor.user_profile.user.first_name = request.POST['fname']
        doctor.user_profile.user.last_name = request.POST['lname']
        doctor.address = request.POST['address']
        new_image=request.FILES.get('image')

        if new_image:
            doctor.image = new_image

        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')

        if new_password:

            if doctor.user_profile.user.check_password(old_password):

                doctor.user_profile.user.set_password(new_password)
                messages.success(request, 'Profile updated successfully.Login with new password')
                doctor.user_profile.user.save()
                doctor.save()
                auth.logout(request)
                return redirect('hospital_loginpage')
            
            else:

                messages.error(request, 'Old password is incorrect.')
                return redirect('doctor_profile')
            
        doctor.user_profile.user.save()
        doctor.save()

        if not new_password:

            messages.success(request, 'Profile updated successfully.')

        return redirect('doctor_profile')


#      <---------------------------------------------- Receptionist functions ---------------------------------------------------->

@login_required(login_url='hospital_loginpage') 
def receptionist_home(request):
    """reeceptionist patient register view"""

    user = request.user.id
    Appointment.auto_cancel_past_appointments()
    receptionist = Receptionist.objects.get(user_profile__user_id=user)
    return render(request,'receptionist/receptionist_home.html',{'receptionist':receptionist})




@login_required(login_url='hospital_loginpage') 
def receptionist_patient_register(request):
    """reeceptionist patient register view"""
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password = generate_random_password()

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please try another one.")
            return redirect('receptionist_appointments') 
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists. Please try another one.')
            return redirect('receptionist_appointments') 
        else:
            user = User.objects.create_user(username=uname, email=email, first_name=fname, last_name=lname, password=password)
            user.save()
      
            user_profile = UserProfile.objects.create(user=user, role='Patient')
            patient_id = generate_unique_patient_id()
            Patient.objects.create(
                user_profile=user_profile,
                gender=gender,
                address=address,
                patient_id=patient_id  
            )
            subject = "Starlight Hospital"
            message = f"Thank you for registering. Your username is: {user.username}, Your patient ID is: {patient_id} and your password is: {password}."
            recipient = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
            messages.success(request, "Patient registered successfully. Please check registered email for login credentials.")
            return redirect('receptionist_appointments')




@login_required(login_url='hospital_loginpage') 
def receptionist_appointments(request):
    """receptionist appointments"""

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request,'receptionist/receptionist_appointments.html',{'patients':patients,'doctors':doctors})



@login_required(login_url='hospital_loginpage') 
def book_appointment_reception(request):
    """receptionist appointments"""

    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        reason = request.POST.get('reason')
        appointment_date_object = datetime.fromisoformat(appointment_date) 
        formatted_date = appointment_date_object.strftime('%d %b %Y')
        patient = Patient.objects.get(patient_id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        existing_appointment = Appointment.objects.filter(patient=patient,doctor=doctor,status__in=['Scheduled', 'Rescheduled']).exists()
        same_day_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=appointment_date_object.date()
        ).count()
        
        if same_day_appointments >= 2:

            messages.error(request, "Booking is filled for the doctor on the selected date. Please choose another date or doctor.")
            return redirect('receptionist_appointments')
        
        if existing_appointment:

            messages.error(request, "You already have an existing appointment.")
            return redirect('receptionist_appointments')
        
        Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=appointment_date, reason=reason)
        messages.success(request, "Appointment booked successfully.")
        subject="Starlight Hospital"
        message= f'Your appointment is confirmed for the date {formatted_date}'
        recepient=patient.user_profile.user.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
        return redirect('receptionist_appointments')
    



@login_required(login_url='hospital_loginpage') 
def receptionist_generate_bill(request):
    """Bill generation"""

    medical_histories = Discharge.objects.filter(bill_generated=False)
    
    for medical_history in medical_histories:
        medicalhistory = medical_history.medical_history
        total_medicine_cost = medical_history.total_medicine_cost
        lab_cost = medical_history.medical_history.lab_report_cost

        bed_allocation = BedAllocation.objects.filter(medical_history=medicalhistory).first()

        room_charge = 0
        total_days = 0

        if bed_allocation:

            allocated_date = bed_allocation.allocated_date
            discharged_date = now() 

            if is_naive(allocated_date):
                discharged_date = make_naive(discharged_date)

            total_days = (discharged_date - allocated_date).days or 1
            room_charge = bed_allocation.room_type.rate_per_day * total_days

        consultation_fee = 200
        total_amount = total_medicine_cost + consultation_fee + room_charge + lab_cost 
        medical_history.room_charge = room_charge
        medical_history.total_amount = total_amount

    return render(request, "receptionist/receptionist_generate_bill.html", {
        "medical_histories": medical_histories,
    })



@login_required(login_url='hospital_loginpage') 
def generate_bill(request, id):
    """Bill generation"""

    discharge = Discharge.objects.get(id=id)
    patient = discharge.patient
    doctor = discharge.doctor
    medical_history = discharge.medical_history
    appointment = medical_history.appointment
    lab_cost = discharge.medical_history.lab_report_cost

    prescriptions = MedicalHistoryPrescription.objects.filter(medical_history=medical_history)
    
    total_medicine_cost = sum(
        prescription.prescription.rate * prescription.quantity for prescription in prescriptions
    )

    bed_allocation = BedAllocation.objects.filter(medical_history=medical_history).first()
    room_charge = 0
    total_days = 0
    
    if bed_allocation:
            
            allocated_date = bed_allocation.allocated_date
            discharged_date = now()  

            if is_naive(allocated_date):

                discharged_date = make_naive(discharged_date)

            total_days = (discharged_date - allocated_date).days or 1
            room_charge = bed_allocation.room_type.rate_per_day * total_days
            bed_allocation.room_type.available_rooms += 1
            bed_allocation.discharged_date = discharged_date
            bed_allocation.room_type.save()
            bed_allocation.save()

   
    consultation_fee = 200 
    total_amount = total_medicine_cost + consultation_fee + room_charge + lab_cost
    discharge.total_medicine_cost = total_medicine_cost
    discharge.consultation_fee = consultation_fee
    discharge.room_charge = room_charge
    discharge.total_amount = total_amount
    discharge.bill_generated = True
    discharge.discharge_date = now()
    discharge.medical_history.is_inpatient=False
    discharge.save()
    subject="Starlight Hospital"
    message= f'Bill generated successfully, Total amount is Rs.{total_amount}, visit the reception to pay the amount by cash or card or you can pay through your registered account'
    recepient=patient.user_profile.user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
    messages.success(request, "Bill generated successfully.")
    return redirect('receptionist_generate_bill')




@login_required(login_url='hospital_loginpage') 
def receptionist_pay_bill(request):
    """Receptionist pay bill"""

    bill = Discharge.objects.filter(bill_payed=False , bill_generated=True)
    return render(request,'receptionist/receptionist_pay_bill.html',{'bill':bill})




 
def receptionist_bill_final(request, id):
    """Receptionist pay bill razorpay"""

    discharge = Discharge.objects.get(id=id)
    medical_history = discharge.medical_history
    medicines = MedicalHistoryPrescription.objects.filter(medical_history=medical_history).select_related('prescription')

    medicine_details = []

    for item in medicines:
        medicine_details.append({
            'medicine': item.prescription.medicine,
            'rate': item.prescription.rate,
            'quantity': item.quantity,
            'total_cost': item.prescription.rate * item.quantity
        })

    razorpay_amount = int(discharge.total_amount * 100)  
    razorpay_key = settings.RAZORPAY_KEY_ID
  
    context = {
        'discharge': discharge,
        'medicine_details': medicine_details,'razorpay_amount': razorpay_amount, 'razorpay_key': razorpay_key
    }
    return render(request, 'receptionist/receptionist_bill_final.html', context)




@login_required(login_url='hospital_loginpage') 
def receptionist_pay_cash(request, id):
    """Receptionist pay bill by cash"""

    discharge = Discharge.objects.get(id=id)
    
    if request.method == 'POST':
        discharge.bill_payed = True  
        discharge.save()
        messages.success(request, "Bill payment successful.")
    
    return redirect('receptionist_pay_bill')



@csrf_exempt
def razorpay_payment_callback(request):
    """Razor pay"""

    if request.method == 'POST':
       
        payment_id = request.POST.get('razorpay_payment_id')
        discharge_id = request.POST.get('discharge_id')

        if payment_id and discharge_id:
            discharge = get_object_or_404(Discharge, id=discharge_id)
            discharge.bill_payed = True  
            discharge.save()
            return JsonResponse({'success': True, 'message': 'Payment successful and bill marked as paid.'})
        
        return JsonResponse({'success': False, 'message': 'Invalid payment details.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




@login_required(login_url='hospital_loginpage') 
def receptionist_payment_history(request):
    """receptionist access to bill history"""

    bill = Discharge.objects.filter(bill_payed=True)
    return render(request,'receptionist/receptionist_payment_history.html',{'bill':bill})




@login_required(login_url='hospital_loginpage') 
def receptionist_payment_history_eachbill(request,id):
    discharge = Discharge.objects.get(id=id)
    medical_history = discharge.medical_history

    medicines = MedicalHistoryPrescription.objects.filter(medical_history=medical_history).select_related('prescription')
  
    medicine_details = []

    for item in medicines:

        medicine_details.append({
            'medicine': item.prescription.medicine,
            'rate': item.prescription.rate,
            'quantity': item.quantity,
            'total_cost': item.prescription.rate * item.quantity
        })
    
    context = {
        'discharge': discharge,
        'medicine_details': medicine_details,
    }

    return render(request, 'receptionist/receptionist_payment_history_eachbill.html', context)




@login_required(login_url='hospital_loginpage') 
def receptionist_profile(request):
    """Receptionist profile"""

    user = request.user.id
    receptionist = Receptionist.objects.get(user_profile__user_id=user)
    return render(request,'receptionist/receptionist_profile.html',{'receptionist':receptionist})



@login_required(login_url='hospital_loginpage') 
def update_receptionist(request):
    """Receptionist profile updation"""

    if request.method == 'POST':

        user = request.user
        receptionist = Receptionist.objects.get(user_profile__user_id=user.id)
        receptionist.user_profile.user.first_name = request.POST['fname']
        receptionist.user_profile.user.last_name = request.POST['lname']
        receptionist.address = request.POST['address']
        new_image=request.FILES.get('image')

        if new_image:

            receptionist.image = new_image

        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')

        if new_password:

            if receptionist.user_profile.user.check_password(old_password):

                receptionist.user_profile.user.set_password(new_password)
                messages.success(request, 'Profile updated successfully.Login with new password')
                receptionist.user_profile.user.save()
                receptionist.save()
                auth.logout(request)
                return redirect('hospital_loginpage')
            
            else:
                messages.error(request, 'Old password is incorrect.')
                return redirect('receptionist_profile')
            
        receptionist.user_profile.user.save()
        receptionist.save()

        if not new_password:
            messages.success(request, 'Profile updated successfully.')

        return redirect('receptionist_profile')



@login_required(login_url='hospital_loginpage') 
def receptionist_manage_appointments(request):
    """Receptionist Appoitnments """

    doctors = Doctor.objects.all()
    Appointment.auto_cancel_past_appointments()
    appointments = Appointment.objects.filter(status__in=['Scheduled', 'Rescheduled'])
    patients = Patient.objects.all()
    return render(request, 'receptionist/receptionist_manage_appointments.html', {'doctors': doctors,'appointments': appointments,'patients':patients })



@login_required(login_url='hospital_loginpage') 
def receptionist_delete_appointment(request, id):
    """Receptionist appointment deletion"""

    if request.method == "POST":

        try:
            appointment = Appointment.objects.get(id=id)
            appointment.delete()
            return JsonResponse({'message': 'Appointment deleted successfully!'})
        
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'Appointment not found!'})
        
    return JsonResponse({'message': 'Invalid request'})


#      <---------------------------------------------- Pharmacist functions ---------------------------------------------------->

@login_required(login_url='hospital_loginpage') 
def pharmacist_home(request):
    """medicine dispatch page views"""

    user = request.user.id
    low_stock_medicines = Prescription.objects.filter(stock__lt=50)
    pharmacist = Pharmacist.objects.get(user_profile__user_id=user)
    
    medical_histories = MedicalHistory.objects.all().order_by('-id')

    for history in medical_histories:
        prescriptions = MedicalHistoryPrescription.objects.filter(medical_history=history)
        
        
        prescription_costs = []

        for prescription in prescriptions:
            individual_cost = prescription.prescription.rate * prescription.quantity
            prescription_costs.append({
                'medicine': prescription.prescription.medicine,
                'quantity': prescription.quantity,
                'rate': prescription.prescription.rate,
                'cost': individual_cost
            })
        
        total_cost = sum(p['cost'] for p in prescription_costs)
        history.total_medicine_cost = total_cost 
        history.prescription_costs = prescription_costs  

    return render(request, 'pharmacist/pharmacist_home.html', {
        'pharmacist': pharmacist,
        'medical_histories': medical_histories,
        'low_stock_medicines':low_stock_medicines
    })




@login_required(login_url='hospital_loginpage') 
def pharmacist_dispatch_medicines(request, id):
    """medicine dispatch page views"""

    if request.method == "POST":
        
        lab_report = request.FILES.get("lab_report")
        lab_report_amount = request.POST["lab_report_amount"]
        medical_history = MedicalHistory.objects.get(id=id)
        patient=medical_history.patient

        if medical_history.is_dispatched:
            messages.error(request, "Medicines for this consultation have already been dispatched.")
            return redirect("pharmacist_dashboard")  

        
        prescriptions = MedicalHistoryPrescription.objects.filter(medical_history=medical_history)
        total_medicine_cost = 0  

        for prescription_record in prescriptions:
            prescription = prescription_record.prescription
            quantity = prescription_record.quantity


            if prescription.stock >= quantity:
 
                prescription.stock -= quantity
                prescription.save()

                total_medicine_cost += prescription.rate * quantity
            else:
                messages.error(request, f"Not enough stock for {prescription.medicine}. Dispatch failed.")
                return redirect("pharmacist_dashboard")

        if lab_report:
            medical_history.lab_reports = lab_report
            medical_history.lab_report_cost=lab_report_amount
            medical_history.save()
            subject="Starlight Hospital"
            message= f'Lab reports are ready.Log in to your registered account to access lab report in medical history'
            recepient=patient.user_profile.user.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
           

        medical_history.is_dispatched = True
        medical_history.save()

        Discharge.objects.create(
            patient=medical_history.patient,
            doctor=medical_history.doctor,
            medical_history=medical_history,
            appointment=medical_history.appointment,
            total_medicine_cost=total_medicine_cost,
        )

        messages.success(request, "Medicines dispatched successfully ")
    return redirect("pharmacist_home")




@login_required(login_url='hospital_loginpage') 
def pharmacist_inventory(request):
    """pharmacist inventory views"""

    medicines = Prescription.objects.all()
    low_stock_medicines = medicines.filter(stock__lt=50)
    return render(request,'pharmacist/pharmacist_inventory.html',{'medicines':medicines,'low_stock_medicines':low_stock_medicines})



@login_required(login_url='hospital_loginpage') 
def pharmacist_request_inventory(request,id):
    """pharmacist request inventory views"""

    medicine = Prescription.objects.get(id=id)
    medicine.alert = True
    medicine.save()
    messages.success(request, "Medicines requested successfully ")
    return redirect("pharmacist_inventory")



@login_required(login_url='hospital_loginpage') 
def pharmacist_profile(request):
    """pharmacist profile views"""

    user = request.user.id
    pharmacist = Pharmacist.objects.get(user_profile__user_id=user)
    return render(request,'pharmacist/pharmacist_profile.html',{'pharmacist':pharmacist})



@login_required(login_url='hospital_loginpage') 
def update_pharmacist(request):
    """pharmacist profile edit"""

    if request.method == 'POST':

        user = request.user
        pharmacist = Pharmacist.objects.get(user_profile__user_id=user.id)
        pharmacist.user_profile.user.first_name = request.POST['fname']
        pharmacist.user_profile.user.last_name = request.POST['lname']
        pharmacist.address = request.POST['address']
        new_image=request.FILES.get('image')

        if new_image:
            pharmacist.image = new_image

        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')

        if new_password:

            if pharmacist.user_profile.user.check_password(old_password):
                pharmacist.user_profile.user.set_password(new_password)
                messages.success(request, 'Profile updated successfully.Login with new password')
                pharmacist.user_profile.user.save()
                pharmacist.save()
                auth.logout(request)
                return redirect('hospital_loginpage')
            
            else:
                messages.error(request, 'Old password is incorrect.')
                return redirect('pharmacist_profile')
            
        pharmacist.user_profile.user.save()
        pharmacist.save()

        if not new_password:
            messages.success(request, 'Profile updated successfully.')

        return redirect('pharmacist_profile')


#      <---------------------------------------------- Patient functions ---------------------------------------------------->

@login_required(login_url='hospital_loginpage') 
def patient_home(request):
    """Patient booking"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    doctors = Doctor.objects.all()
    return render(request,'patient/patient_home.html',{'patient':patient,'doctors':doctors})



@login_required(login_url='hospital_loginpage') 
def book_appointment(request):
    """Patient booking"""

    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        reason = request.POST.get('reason')
        appointment_date_object = datetime.fromisoformat(appointment_date)  # Parses ISO 8601 format
        formatted_date = appointment_date_object.strftime('%d %b %Y') 
        patient = Patient.objects.get(patient_id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        same_day_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=appointment_date_object.date()
        ).count()
        
        if same_day_appointments >= 10:
            messages.error(request, "Booking is filled for the doctor on the selected date. Please choose another date or doctor.")
            return redirect('patient_home')
        
        existing_appointment = Appointment.objects.filter(patient=patient,doctor=doctor,status__in=['Scheduled', 'Rescheduled']).exists()

        if existing_appointment:
            messages.error(request, "You already have an existing appointment.")
            return redirect('patient_home')
        
        Appointment.objects.create(patient=patient, doctor=doctor, appointment_date=appointment_date, reason=reason)
        subject="Starlight Hospital"
        message= f'Your appointment is confirmed for the date {formatted_date}'
        recepient=patient.user_profile.user.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])
        messages.success(request, "Appointment booked successfully.")

        return redirect('patient_home') 
    return render(request, 'patient/patient_home.html') 




@login_required(login_url='hospital_loginpage') 
def manage_appointments(request):
    """Patient booking management"""

    user = request.user.id
    Appointment.auto_cancel_past_appointments()
    patient = Patient.objects.get(user_profile__user_id=user) 
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    return render(request, 'patient/manage.html', {'appointments': appointments })



@login_required(login_url='hospital_loginpage') 
def reschedule_appointment(request,id):
    """Patient booking management"""

    if request.method == "POST":
        appointment = Appointment.objects.get( id=id)
        new_date = request.POST.get('appointment_date')
        appointment.appointment_date = new_date
        appointment.status = 'Rescheduled'
        appointment.save()
        messages.success(request, "Appointment rescheduled successfully!")
        appointment_date_object = datetime.fromisoformat(new_date)  # Parses ISO 8601 format
        formatted_date = appointment_date_object.strftime('%d %b %Y') 
        subject="Starlight Hospital"
        message= f'Your appointment is rescheduled to {formatted_date}'
        recepient=appointment.patient.user_profile.user.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recepient])

    return redirect('manage_appointments')



@login_required(login_url='hospital_loginpage') 
def delete_appointment(request, id):
    """Patient booking management"""

    if request.method == "POST":
        appointment =Appointment.objects.get(id=id)
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
    return redirect('manage_appointments')



@login_required(login_url='hospital_loginpage') 
def patient_profile(request):
    """Patient profile views"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    return render(request,'patient/patient_profile.html',{'patient':patient})




@login_required(login_url='hospital_loginpage') 
def patient_bill_payment(request):
    """Patient bill payment"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    bill = Discharge.objects.filter(patient=patient, bill_payed=False , bill_generated=True)
    return render(request,'patient/patient_bill_payment.html',{'bill':bill})



@login_required(login_url='hospital_loginpage') 
def patient_bill_final(request, id):
    """Patient pay bill razor pay"""

    discharge = Discharge.objects.get(id=id)
    medical_history = discharge.medical_history

    medicines = MedicalHistoryPrescription.objects.filter(medical_history=medical_history).select_related('prescription')

    medicine_details = []
    for item in medicines:
        medicine_details.append({
            'medicine': item.prescription.medicine,
            'rate': item.prescription.rate,
            'quantity': item.quantity,
            'total_cost': item.prescription.rate * item.quantity
        })

    razorpay_amount = int(discharge.total_amount * 100)
    razorpay_key = settings.RAZORPAY_KEY_ID

    context = {
        'discharge': discharge,
        'medicine_details': medicine_details,'razorpay_amount': razorpay_amount, 'razorpay_key': razorpay_key
    }

    return render(request, 'patient/patient_bill_final.html', context)




@login_required(login_url='hospital_loginpage') 
def patient_payment_history(request):
    """Patient access to payment history"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    bill = Discharge.objects.filter(patient=patient , bill_payed=True)
    return render(request,'patient/patient_payment_history.html',{'bill':bill})




@login_required(login_url='hospital_loginpage') 
def patient_payment_history_eachbill(request,id):
    """Patient access to payment history"""

    discharge = Discharge.objects.get(id=id)
    medical_history = discharge.medical_history

    medicines = MedicalHistoryPrescription.objects.filter(medical_history=medical_history).select_related('prescription')

    medicine_details = []
    for item in medicines:
        medicine_details.append({
            'medicine': item.prescription.medicine,
            'rate': item.prescription.rate,
            'quantity': item.quantity,
            'total_cost': item.prescription.rate * item.quantity
        })

    context = {
        'discharge': discharge,
        'medicine_details': medicine_details,
    }

    return render(request, 'patient/patient_payment_history_eachbill.html', context)




@login_required(login_url='hospital_loginpage') 
def patient_insurance(request,id):
    """Patient insurance"""

    discharge = Discharge.objects.get(id=id)
    return render(request, 'patient/patient_insurance.html',{'discharge':discharge})



@login_required(login_url='hospital_loginpage') 
def patient_insurance_apply(request,id):
    """Patient insurance"""

    discharge = Discharge.objects.get(id=id)
    
    if request.method == 'POST':
        insurance_company = request.POST.get('iname')
        insurance_number = request.POST.get('inumber') 
        data = Insurance(insurance_company=insurance_company, insurance_number=insurance_number,discharge=discharge)
        data.save()
        messages.success(request, 'Insurance appied successfully')
        discharge.insurance_applied=True
        discharge.save()
        return redirect('patient_payment_history')
    



@login_required(login_url='hospital_loginpage') 
def patient_view_insurance(request,id):
    """Patient access to insurance history"""

    discharge = Discharge.objects.get(id=id)
    insurance = Insurance.objects.get(discharge=discharge)
    return render(request, 'patient/patient_view_insurance.html',{'insurance':insurance})
    



@login_required(login_url='hospital_loginpage') 
def patient_medical_history(request):
    """Patient access to medical history"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    medical_history = MedicalHistory.objects.filter(patient=patient).order_by('-visit_date')

    for history in medical_history:
       
        medicines = MedicalHistoryPrescription.objects.filter(medical_history=history).select_related('prescription')
        history.medicine_details = [
            {'medicine': item.prescription.medicine, 'quantity': item.quantity}
            for item in medicines
        ]
    
    return render(request, 'patient/patient_medical_history.html', {
        'medical_history': medical_history,
    })




@login_required(login_url='hospital_loginpage') 
def patient_doctor_review(request, id):
    """Patient reviewing doctor views"""

    medical_history =MedicalHistory.objects.get(id=id)
    doctor = medical_history.doctor
    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    review = DoctorReview.objects.filter(doctor=doctor, patient=patient).first()

    return render(request, 'patient/patient_doctor_review.html', {
        'doctor': doctor,
        'review': review
    })




@login_required(login_url='hospital_loginpage') 
def patient_submit_review(request, id):
    """Patient review submission code"""

    doctor = get_object_or_404(Doctor, id=id)


    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)

    review = DoctorReview.objects.filter(doctor=doctor, patient=patient).first()

    if request.method == "POST":
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        if not rating:
            messages.error(request, "Please provide a rating.")
            return redirect('patient_doctor_review', id=id)

        if review:
            review.rating = int(rating)
            review.review = review_text
            review.save()  
            messages.success(request, "Your review has been updated successfully!")
            
        else:
            
            DoctorReview.objects.create(
                doctor=doctor,
                patient=patient,  
                rating=int(rating),
                review=review_text
            )
            messages.success(request, "Your review has been submitted successfully!")

        return redirect('patient_doctor_review', id=id)

    return redirect('patient_doctor_review', id=id)




@login_required(login_url='hospital_loginpage') 
def update_patient(request):
    """Patient profile edit"""

    if request.method == 'POST':
        user = request.user
        patient = Patient.objects.get(user_profile__user_id=user.id)
        patient.user_profile.user.first_name = request.POST['fname']
        patient.user_profile.user.last_name = request.POST['lname']
        patient.address = request.POST['address']
        patient.gender = request.POST['gender']
        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')

        if new_password:

            if patient.user_profile.user.check_password(old_password):

                patient.user_profile.user.set_password(new_password)
                update_session_auth_hash(request, user)  
                messages.success(request, 'Profile updated successfully.Login with new password')
                patient.user_profile.user.save()
                patient.save()
                auth.logout(request)
                return redirect('hospital_loginpage')
            
            else:

                messages.error(request, 'Old password is incorrect.')
                return redirect('patient_profile')
            
        patient.user_profile.user.save()
        patient.save()

        if not new_password:
            messages.success(request, 'Profile updated successfully.')

        return redirect('patient_profile')
    



@login_required(login_url='hospital_loginpage') 
def patient_hospital_review(request):
    """Patient review hospital"""

    user = request.user.id
    return render(request,'patient/patient_hospital_review.html')
    


@login_required(login_url='hospital_loginpage') 
def patient_review(request):
    """Patient review hospital"""

    user = request.user.id
    patient = Patient.objects.get(user_profile__user_id=user)
    
    if request.method == 'POST':
        review = request.POST.get('review').strip() 
        
        existing_review = HospitalReview.objects.filter(patient=patient).first()
        
        if existing_review:
            existing_review.review = review
            existing_review.save()
            messages.success(request, 'Review updated successfully')

        else:
            data = HospitalReview(patient=patient, review=review)
            data.save()
            messages.success(request, 'Review submitted successfully')
        
        return redirect('patient_hospital_review')