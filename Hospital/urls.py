from django.contrib import admin
from django.urls import path
from hospitalmaster import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('adminclick/', views.adminclick),
    path('adminsignup/', views.adminsignup, name='adminsignup'),

    path('doctorclick/', views.doctorclick),
    path('doctorsignup/', views.doctorsignup, name='doctorsignup'),

    path('patientclick/', views.patientclick),
    path('patientsignup/', views.patientsignup, name='patientsignup'),

#......................adminlogin and after signup redirect.....................................
    path('adminlogin/', LoginView.as_view(template_name='adminlogin.html'), name='adminlogin'),
    path('adminsignup/adminlogin/', LoginView.as_view(template_name='adminlogin.html'), name='adminlogin'),


#......................doctorlogin and after signup redirect.....................................

    path('doctorlogin/', LoginView.as_view(template_name='doctorlogin.html'), name='doctorlogin'),
    path('doctorsignup/doctorlogin/', LoginView.as_view(template_name='doctorlogin.html'), name='doctorlogin'),

#......................Patientlogin and after signup.....................................

    path('patientlogin/', LoginView.as_view(template_name='patientlogin.html'), name='patientlogin'),
    path('patientsignup/patientlogin/', LoginView.as_view(template_name='patientlogin.html'), name='patientlogin'),



    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),


    path('afterlogin/', views.afterlogin_view, name= 'afterlogin' ),
    path('admin-dashboard/', views.admin_dashboard_view, name= 'admin_dashboard'),
    path('admin-doctor/', views.admin_doctor, name= 'admin_doctor'),
    path('admin-patient/', views.admin_patient, name= 'admin_patient'),

    #....................apopointment and after view....................
    path('admin-appointment/', views.admin_appointment, name= 'admin_appointment'),
    path('admin-add-patient/admin_view_patient/', views.admin_view_patient, name= 'admin_view_patient'),

    path('admin_view_patient/', views.admin_view_patient, name= 'admin_view_patient'),
    path('admin-add-patient/', views.admin_add_patient, name= 'admin_add_patient'),
    path('admin-approve-patient/', views.admin_approve_patient, name= 'admin_approve_patient'),
    path('admin-discharge-patient/', views.admin_discharge_patient, name= 'admin_discharge_patient'),

    path('admin-view-doctor/', views.admin_view_doctor, name= 'admin-view-doctor'),
    path('admin-add-doctor/admin-view-doctor/', views.admin_view_doctor, name= 'admin-view-doctor'),


    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,
         name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view, name='update-doctor'),


    path('admin-add-doctor/', views.admin_add_doctor, name= 'admin-add-doctor'),


    path('admin-approve-doctor/', views.admin_approve_doctor, name= 'admin-approve-doctor'),
    path('admin-approve-doctor/<int:pk>', views.approve_doctor_view, name='admin-approve-doctor'),
    path('admin-reject-doctor/<int:pk>', views.reject_doctor_view, name='admin-reject-doctor'),




    path('admin-view-doctor-specialisation/', views.admin_view_doctor_specialization, name='admin-view-doctor-specialization'),
    path('admin-view-appointment/', views.admin_view_appointment, name='admin-view-appointment'),
    path('admin-add-appointment/', views.admin_add_appointment, name='admin-add-appointment'),
    path('admin-approve-appointment/', views.admin_approve_appointment, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view, name='reject-appointment'),




    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,
         name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view, name='update-patient'),


    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),

    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),

    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),


#........................Doctor URL.................................

    path('doctor-dashboard/', views.doctor_dashboard_view, name= 'doctor_dashboard'),
    path('doctor_patient', views.doctor_patient_view, name='doctor_patient'),
    path('doctor-view-patient', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-discharge-patient', views.doctor_view_discharge_patient_view,
         name='doctor-view-discharge-patient'),

    path('doctor_appointment', views.doctor_appointment_view, name='doctor_appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_delete_appointment_view, name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),



#..........................Patient URL................................
    path('patient-dashboard', views.patient_dashboard_view, name='patient_dashboard'),
    path('patient-appointment', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view, name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view, name='patient-discharge'),


]
