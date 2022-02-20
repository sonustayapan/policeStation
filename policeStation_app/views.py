import email
from email.policy import default
from django.shortcuts import render, redirect
from .models import * 
import random
from django.http import request
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import os, re
from random import randint
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError



# Create your views here.

  
default_dict = {
    'app_title': 'Police station',
    'app_name': 'Bihar police',
    'msg_data': {'name': '', 'msg': '', 'type':'success', 'display': ''},
    "acc_page": ["login_page", "register_page"]

}
def index(request):
    default_dict["current_page"] = "index"
    return render(request,'index.html',default_dict)


def console(err):
    print(err)
    print('Type of error: ', type(err))



# check internet connection


def send_otp(request, otp_for='reg'):
    default_dict['verify_for'] = otp_for

    email_to_list = [request.session['email'],]
    subject = 'OTP for Forgot Password'
    otp = randint(1000,9999)
    print('OTP is: ', otp)
    request.session['otp'] = otp
    message = f"your one time otp for Register Police Station Web Service is: {otp}"
    email_from = settings.EMAIL_HOST_USER

   
    send_mail(subject, message, email_from, email_to_list)
           
   
        
    default_dict['msg_data']['name'] = 'Auth Error'
    default_dict['msg_data']['msg'] = f'Username and password not accepted.'
      
    default_dict['msg_data']['type'] = 'success'
    default_dict['msg_data']['display'] = 'show'
    

# otp page
def otp_page(request):
    print('Verify for: ', default_dict['verify_for'])
    return render(request,'otp_page.html', default_dict)

# otp verify functionality
def verify_otp(request, verify_for='reg'):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            master = Master.objects.get(Email=request.session['email'])
            
            if verify_for == 'rec':
                master.Password = request.POST['Password']
                default_dict['msg_data']['name'] = 'Password Changed'
                default_dict['msg_data']['msg'] = 'Congratulations!! Your password has successfully changed.'
            else:
                master.IsActive = True
                if master.Role.Role == 'citizen':
                    Citizen.objects.create(Master=master)
                elif master.Role.Role == 'department':
                    Department.objects.create(Master=master)
               
                
                default_dict['msg_data']['name'] = 'Verified'
                default_dict['msg_data']['msg'] = 'Congratulations!! Your email has successfully verified.'

            master.save()

            default_dict['msg_data']['type'] = 'success'
            default_dict['msg_data']['display'] = 'show'

            del request.session['otp']
            del request.session['email']
            
            return redirect(login_page)
        else:
            default_dict['msg_data']['name'] = 'Invalid OTP'
            default_dict['msg_data']['msg'] = "OTP does not matched. Please enter correct otp."
            default_dict['msg_data']['type'] = 'warning'
            default_dict['msg_data']['display'] = 'show'
            return redirect(otp_page)
    else:
        default_dict['msg_data']['name'] = 'Invalid Request'
        default_dict['msg_data']['msg'] = "Something went wrong. Please try again leter."
        default_dict['msg_data']['type'] = 'warning'
        default_dict['msg_data']['display'] = 'show'
        return redirect(otp_page)
    pass
      
# load all roles
def load_role():
    all_role = Role.objects.all()
    return all_role

default_dict['all_roles'] = load_role()

# register page
def register_page(request):
    print(default_dict['msg_data'])
    default_dict["current_page"] = "register_page"

    return render(request, 'register_page.html', default_dict)

# register functionality
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        role_id = int(request.POST['role'])
        password = request.POST['password']
        print(request.POST)
        try:
            role = Role.objects.get(id=role_id)
            Master.objects.create(Email=email,Role=role,Password=password)

            request.session['email'] = email
            
            on_success = send_otp(request)

            print('success: ', on_success)
            
            if on_success:
                default_dict['msg_data']['name'] = 'OTP Sent'
                default_dict['msg_data']['msg'] = f'One-Time Password has sent to {email}.'
                default_dict['msg_data']['type'] = 'success'
                default_dict['msg_data']['display'] = 'show'
                
            return redirect(otp_page)
            

        except IntegrityError as err:
            msg = f'Error in register view @ line 174: {err}'
            print(msg)
            console(err) # display error in terminal
            print('unique'.upper() in err.args[0])
            
            if 'unique'.upper() in err.args[0]:
                default_dict['msg_data']['name'] = 'Email existed'
                default_dict['msg_data']['msg'] = f'{email} is already existed.'

            default_dict['msg_data']['type'] = 'danger'
            default_dict['msg_data']['display'] = 'show'

            return redirect(register_page)
    else:
        pass
