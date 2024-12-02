from django.urls import path
from. import views

urlpatterns = [

    #<---------------------------------------------- home urls ------------------------------------------------------------->
    path('',views.hospital_homepage,name='hospital_homepage'),
    path('hospital/loginpage',views.hospital_loginpage,name='hospital_loginpage'),
    path('forgot/password/', views.send_otp, name='send_otp'),
    path('verify/otp/', views.verify_otp, name='verify_otp'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('hospital/doctor/registration',views.doctor_signup,name='doctor_signup'),
    path('doctor_register',views.doctor_register,name='doctor_register'),
    path('hospital/reception/registration',views.receptionist_signup,name='receptionist_signup'),
    path('receptionist_register',views.receptionist_register,name='receptionist_register'),
    path('hospital/pharmacy/registration',views.pharmacist_signup,name='pharmacist_signup'),
    path('pharmacist_register',views.pharmacist_register,name='pharmacist_register'),
    path('hospital/patient/registration',views.patient_signup,name='patient_signup'),
    path('patient_register',views.patient_register,name='patient_register'),
    path('log',views.log,name='log'),
    path('logout', views.log_out, name='logout'),



    #<---------------------------------------------- admin urls ------------------------------------------------------------>

    path('hospital/admin',views.admin_homepage,name='admin_homepage'),
    path('hospital/admin/doctor/reject/<int:id>/', views.reject_doctor, name='reject_doctor'),
    path('hospital/admin/doctor/approve/<int:id>/', views.approve_doctor, name='approve_doctor'),
    path('hospital/admin/receptionist/reject/<int:id>/', views.reject_receptionist, name='reject_receptionist'),
    path('hospital/admin/receptionist/approve/<int:id>/', views.approve_receptionist, name='approve_receptionist'),
    path('hospital/admin/pharmacist/reject/<int:id>/', views.reject_pharmacist, name='reject_pharmacist'),
    path('hospital/admin/pharmacist/approve/<int:id>/', views.approve_pharmacist, name='approve_pharmacist'),
    path('hospital/admin/manage',views.admin_manage,name='admin_manage'),
    path('admin_add_department',views.admin_add_department,name='admin_add_department'),
    path('admin_add_rooms',views.admin_add_rooms,name='admin_add_rooms'),
    path('admin_add_room_count',views.admin_add_room_count,name='admin_add_room_count'),
    path('admin_add_medicine',views.admin_add_medicine,name='admin_add_medicine'),
    path('admin_add_medicine_price',views.admin_add_medicine_price,name='admin_add_medicine_price'),
    path('hospital/admin/doctor',views.admin_doctor,name='admin_doctor'),
    path('hospital/admin/doctor/reviews/<int:id>',views.admin_doctor_reviews,name='admin_doctor_reviews'),
    path('hospital/admin/doctor/restrict/<int:id>',views.admin_restrict_doctor,name='admin_restrict_doctor'),
    path('hospital/admin/doctor/access/<int:id>',views.admin_access_doctor,name='admin_access_doctor'),
    path('hospital/admin/receptionist',views.admin_receptionist,name='admin_receptionist'),
    path('hospital/admin/receptionist/restrict/<int:id>',views.admin_restrict_receptionist,name='admin_restrict_receptionist'),
    path('hospital/admin/receptionist/access/<int:id>',views.admin_access_receptionist,name='admin_access_receptionist'),
    path('hospital/admin/pharmacist',views.admin_pharmacist,name='admin_pharmacist'),
    path('hospital/admin/pharmacist/restrict/<int:id>',views.admin_restrict_pharmacist,name='admin_restrict_pharmacist'),
    path('hospital/admin/pharmacist/access/<int:id>',views.admin_access_pharmacist,name='admin_access_pharmacist'),
    path('hospital/admin/patient',views.admin_patient,name='admin_patient'),
    path('hospital/admin/patient/restrict/<int:id>',views.admin_restrict_patient,name='admin_restrict_patient'),
    path('hospital/admin/patient/access/<int:id>',views.admin_access_patient,name='admin_access_patient'),
    path('hospital/admin/patient/medical/history/<int:id>',views.admin_patient_medical_history,name='admin_patient_medical_history'),
    path('hospital/admin/patient/bill/history/<int:id>',views.admin_patient_bill_history,name='admin_patient_bill_history'),
    path('hospital/admin/patient/statistics/<int:id>',views.admin_patient_statistics,name='admin_patient_statistics'),
    path('hospital/admin/inventory',views.admin_inventory,name='admin_inventory'),
    path('hospital/admin/inventory/stock',views.admin_update_stock,name='admin_update_stock'),
    path('hospital/admin/reports', views.admin_reports, name='admin_reports'),



    #<---------------------------------------------- doctor urls ----------------------------------------------------------->

    path('hospital/doctor',views.doctor_home,name='doctor_home'),
    path('hospital/doctor/appointments',views.doctor_appointments,name='doctor_appointments'),
    path('hospital/doctor/appointments/history/<int:id>',views.doctor_view_medical_history,name='doctor_view_medical_history'),
    path('hospital/doctor/appointments/consultation',views.start_consultation,name='start_consultation'),
    path('hospital/doctor/inpatients',views.doctor_inpatients,name='doctor_inpatients'),
    path('hospital/doctor/appointments/inpatient_consultation',views.start_inpatient_consultation,name='start_inpatient_consultation'),
    path('hospital/doctor/doctor_discharge/<int:id>',views.doctor_discharge,name='doctor_discharge'),
    path('hospital/doctor/profile',views.doctor_profile,name='doctor_profile'),
    path('update_doctor',views.update_doctor,name='update_doctor'),




    #<---------------------------------------------- receptionist urls ----------------------------------------------------->

    path('hospital/receptionist',views.receptionist_home,name='receptionist_home'),
    path('receptionist_patient_register',views.receptionist_patient_register,name='receptionist_patient_register'),
    path('hospital/receptionist/appointments',views.receptionist_appointments,name='receptionist_appointments'),
    path('book_appointment_reception',views.book_appointment_reception,name='book_appointment_reception'),
    path('hospital/receptionist/generate_bill',views.receptionist_generate_bill,name='receptionist_generate_bill'),
    path('generate_bill/<int:id>',views.generate_bill,name='generate_bill'),
    path('hospital/receptionist/pay_bill',views.receptionist_pay_bill,name='receptionist_pay_bill'),
    path('hospital/receptionist/bill_final/<int:id>',views.receptionist_bill_final,name='receptionist_bill_final'),
    path('hospital/receptionist/bill_final/receptionist_pay_cash/<int:id>',views.receptionist_pay_cash,name='receptionist_pay_cash'),
    path('razorpay-callback/', views.razorpay_payment_callback, name='razorpay_payment_callback'),
    path('hospital/receptionist/receptionist_payment_history',views.receptionist_payment_history,name='receptionist_payment_history'),
    path('hospital/receptionist/receptionist_payment_history/<int:id>',views.receptionist_payment_history_eachbill,name='receptionist_payment_history_eachbill'),
    path('hospital/receptionist/hospital/receptionist/appointments/manage',views.receptionist_manage_appointments,name='receptionist_manage_appointments'),
    path('receptionist_delete_appointment/<int:id>',views.receptionist_delete_appointment,name='receptionist_delete_appointment'),
    path('hospital/receptionist/profile',views.receptionist_profile,name='receptionist_profile'),
    path('update_receptionist',views.update_receptionist,name='update_receptionist'),




    #<---------------------------------------------- pharmacist urls ------------------------------------------------------->

    path('hospital/pharmacist',views.pharmacist_home,name='pharmacist_home'),
    path('pharmacist_dispatch_medicines/<int:id>', views.pharmacist_dispatch_medicines, name='pharmacist_dispatch_medicines'),
    path('hospital/pharmacist/inventory',views.pharmacist_inventory,name='pharmacist_inventory'),
    path('hospital/pharmacist/inventory<int:id>',views.pharmacist_request_inventory,name='pharmacist_request_inventory'),
    path('hospital/pharmacist/profile',views.pharmacist_profile,name='pharmacist_profile'),
    path('update_pharmacist',views.update_pharmacist,name='update_pharmacist'),




    #<---------------------------------------------- patient urls ---------------------------------------------------------->
    
    path('hospital/patient',views.patient_home,name='patient_home'),
    path('book_appointment',views.book_appointment,name='book_appointment'),
    path('hospital/patient/manage_appointments',views.manage_appointments,name='manage_appointments'),
    path('reschedule_appointment/<int:id>',views.reschedule_appointment,name='reschedule_appointment'),
    path('delete_appointment/<int:id>',views.delete_appointment,name='delete_appointment'),
    path('hospital/patient/pay_bill',views.patient_bill_payment,name='patient_bill_payment'),
    path('hospital/patient/bill_final/<int:id>',views.patient_bill_final,name='patient_bill_final'),
    path('hospital/patient/payment_history',views.patient_payment_history,name='patient_payment_history'),
    path('hospital/patient/patient_payment_history/<int:id>',views.patient_payment_history_eachbill,name='patient_payment_history_eachbill'),
    path('hospital/patient/insurance/<int:id>',views.patient_insurance,name='patient_insurance'),
    path('hospital/patient/insurance/apply/<int:id>',views.patient_insurance_apply,name='patient_insurance_apply'),
    path('hospital/patient/insurance/view/<int:id>',views.patient_view_insurance,name='patient_view_insurance'),
    path('hospital/patient/medical/history',views.patient_medical_history,name='patient_medical_history'),
    path('hospital/admin/patient/medical/history/review/<int:id>',views.patient_doctor_review,name='patient_doctor_review'),
    path('hospital/admin/patient/medical/history/review/submit/<int:id>',views.patient_submit_review,name='patient_submit_review'),
    path('hospital/patient/profile',views.patient_profile,name='patient_profile'),
    path('update_patient',views.update_patient,name='update_patient'),
    path('hospital/patient/review_hospital',views.patient_hospital_review,name='patient_hospital_review'),
    path('patient_review',views.patient_review,name='patient_review'),
  

    ]