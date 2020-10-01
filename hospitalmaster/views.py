from django.shortcuts import render, redirect,reverse
from hospitalmaster import forms, models

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import datetime, timedelta, date

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')

def adminclick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')

    return render(request, 'adminclick.html')

def doctorclick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'doctorclick.html')


def adminsignup(request):
    form = forms.AdminSignUpForm()
    if request.method == 'POST':
        form = forms.AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_admin_group = Group.objects.get_or_create(name= 'ADMIN PANEL')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'adminsignup.html', {'form':form})






def doctorsignup(request):
    UserForm = forms.DoctorUserForm()
    DoctorForm = forms.DoctorForm()
    mydict={ 'userForm':UserForm , 'doctorForm': DoctorForm}
    if request.method == 'POST':
        UserForm = forms.DoctorUserForm(request.POST)
        DoctorForm = forms.DoctorForm(request.POST , request.FILES)
        if UserForm.is_valid() and DoctorForm.is_valid():
            user = UserForm.save()
            user.set_password(user.password)
            doctor = DoctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name="Doctor Panel")
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('doctorlogin')

    return render(request, 'doctorsignup.html', context=mydict)




#---> Patient block --->

def patientclick(request):
    return render(request, 'patientclick.html')

def patientsignup(request):

    userForm= forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict ={'userForm':userForm, 'patientForm':patientForm}

    if request.method == 'POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient= patient.save()
            my_patient_group = Group.objects.get_or_create(name='Patient Panel')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')

    return render(request, 'patientsignup.html', context=mydict)

def patientlogin(request):
    return render(request, 'patientlogin.html')





#..............................is_ permission........................................#


def is_admin(user):
    #print(user.groups.filter(name='ADMIN PANEL').exists())
    return user.groups.filter(name='ADMIN PANEL').exists()


def is_doctor(user):
    return user.groups.filter(name='Doctor Panel').exists()


def is_patient(user):
    return user.groups.filter(name='Patient Panel').exists()



#After login for all user......................................

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('doctor_dashboard')
        else:
            return render(request, 'doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('patient_dashboard')
        else:
            return render(request, 'patient_wait_for_approval.html')




#Admin Dashboard View

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = models.Appointment.objects.all().filter(status=False).count()
    mydict = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'appointmentcount': appointmentcount,
        'pendingappointmentcount': pendingappointmentcount,
    }
    return render(request, 'admin_dashboard.html', context=mydict)