def login_page(request):
    default_dict["current_page"] = "login_page"
    return render(request, 'login_page.html', default_dict)

# login functionality
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        master = ''
        try:
            master =  Master.objects.get(Email=email)
            print(password, master.Password)
            role = master.Role
            print(role.Role)
            default_dict['user_role'] = role
            if master.Password != password:
                raise Exception('password does not matched.')
            else:
                request.session['email'] = email

            profile_data(request)
            return redirect(profile_page)
        except Master.DoesNotExist as err:
            console(err) # display error in terminal
            print('not exist' in err.args[0])
            
            if 'not exist' in err.args[0]:
                default_dict['msg_data']['name'] = 'Not Registered'
                default_dict['msg_data']['msg'] = f'{email} is not registered.'

                default_dict['msg_data']['type'] = 'warning'
                default_dict['msg_data']['display'] = 'show'
            return redirect(login_page)
        except Exception as err:
            console(err) # display error in terminal
            if master.Password != password:
                default_dict['msg_data']['name'] = 'Wrong Password'
                default_dict['msg_data']['msg'] = f'Your {err.args[0]}'

                default_dict['msg_data']['type'] = 'warning'
                default_dict['msg_data']['display'] = 'show'
            return redirect(profile_page)
    else:
        pass


def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])

    if master.Role.Role == 'citizen':
        user = Citizen.objects.get(Master=master)
    elif master.Role.Role == 'department':
        user = Department.objects.get(Master=master)

    default_dict['user_profile'] = user

def profile_update(request):
    user = default_dict['user_profile']
    user_role = user.Master.Role.Role

    fullname = request.POST['fullname']
    country = request.POST['country']
    gender = request.POST['gender']
    state = request.POST['state']
    mobile = request.POST['mobile']
    city = request.POST['city']
    address = request.POST['address']
    pincode = request.POST['pincode']

    if user_role == 'citizen':
        user = Citizen.objects.get(id = user.id)
    elif user_role == 'department':
        user = Department.objects.get(id = user.id)

    user.FullName = fullname
    user.Country = country
    user.Gender = gender
    user.State = state
    user.Mobile = mobile
    user.City = city
    user.Address = address
    user.Pincode = pincode

    user.save()

    return redirect(profile_page)

def profile_page(request):
    profile_data(request)
    default_dict['current_page'] = 'department_profile'
    return render(request, 'app/profile.html', default_dict)
 


@csrf_exempt
def complaint(request):
    default_dict["current_page"] = "complaint"
    if request.method == 'POST':
        fullname = request.POST['full_name']
        fathername = request.POST['father_name']
        gender = request.POST['gender']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        policestation = request.POST['police_station']
        pin_code = request.POST['pin_code']
        house_no = request.POST['house_no']
        discription = request.POST['description']

       
        Complaint.objects.create(

                    FullName=fullname,
                    FatherName = fathername,
                    Gender = gender,
                    Address = address,
                    Country = country,
                    State = state,
                    City = city,
                    PoliceStation = policestation,
                    Pin_Code = pin_code,
                    House_No = house_no,
                    Discription= discription,


             )

    return render(request, 'complaint.html', default_dict)

def complaint_view(request):
    default_dict["current_page"] = "current_page"
    complaint = Complaint.objects.all()
    default_dict['complaint'] = complaint
    return render(request, 'complaint_view.html', default_dict)


def e_fir_page(request):
    default_dict["current_page"] = "e_fir_page"

    try:
        master = Master.objects.get(Email = request.session['email'])
        if request.method == 'POST':
        
            fullname = request.POST['full_name']
            criminalname = request.POST['criminal_name']
            gender = request.POST['gender']
            address = request.POST['address']
            state = request.POST['state']
            city = request.POST['city']
            policestation = request.POST['police_station']
            house_No = request.POST['house_no']
            e_fir= request.POST['description']

            E_fir.objects.create(
                Master = master,
                FullName = fullname,
                CriminalName = criminalname,
                Gender = gender,
                Address = address,
                State = state,
                City = city,
                PoliceStation = policestation,
                House_No = house_No,
                E_fir = e_fir,
                )

        return render(request, 'e_fir_page.html', default_dict)

    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        return render(request, 'e_fir_page.html', default_dict)

def fir_view(request):
    default_dict["current_page"] = "fir_view"
    e_fir = E_fir.objects.all()
    default_dict['E_fir'] = e_fir
    return render(request, 'fir_view.html', default_dict)