# Admin Sidebar Hit click Start

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor(request):
    return render(request, 'admin-doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient(request):
    return render(request, 'admin-patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment(request):
    return render(request, 'admin-appointment.html')

#Sidebar Hitclick End



#Admin Patient all start

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_view_patient.html', {'patients':patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request, 'admin_update_patient.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin_view_patient')
    return render(request, 'admin_add_patient.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient(request):
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'admin_approve_patient.html', {'patients':patients})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin_approve_patient'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_approve_patient')



#Admin Patient Discharge Start..............................


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_discharge_patient.html', {'patients':patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    days = (date.today() - patient.admitDate)  # 2 days, 0:00:00
    assignedDoctor = models.User.objects.all().filter(id=patient.assignedDoctorId)
    d = days.days  # only how many day that is 2
    patientDict = {
        'patientId': pk,
        'name': patient.get_name,
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'admitDate': patient.admitDate,
        'todayDate': date.today(),
        'day': d,
        'assignedDoctorName': assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict = {
            'roomCharge': int(request.POST['roomCharge']) * int(d),
            'doctorFee': request.POST['doctorFee'],
            'medicineCost': request.POST['medicineCost'],
            'OtherCharge': request.POST['OtherCharge'],
            'total': (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
                request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        # for updating to database patientDischargeDetails (pDD)
        pDD = models.PatientDischargeDetails()
        pDD.patientId = pk
        pDD.patientName = patient.get_name
        pDD.assignedDoctorName = assignedDoctor[0].first_name
        pDD.address = patient.address
        pDD.mobile = patient.mobile
        pDD.symptoms = patient.symptoms
        pDD.admitDate = patient.admitDate
        pDD.releaseDate = date.today()
        pDD.daySpent = int(d)
        pDD.medicineCost = int(request.POST['medicineCost'])
        pDD.roomCharge = int(request.POST['roomCharge']) * int(d)
        pDD.doctorFee = int(request.POST['doctorFee'])
        pDD.OtherCharge = int(request.POST['OtherCharge'])
        pDD.total = (int(request.POST['roomCharge']) * int(d)) + int(request.POST['doctorFee']) + int(
            request.POST['medicineCost']) + int(request.POST['OtherCharge'])
        pDD.save()
        return render(request, 'patient_final_bill.html', context=patientDict)
    return render(request, 'patient_generate_bill.html', context=patientDict)




# --------------for Admin discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.db.models import Sum


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf_view(request, pk):
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict = {
        'patientName': dischargeDetails[0].patientName,
        'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
        'address': dischargeDetails[0].address,
        'mobile': dischargeDetails[0].mobile,
        'symptoms': dischargeDetails[0].symptoms,
        'admitDate': dischargeDetails[0].admitDate,
        'releaseDate': dischargeDetails[0].releaseDate,
        'daySpent': dischargeDetails[0].daySpent,
        'medicineCost': dischargeDetails[0].medicineCost,
        'roomCharge': dischargeDetails[0].roomCharge,
        'doctorFee': dischargeDetails[0].doctorFee,
        'OtherCharge': dischargeDetails[0].OtherCharge,
        'total': dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html', dict)

#..................End Billing .......................



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'admin-view-doctor.html', {'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request, 'admin_update_doctor.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor(request):

    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='Doctor Panel')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')

    return render(request, 'admin-add-doctor.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor(request):
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'admin-approve-doctor.html', {'doctors': doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialization(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'admin-view-doctor-specialization.html', {'doctors':doctors})




#................................Appointment Start......................................


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'admin-view-appointment.html', {'appointments':appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {'appointmentForm': appointmentForm, }
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')

    return render(request, 'admin-add-appointment.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment(request):
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(request, 'admin-approve-appointment.html', {'appointments':appointments})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

#end Admin Appointments part.....................................................




#Doctor Dashboard Start.................................#


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentcount = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).count()
    patientdischarged = models.PatientDischargeDetails.objects.all().distinct().filter(
        assignedDoctorName=request.user.first_name).count()

    # for  table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid).order_by('-id')
    appointments = zip(appointments, patients)
    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'appointments': appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'doctor_dashboard.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'doctor_patient.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients = models.PatientDischargeDetails.objects.all().distinct().filter(
        assignedDoctorName=request.user.first_name)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_view_discharge_patient.html',
                  {'dischargedpatients': dischargedpatients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_appointment.html', {'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


# ...................................Doctor end..........................................


#...................Patient Start........................................


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    return render(request, 'patient_appointment.html', {'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    mydict = {'appointmentForm': appointmentForm, 'patient': patient}
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.user.id  # ----user can choose any patient but only their info will be stored
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = request.user.first_name  # ----user can choose any patient but only their info will be stored
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request, 'patient_book_appointment.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments, 'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    dischargeDetails = models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict = None
    if dischargeDetails:
        patientDict = {
            'is_discharged': True,
            'patient': patient,
            'patientId': patient.id,
            'patientName': patient.get_name,
            'assignedDoctorName': dischargeDetails[0].assignedDoctorName,
            'address': patient.address,
            'mobile': patient.mobile,
            'symptoms': patient.symptoms,
            'admitDate': patient.admitDate,
            'releaseDate': dischargeDetails[0].releaseDate,
            'daySpent': dischargeDetails[0].daySpent,
            'medicineCost': dischargeDetails[0].medicineCost,
            'roomCharge': dischargeDetails[0].roomCharge,
            'doctorFee': dischargeDetails[0].doctorFee,
            'OtherCharge': dischargeDetails[0].OtherCharge,
            'total': dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict = {
            'is_discharged': False,
            'patient': patient,
            'patientId': request.user.id,
        }
    return render(request, 'patient_discharge.html', context=patientDict)



    #.............................THE END............................

    #........................NAJMUL AHSAN RAKIB.........................