def lost_parson(request):
    default_dict["current_page"] = "lost_parson"

    master = Master.objects.get(Email = request.session['email'])
    if request.method == 'POST':

        fullname = request.POST['full_name']
        fathername = request.POST['father_name']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        policestation = request.POST['police_station']
        identification_mark = request.POST['identification_mark']
        identity_Card = request.POST['identity_card']
        date = request.POST['date']
        discription = request.POST['description']

        Lost_Parson.objects.create(
            Master = master,
            FullName=fullname,
            FatherName = fathername,
            Gender = gender,
            Address = address,
            State = state,
            City = city,
            PoliceStation = policestation,
            Identification_Mark = identification_mark,
            Identity_Card = identity_Card,
            Date = date,
            Discription= discription,


        )

    return render(request, 'lost_parson.html', default_dict)

def lost_parsons_view(request):
    default_dict["current_page"] = "lost_parsons_view"
    lost_parson = Lost_Parson.objects.all()
    default_dict['Lost_parson'] = lost_parson
    return render(request, 'lost_parsons_view.html', default_dict)

def report(request):
    default_dict["current_page"] = "report"
    master = Master.objects.get(Email = request.session['email'])

    if request.method == 'POST':

        fullname = request.POST['full_name']
        select_category= request.POST['select_category']
        subject = request.POST['subject']
        address = request.POST['address']
        policestation = request.POST['police_station']
        mobile = request.POST['mobile']
        discription = request.POST['discription']

        Report.objects.create(
            Master = master,
            FullName=fullname,
            Select_Category = select_category,
            Address = address,
            Subject = subject,
            PoliceStation = policestation,
            Mobile = mobile,
            Discription= discription,


        )

    return render(request, 'report.html', default_dict)

def report_view(request):
    default_dict["current_page"] = "report_view"
    report = Report.objects.all()
    default_dict['Report'] = report
    return render(request, 'report_view.html', default_dict)

def police_varification(request):
    default_dict["current_page"] = "police_varification"

    master = Master.objects.get(Email = request.session['email'])

    if request.method == 'POST':

        fullname = request.POST['full_name']
        fathername = request.POST['father_name']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        policestation = request.POST['police_station']
        pin_code = request.POST['pin_code']
        house_no = request.POST['house_no']
        discription = request.POST['discription']

        Police_Varification.objects.create(
            Master = master,
            FullName=fullname,
            FatherName = fathername,
            Gender = gender,
            Address = address,
            City = city,
            PoliceStation = policestation,
            Pin_Code = pin_code,
            House_No = house_no,
            Discription = discription,

        )

    return render(request, 'police_varification.html', default_dict)

def police_verification_view(request):
    default_dict["current_page"] = "police_verification_view"
    police_varification = Police_Varification.objects.all()
    default_dict['Police_Varification'] = police_varification
    return render(request, 'police_verification_view.html', default_dict)

def accident(request):
    default_dict["current_page"] = "accident"
    master = Master.objects.get(Email = request.session['email'])

    if request.method == 'POST':

        fullname = request.POST['full_name']
        adhar_no = request.POST['adhar_no']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        policestation = request.POST['police_station']
        car_no = request.POST['car_no']
        age = request.POST['age']
        accident_car = request.POST['accident_car']
        discription = request.POST['discription']

        Accident.objects.create(
            Master = master,
            FullName=fullname,
            Adhar_No = adhar_no,
            Gender = gender,
            Address = address,
            City = city,
            PoliceStation = policestation,
            Age = age,
            Car_No = car_no,
            Accident_Car = accident_car,
            Discription= discription,


        )

    return render(request, 'accident.html', default_dict)

def accident_view(request):
    default_dict["current_page"] = "accident_view"
    accident = Accident.objects.all()
    default_dict['Accident'] = accident
    return render(request, 'accident_view.html', default_dict)

def passport_status(request):
    default_dict["current_page"] = "passport_status"
    master = Master.objects.get(Email = request.session['email'])

    if request.method == 'POST':
    
        fullname = request.POST['full_name']
        dob = request.POST['date_of_birth']
        city = request.POST['city']
        select_appliction_type = request.POST['select_appliction_type']

        Passport_Status.objects.create(
            Master = master,
            FullName = fullname,
            Dob = dob,
            City = city,
            Select_Appliction_Type = select_appliction_type,


        )

    return render(request, 'passport_status.html', default_dict)

def passport_status_view(request):
    default_dict["current_page"] = "passport_status_view"
    passport_status = Passport_Status.objects.all()
    default_dict['Passport_Status'] = passport_status
    return render(request, 'passport_status_view.html', default_dict) 

def go_message(request):
    default_dict["current_page"] = "go_message"
    master = Master.objects.get(Email = request.session['email'])

    if request.method == 'POST':

        fullname = request.POST['full_name']
        subject  = request.POST['subject']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        messege = request.POST['messege']

        Go_messege.objects.create(
            Master = master,
            FullName = fullname,
            Subject  = subject ,
            Address = address,
            State = state,
            City = city,
            Messege = messege,

        )

    return render(request, 'go_message.html', default_dict)



default_dict['all_state'] = []
for state in state_choices:
    default_dict['all_state'].append({'short_tag': state[0], 'tag': state[0]})

default_dict['all_city'] = []
for city in city_choices:
    default_dict['all_city'].append({'short_tag': city[0], 'tag': city[0]})

default_dict['all_police_station'] = []
for police_station in station_choices:
    default_dict['all_police_station'].append({'short_tag': police_station[0], 'tag': police_station[0]})

def citizen_connect(request):
    default_dict["current_page"] = "citizen_connect"
    return render(request,'app/citizen_connect.html', default_dict)  

def citizen_profile(request):
    default_dict["current_page"] = "citizen_profile"
    return render(request,'app/citizen_profile.html', default_dict)  

def department_profile(request):
    default_dict["current_page"] = "department_profile"
    return render(request,'app/department_profile.html', default_dict)  

def officer_list(request):
    default_dict["current_page"] = "officer_list"
    return render(request, 'officer_list.html', default_dict)

def public_interface(request):
    default_dict["current_page"] = "public_interface"
    return render(request, 'public_interface.html', default_dict)

def traffic_education(request):
    default_dict["current_page"] = "traffic_education"
    return render(request, 'traffic_education.html', default_dict)

def community_policing(request):
    default_dict["current_page"] = "community_policing"
    return render(request, 'community_policing.html', default_dict)

def do_dont(request):
    default_dict["current_page"] = "do_dont"
    return render(request, 'do_dont.html', default_dict)

def emergency_dailing(request):
    default_dict["current_page"] = "emergency_dailing"
    return render(request, 'emergency_dailing.html', default_dict)

def change_password(request):
    default_dict["current_page"] = "change_password"
    return render(request,'change_password.html', default_dict)  

def citizen_rights(request):
    default_dict["current_page"] = "citizen_rights"
    return render(request,'citizen_rights.html', default_dict)  

def children_rights(request):
    default_dict["current_page"] = "children_rights"
    return render(request,'children_rights.html', default_dict)  

def women_rights(request):
    default_dict["current_page"] = "women_rights"
    return render(request,'women_rights.html', default_dict)  

def arrest_rights(request):
    default_dict["current_page"] = "arrest_rights"
    return render(request,'arrest_rights.html', default_dict)  

def prisoner_rights(request):
    default_dict["current_page"] = "prisoner_right"
    return render(request,'prisoner_rights.html', default_dict)  

def duties_rights(request):
    default_dict["current_page"] = "duties_right"
    return render(request,'duties_rights.html', default_dict)

def contact_us(request):
    default_dict["current_page"] = "contact_us"
    return render(request, 'contact_us.html', default_dict)

def history(request):
    default_dict["current_page"] = "history"
    return render(request, 'history.html', default_dict)

def ourgoal(request):
    default_dict["current_page"] = "ourgoal"
    return render(request, 'ourgoal.html', default_dict)

def hierarchy(request):
    default_dict["current_page"] = "hierarchy"
    return render(request, 'hierarchy.html', default_dict)

def who_is_who(request):
    default_dict["current_page"] = "who_is_who"
    return render(request, 'who_is_who.html', default_dict)

def children_safety(request):
    default_dict["current_page"] = "children_safety"
    return render(request, 'children_safety.html', default_dict)

def women_safety(request):
    default_dict["current_page"] = "women_safety"
    return render(request, 'women_safety.html', default_dict)

def senior_citizen_safety(request):
    default_dict["current_page"] = "senior_citizen_safety"
    return render(request, 'senior_citizen_safety.html', default_dict)

def road_safety(request):
    default_dict["current_page"] = "road_safety"
    return render(request, 'road_safety.html', default_dict)

def vehicale_safety(request):
    default_dict["current_page"] = "vehicale_safety"
    return render(request, 'vehicale_safety.html', default_dict)

def mobile_safety(request):
    default_dict["current_page"] = "mobile_safety"
    return render(request, 'mobile_safety.html', default_dict)

def internet_safety(request):
    default_dict["current_page"] = "internet_safety"
    return render(request, 'internet_safety.html', default_dict)

def cm_message(request):
    default_dict["current_page"] = "cm_message"
    return render(request, 'cm_message.html', default_dict)

def signout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(index)



    