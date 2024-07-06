from django.shortcuts import render,redirect
from.models import *
from django.http import HttpResponse
from  django.core.mail import send_mail
from django.contrib import messages
import razorpay
from django.utils.crypto import get_random_string
from .models import usertable
from .models import salontable
from .models import logintable
from .models import servicetable
from .models import bookingtable
from .models import payment
from .models import payment
from .models import complaint
from .models import complaint
# Create your views here.

# def display(request):
#     return render(request,'index.html')

def profile(request):
    if 'u_id' in request.session:
        x=request.session['u_id']
        d=usertable.objects.filter(username=x)
        data = salontable.objects.filter(action='confirm')
        s = set()
        for i in data:
            s.add(i.city)
        l = list(s)
        return render(request,'user_page.html',{'r':d,'r1':l})
    elif 's_id' in request.session:
        x=request.session['s_id']
        d=salontable.objects.filter(username=x)
        return render(request,'salon_page.html',{'r':d})
    elif 'a_id' in request.session:
        x=request.session['a_id']
        # d=logintable.objects.filter(username=x)
        return render(request,'admin_page.html',{'username':x})
    else:
        return render(request, 'index.html')

def aboutpage(request):
    return render(request,'about.html')

def contactpage(request):
    if request.method == 'POST':
        w = request.POST['name']
        x = request.POST['email']
        y = request.POST['subject']
        z = request.POST['message']
        data = contact.objects.create(name=w, email=x, subject=y, message=z)
        print(data)
        data.save()
        return render(request, 'contact.html')
    else:
        return render(request, 'contact.html')


def userreg(request):
    return render(request,'user_registration.html')

def salonreg(request):
    return render(request,'salon_registration.html')

def login_page(request):
    return render(request,'login.html')


def user_create(request):
    message = ""
    if request.method == 'POST':
        name = request.POST['n1']
        username = request.POST['n2']
        email = request.POST['n3']
        phone_number = request.POST['n4']
        password = request.POST['n5']
        confirm_password = request.POST['n6']

        # Check if username already exists
        username_exists = usertable.objects.filter(username=username).exists()
        # Check if email already exists
        email_exists = usertable.objects.filter(email=email).exists()

        if email_exists:
            message = "Email already exists!"
        elif username_exists:
            message = "Username already exists!"
        elif password == confirm_password:
            # Inserting data into the User table
            new_user = usertable.objects.create(name=name, username=username, email=email, phone_number=phone_number,
                                                password=password, confirm_password=confirm_password)
            new_login = logintable.objects.create(username=username, password=password, status=1)
            # Save the new user
            new_user.save()
            new_login.save()
            return redirect(profile)
        else:
            message = "Password and Confirm Password do not match!"
    return render(request, 'user_registration.html', {'message': message})


def salon_create(request):
    message = ""
    if request.method == 'POST':
        salon_name = request.POST['n1']
        username = request.POST['n2']
        owner_name = request.POST['n3']
        email = request.POST['n4']
        phone_number = request.POST['n5']
        city = request.POST['n6']
        zip_code = request.POST['n7']
        license = request.FILES['n8']
        password = request.POST['n9']
        confirm_password = request.POST['n10']
        photo = request.FILES['n11']
        time = request.POST['n12']

        # Check if the username already exists in the salontable
        username_exists = salontable.objects.filter(username=username).exists()
        # Check if the email already exists in the usertable
        email_exists = salontable.objects.filter(email=email).exists()

        if email_exists:
            message = "Email already exists!"
        elif username_exists:
            message = "Username already exists!"
        elif password == confirm_password:
            # Inserting data into the salontable
            new_salon = salontable.objects.create(salon_name=salon_name, username=username, owner_name=owner_name,
                                                   email=email, phone_number=phone_number,
                                                   city=city, zip_code=zip_code, license=license, password=password,
                                                   confirm_password=confirm_password, action='pending', photo=photo,
                                                   time=time)
            # Inserting data into the logintable
            new_login = logintable.objects.create(username=username, password=password, status=2)
            # Save the new entries
            new_salon.save()
            new_login.save()
            return redirect(profile)
        else:
            message = "Password and Confirm Password do not match!"

    return render(request, 'salon_registration.html', {'message': message})

def login_details(request):
    # if request.method == 'POST':
    #     u = request.POST['n1']
    #     p = request.POST['n2']
    #     try:
    #         data = logintable.objects.get(username=u)
    #         if data.password == p:
    #             if data.status == 1:
    #                 request.session['u_id'] = u
    #                 return redirect(profile)
    #                 # Filter user data based on username
    #                 # user_data = usertable.objects.filter(username=u)
    #                 # return render(request, 'user_page.html', {'udetails': user_data})
    #             elif data.status == 2:
    #                 request.session['s_id'] = u
    #                 # return render(request, 'salon_page.html')
    #                 return redirect(profile)
    #             elif data.status == 0:
    #                 request.session['a_id'] = u
    #                 # return render(request, 'admin_page.html')
    #                 return redirect(profile)
    #             else:
    #                 return HttpResponse("Unknown status")
    #         else:
    #             return HttpResponse('Password incorrect')
    #     except Exception:
    #         return HttpResponse("Username incorrect")
    # else:
    #     return render(request, 'login.html')
    if request.method == 'POST':
        u = request.POST['n1']
        p = request.POST['n2']
        try:
            data = logintable.objects.get(username=u)
            if data.password == p:
                if data.status==1 :
                    request.session['u_id'] = u
                    return redirect(profile)
                elif data.status==2:
                    data = salontable.objects.get(username=u)
                    if data.action == 'confirm':
                        request.session['s_id']= u
                        return redirect(profile)
                    else:
                        messages.info(request, 'login failed,request is processing...')
                        return render(request,'login.html')
                else:
                    request.session['a_id'] = u
                    return redirect(profile)
            else:
                messages.info(request, 'login failed,password incorrect...')
                return render(request, 'login.html')
        except Exception:
            messages.info(request, 'login failed,incorrect username...')
            return render(request, 'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    if 'u_id' in request.session:
        request.session.flush()
        return render(request, 'index.html')
    elif 's_id' in request.session:
        request.session.flush()
        return render(request, 'index.html')
    elif 'a_id' in request.session:
        request.session.flush()
        return render(request, 'index.html')
    else:
        request.session.flush()
        return render(request, 'index.html')

def profilepage(request):
    # if 'u_id' in request.session:  # Check if user is logged in
    #     username = request.session['u_id']
    #     # Fetch user's details from the database
    #     user_details = usertable.objects.filter(username=username).first()
    #     return render(request, 'profile_user.html', {'user_details': user_details})
    # else:
    #     # Handle case where user is not logged in
    #     return HttpResponse("Please log in to view this page.")
    if request.method=='GET':
        x=request.session['u_id']
        d=usertable.objects.filter(username=x)
        return render(request,'profile_user.html',{'r':d})
    else:
        return render(request,'user_page.html')


def change_password(request):
    return render(request,'change_password.html')

def password_change(request):
    if 'u_id' in request.session:  # Check if user is logged in
        username = request.session['u_id']
        user = usertable.objects.get(username=username)

        if request.method == 'POST':
            # Get the form data
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            # Check if the old password matches
            if old_password != user.password:
                error_message = 'Incorrect old password'
                return render(request, 'change_password.html', {'error_message': error_message})

            # Check if the new password and confirm password match
            if new_password != confirm_password:
                error_message = 'New password and confirm password do not match'
                return render(request, 'change_password.html', {'error_message': error_message})

            # Update the password in the usertable
            user.password = new_password
            user.confirm_password = new_password
            user.save()

            # Update the password in the logintable (if applicable)
            try:
                login_user = logintable.objects.get(username=username)
                login_user.password = new_password
                login_user.save()
            except logintable.DoesNotExist:
                pass  # Handle case where the user does not exist in the logintable

            return redirect(login_details)  # Redirect to the login page after successful password change

        else:
            return render(request, 'change_password.html')

    else:
        return HttpResponse('User not logged in')
def update_user(request):
    # if 'u_id' in request.session:  # Check if user is logged in
    #     username = request.session['u_id']
    #     # Fetch user's details from the database
    #     user_details = usertable.objects.filter(username=username).first()
    #     return render(request, 'update_user.html', {'user_details': user_details})
    # else:
    #     # Handle case where user is not logged in
    #     return HttpResponse("Please log in to view this page.")
    if request.method=='POST':
        x=request.POST['c1']
        d=usertable.objects.filter(username=x)
        return render(request,'update_user.html',{'r':d})
    else:
        return render(request,'update_user.html')

def user_update(request):
    # message = None
    #
    # if 'u_id' in request.session:  # Check if user is logged in
    #     username = request.session['u_id']
    #     if request.method == 'POST':
    #         name = request.POST.get('name')
    #         username = request.POST.get('username')
    #         email = request.POST.get('email')
    #         phone_number = request.POST.get('phone_number')
    #
    #         # Assuming 'username' is used to identify the user
    #         user = usertable.objects.filter(username=username).first()
    #
    #         if user:
    #             # Update the user's email and phone number
    #             user.name = name
    #             user.username = username
    #             user.email = email
    #             user.phone_number = phone_number
    #             user.save()
    #
    #             message = "User profile updated successfully."
    #         else:
    #             message = "User not found."
    #     else:
    #         message = "Invalid request method."
    # else:
    #     message = "User not logged in."
    #
    # # Render the template with the message
    # return render(request, 'update_user.html', {'message': message})
    if request.method=='POST':
        a = request.POST['username']
        b = request.POST['name']
        c = request.POST['email']
        g = int(request.POST['phone_number'])
        d = usertable.objects.filter(username=a)
        d.update(name=b,email=c,phone_number=g)
        return redirect(profilepage)
    else:
        return HttpResponse(request, 'update_user.html')

#admin view request for salons
def s_request(request):
    if request.method=='GET':
         d=salontable.objects.filter(action='pending')
         return render(request,'request.html',{'r':d})
    else:
        return render(request,'admin_page.html')

#admin confirm salons
def supdate(request):
    if request.method=='POST':
        a = request.POST['b1']
        d = salontable.objects.filter(salon_name=a)
        d.update(action='confirm')
        # return HttpResponse('updated')
        return redirect(profile)
    else:
        return render(request,'request.html')

#admin delete salons
def sdelete(request):
        if request.method=='POST':
            a = request.POST['b2']
            d = salontable.objects.filter(salon_name=a)
            d.delete()
            logintable.objects.filter(username=a).delete()
            return redirect(profile)
        else:
            return render(request,'request.html')

#admin view salons(confirm)
def vsalon(request):
    if request.method=='GET':
         d=salontable.objects.filter(action='confirm')
         return render(request,'view_salon.html',{'r':d})
    else:
        return render(request,'salon_page.html')

#admin delete salon
def salondelete(request):
    if request.method=='POST':
        a = request.POST['b2']
        d = salontable.objects.get(username=a)
        b=d.email
        d.delete()
        logintable.objects.filter(username=a).delete()
        send_mail('Removed', 'your removed from  Website',
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(profile)
    else:
        return render(request,'view_salon.html')

#admin Warning salon due to feedback
def warning(request):
    if request.method=='POST':
        x=request.POST['b3']
        y=request.POST['b2']
        d=salontable.objects.filter(salon_name=y,email=x)
        return render(request,'warning.html',{'r':d})
    else:
        return render(request, 'warning.html')
#
def salonwarning(request):
    if request.method=='POST':
        b = request.POST['n']
        c = request.POST['n1']
        send_mail('Warning Message', c,
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(profile)
    else:
         return render(request, 'warning.html')

#salon - profile
def s_profilepage(request):
    if request.method=='GET':
        a = request.session['s_id']
        d = salontable.objects.filter(username=a)
        return render(request, 'profile_salon.html', {'r': d})
    else:
        return render(request,'salon_page.html')

#salon - profile update
def update_salonprofile(request):
    if request.method=='POST':
        x=request.POST['c1']
        d=salontable.objects.filter(username=x)
        return render(request,'update_salon.html',{'r':d})
    else:
        return render(request,'update_salon.html')

def salon_update_final(request):
    message = None
    if request.method == 'POST':
        username = request.POST['c1']
        salon_name = request.POST['salon_name']
        owner_name = request.POST['owner_name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        zip_code = int(request.POST['zip'])
        # license = request.FILES['license']
        time = request.POST['time']
        photo = request.FILES['photo']

        # Update the usertable with the corresponding username
        d = salontable.objects.filter(username=username)
        d.update(salon_name=salon_name,owner_name=owner_name,email=email,phone_number=phone,
                 city=city,zip_code=zip_code,time=time,photo=photo)
        message = "Profile updated successfully"
        return render(request, 'salon_page.html',{'message':message})
    else:
        return HttpResponse(request,'update_salon.html')

def change_password2(request):
    return render(request, 'change_password2.html')


def password_change2(request):
    if 's_id' in request.session:  # Check if user is logged in
        username = request.session['s_id']
        salon = salontable.objects.get(username=username)

        if request.method == 'POST':
            # Get the form data
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            # Check if the old password matches
            if old_password != salon.password:
                error_message = 'Incorrect old password'
                return render(request, 'change_password2.html', {'error_message': error_message})

            # Check if the new password and confirm password match
            if new_password != confirm_password:
                error_message = 'New password and confirm password do not match'
                return render(request, 'change_password2.html', {'error_message': error_message})

            # Update the password in the usertable
            salon.password = new_password
            salon.confirm_password = new_password
            salon.save()

            # Update the password in the logintable (if applicable)
            try:
                login_user = logintable.objects.get(username=username)
                login_user.password = new_password
                login_user.save()
            except logintable.DoesNotExist:
                pass  # Handle case where the user does not exist in the logintable

            return redirect(login_details)  # Redirect to the login page after successful password change

        else:
            return render(request, 'change_password.html')

    else:
        return HttpResponse('User not logged in')
#salon adding services
def addservices(request):
    if request.method == 'POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.POST['n6']
        g = request.POST['n7']
        h = request.FILES['n8']
        data = servicetable.objects.create(service_name=a, description=b, amount=c, username=d, salon_name=e, gender=f,
                                           category=g, service_photo=h)
        data.save()
        return render(request, 'salon_page.html')
    else:
        a = request.session['s_id']
        d = salontable.objects.filter(username=a)
        return render(request, 'addservice.html', {'r': d})

#salon viewing service
def viewservice(request):
    if request.method=='GET':
        a = request.session['s_id']
        data = servicetable.objects.filter(username=a)
        return render(request,'viewservice.html',{'r':data})
    else:
        return render(request,'salon_page.html')


#salon - delete service
def deleteservice(request):
    if request.method=='POST':
        a = request.POST['b1']
        b = request.POST['b2']
        c = request.POST['b3']
        d = servicetable.objects.filter(username=a,service_name=b,gender=c)
        d.delete()
        return redirect(profile)
    else:
        return render(request,'viewservice.html')


#salon - update service
def update_service(request):
    if request.method == 'POST':
        x = request.POST['b1']
        y = request.POST['b2']
        z = request.POST['b3']
        # w = request.POST['b4']
        # c = request.POST['b5']
        # p = request.FILES['b6']
        d = servicetable.objects.filter(username=x, service_name=y,gender=z)
        print(d)
        return render(request, 'updateservice.html', {'r': d})
    else:
        return render(request, 'updateservice.html')


def updateservice(request):
    if request.method == 'POST':
        a = request.POST['n']
        b = request.POST['n1']
        c = request.POST['n2']
        e = request.POST['n3']
        f = request.POST['n4']
        g = request.FILES['n5']
        h = request.POST['n6']
        d = servicetable.objects.filter(username=a, service_name=b,gender=h)
        d.update(service_name=b, description=c, amount=e, category=f,service_photo=g)
        return redirect(viewservice)
    else:
        return render(request, 'updateservice.html')


def locfil(request):
    if request.method == 'POST':
        x = request.POST['city']
        d = salontable.objects.filter(city=x,action='confirm')
        return render(request, 'salons.html', {'r':d})
    else:
       return render(request, 'user_page.html')


#each salon - view by user
def salon_avl(request,a):
    request.session['sa_id'] = a
    return render(request, 'salon_avl.html')


#user view - salon profile
def details(request):
    a = request.session['sa_id']
    d = salontable.objects.filter(salon_name=a)
    return render(request, 'salon_user_viewdetails.html', {'r': d})

# #user view services of respective salon
# def services(request):
#     a = request.session['sa_id']
#     d = servicetable.objects.filter(salon_name=a)
#     return render(request, 'services.html', {'r': d})

def selectgender(request):
    return render(request,'select_gender.html')

#filtering category based on gender and salon name
def select_gender(request):
    if request.method == 'POST':
        # Get the selected gender from the form
        selected_gender = request.POST.get('gender')

        # Check if the selected gender is valid
        if selected_gender in ['male', 'female']:
            # Convert selected_gender to match database format
            database_gender = 'F' if selected_gender == 'female' else 'M'

            # Set the session variable for selected_gender
            request.session['selected_gender'] = selected_gender

            # Get the salon ID from session
            salon_id = request.session.get('sa_id')

            # Filter servicetable based on the selected gender and salon name
            filtered_services = servicetable.objects.filter(gender=database_gender, salon_name=salon_id)

            # Get unique categories for the selected gender and salon
            categories = filtered_services.values_list('category', flat=True).distinct()

            # Pass the filtered services and categories to the template
            return render(request, 'select_category.html', {'r': categories})

    # Render the HTML form if it's a GET request or the selected gender is invalid
    return render(request, 'select_gender.html')

def servicepg(request):
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        if selected_category:
            # Get the selected gender and salon ID from the session
            selected_gender = request.session.get('selected_gender')
            salon_id = request.session.get('sa_id')

            # Convert selected gender to match database format
            database_gender = 'F' if selected_gender == 'female' else 'M'

            # Filter servicetable based on the selected category, gender, and salon ID
            services = servicetable.objects.filter(category=selected_category, gender=database_gender,
                                                    salon_name=salon_id)

            # Print the filtered services for debugging
            # print("Selected category:", selected_category)
            # print("Selected gender:", selected_gender)
            # print("Salon ID:", salon_id)
            # print("Filtered services:", services)

            # Pass the filtered services to the template
            return render(request, 'service_page.html', {'services': services})

    # If it's a GET request or no category is selected, render the form
    return render(request, 'select_category.html')

def book_appointment1(request,name,amount):

    a = request.session['sa_id']
    a1 = request.session['u_id']
    print(a1)
    d = servicetable.objects.filter(salon_name=a)
    d1=salontable.objects.get(salon_name=a)
    d3=usertable.objects.filter(username=a1)
    f=d1.time
    n=d1.salon_name
    return render(request, 'appointment.html', {'r': d, 'r1': a1,'r2':f,'r3':n,'r4':d3,'r5':name,'r6':amount})
#user make booking
def book_appointment(request):
    if request.method == 'POST':
        a = request.POST['customer_name']
        c = int(request.POST['mobile'])
        d = request.POST['email']
        e = request.POST['appointment_date']
        f = request.POST['appointment_time']
        g = request.POST['service_name']
        j = request.POST['username']
        k = request.POST['salon_name']

        data = bookingtable.objects.create(customer_name=a,mobile=c,email=d,appointment_date=e,appointment_time=f,service_name=g,
                                        username=j,salon_name=k,status='pending')
        data.save()
        return redirect(profile)
    # else:
    #     a = request.session['sa_id']
    #     a1 = request.session['u_id']
    #     d = servicetable.objects.filter(salon_name=a)
    #     # d1=salontable.objects.get(salon_name=a)
    #     return render(request,'appointment.html',{'r':d,'r1':a1})

# def sucess(request):
#     return render(request,'sucess.html')
#salon view booking requests
def book_request(request):
    if request.method=='GET':
         a = request.session['s_id']
         b=salontable.objects.get(username=a)
         d=bookingtable.objects.filter(salon_name=b.salon_name,status='pending')
         # print(d)
         return render(request,'bookrequest.html',{'r':d})
    else:
        return render(request,'salon_page.html')

# #salon approve appointment
# def approve_appt(request):
#     if request.method=='POST':
#         a = request.POST['b1']
#         b = request.POST['b2']
#         c = request.POST['b3']
#         e = request.POST['b4']
#         d = bookingtable.objects.filter(username=a,customer_name=b,service_name=e)
#         d.update(status='confirm')
#         send_mail('Confirm Appointment', 'Your appointment is confirmed',
#                   'settings.EMAIL_HOST_USER', [c], fail_silently=False)
#         return redirect(profile)
#     else:
#         return render(request,'bookrequest.html')


# salon approve appointment
def approve_appt(request):
    if request.method == 'POST':
        a = request.POST['b1']  # username
        b = request.POST['b2']  # customer_name
        c = request.POST['b3']  # customer email
        e = request.POST['b4']  # service_name

        # Filter appointments that are pending
        d = bookingtable.objects.filter(username=a, customer_name=b, service_name=e, status='pending')
        if d.exists():
            d.update(status='confirm')
            send_mail('Confirm Appointment', 'Your appointment is confirmed',
                      'settings.EMAIL_HOST_USER', [c], fail_silently=False)
        return redirect(profile)
    else:
        return render(request, 'bookrequest.html')

#salon reject appointment
def reject_appt(request):
    if request.method=='POST':
        a = request.POST['b4']
        b = request.POST['b5']
        c = request.POST['b6']
        d = bookingtable.objects.filter(username=a,customer_name=b,service_name=c)
        d.update(status='Reject')
        return redirect(profile)
    else:
        return render(request,'bookrequest.html')


#user view booking details
def user_view_appt(request):
    if request.method=='GET':
        a = request.session['u_id']
        data = bookingtable.objects.filter(username=a)
        return render(request,'user_view_appointment.html',{'r':data})
    else:
        return render(request,'user_page.html')


def payment1(request):
#     if request.method == 'POST':
#             x = request.POST['b1']
#             y = request.POST['b2']
#             z = request.POST['b3']
#             a = request.POST['b4']
#             # b = request.POST['b5']
#             request.session['c_name'] = a
#             request.session['s_name'] = y
#             d = bookingtable.objects.filter(username=x,customer_name=a,salon_name=y,service_name=z,status='confirm')
#             if list(d) ==[]:
#                 url='uviewappt'
#                 msg='''<script>alert('payment not allowed.. your in processing')
#                 window.location='%s'</script>'''%(url)
#                 return HttpResponse(msg)
#             else:
#                 data=servicetable.objects.filter(service_name=z,salon_name=y)
#                 for i in data:
#                     k=i.amount
#                 return render(request,'payment.html',{'r':d,'r1':k})
#     else:
#         return render(request, 'payment.html')
    if request.method == 'POST':
        x = request.POST['b1']
        y = request.POST['b2']
        s = request.POST['b3']
        a = request.POST['b4']
        # b = request.POST['b5']
        request.session['c_name'] = a
        request.session['s_name'] = y
        request.session['se_name'] = s

        # Filter bookings based on the provided criteria
        d = bookingtable.objects.filter(username=x, customer_name=a, salon_name=y, service_name=s)
        # Check if there are any bookings with status 'confirm'
        confirmed_bookings = d.filter(status='confirm')
        if confirmed_bookings.exists():
            data = servicetable.objects.filter(service_name=s, salon_name=y)
            for i in data:
                k = i.amount
            return render(request, 'payment.html', {'r': confirmed_bookings, 'r1': k})
        # Check if there are any bookings with status 'payment completed'
        completed_bookings = d.filter(status='payment completed')
        if completed_bookings.exists():
            url = 'uviewappt'
            msg = '''<script>alert("Payment has already been completed for this booking.")
                  window.location='%s'</script>''' % url
            return HttpResponse(msg)

        # Check if there are any bookings with status 'appointment cancelled'
        cancelled_bookings = d.filter(status='Appointment Cancelled')
        if cancelled_bookings.exists():
            url = 'uviewappt'
            msg = '''<script>alert("Payment not allowed. Your booking has been cancelled.")
                  window.location='%s'</script>''' % url
            return HttpResponse(msg)

        # If no bookings match the provided criteria or have status 'confirm', show a message
        url = 'uviewappt'
        msg = '''<script>alert("Payment not allowed. Your booking is in processing.")
              window.location='%s'</script>''' % url
        return HttpResponse(msg)
    else:
        return render(request, 'payment.html')


#user-paying payment
def pay(request, id):
        # amount = (id+10)*100
        amount = (id)*100
        request.session['amount']=id
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        return render(request, "pay.html",{'r':amount})

def success(request):
    a=request.session['c_name']
    b = request.session['s_name']
    c = request.session['amount']
    s = request.session['se_name']
    d=bookingtable.objects.get(customer_name=a,salon_name=b,service_name=s)
    x=d.email
    d1=payment.objects.create(customer_name=a,s_name=b,amount=c,email=x)
    d1.save()
    # d2 = bookingtable.objects.get(customer_name=a,salon_name=b)
    # y=d2.username
    # d3=adpay.objects.create(username=y,amount=10,s_name=b)
    # d3.save()
    d4=bookingtable.objects.filter(customer_name=a,salon_name=b,service_name=s)
    d4.update(status='payment completed')
    return render(request, 'user_page.html')


# user-cancel booking
def paycancel(request):
    if request.method == 'POST':
        a = request.POST['b4']
        b = request.POST['b5']
        c = request.POST['b1']
        e = request.POST['b2']
        f = request.POST['b3']
        d = bookingtable.objects.filter(customer_name=a, username=c, salon_name=e, service_name=f)

        if (b == 'confirm') or (b == 'pending'):
            # Update status only if it's confirm or pending
            d.update(status='Appointment Cancelled')
            return redirect(profile)

        elif b == 'Appointment Cancelled':
            url = 'uviewappt'
            msg = '''<script>alert('already cancelled')
                                           window.location='%s'</script>''' % (url)
            return HttpResponse(msg)


        else:
            url = 'uviewappt'
            msg = '''<script>alert('not allowed.. no refund after payment')
                               window.location='%s'</script>''' % (url)
            return HttpResponse(msg)

    else:
        return render(request, 'user_view_appointment.html')

#salon view confirm booking
def salon_view_confirm(request):
    if request.method == 'GET':
        a = request.session['s_id']
        b = salontable.objects.get(username=a)
        d = bookingtable.objects.filter(salon_name=b.salon_name, status='confirm')
        return render(request, 'salonconfbook.html', {'r': d})
    else:
        return render(request, 'salon_page.html')

#salon view confirmed booking
def salon_payment_view(request):
    if request.method == 'GET':
        a = request.session['s_id']
        b = salontable.objects.get(username=a)
        d = bookingtable.objects.filter(salon_name=b.salon_name, status='payment completed')
        return render(request, 'bookingcomplt.html', {'r': d})
    else:
        return render(request, 'salon_page.html')

#salon view payment
def salon_payments(request):
    a = request.session['s_id']
    d = salontable.objects.get(username=a)
    b = d.salon_name
    d1 = payment.objects.filter(s_name=b)
    return render(request, 'salonpayments.html', {'r': d1})

#salon view total payment on a particular date
def salontotalpayment(request):
    l = []
    if request.method == 'POST':
        a = request.session['s_id']
        v = request.POST['n1']
        d = salontable.objects.get(username=a)
        b = d.salon_name
        d1 = payment.objects.filter(s_name=b, date=v)
        for i in d1:
            a = i.amount
            l.append(a)
        s = sum(l)
        return render(request, 'salonpayments.html', {'s1': s, 'r': d1})
    else:
        return render(request, 'salonpayments.html')

#admin view booking
def admin_view_booking(request):
    d = bookingtable.objects.filter(status='payment completed')
    return render(request, 'adminviewbook.html', {'r': d})

#user send complaint
def comp(request):
    if request.method == 'POST':
        v = request.POST['p1']
        w = request.POST['p2']
        x = request.POST['p3']
        y = request.POST['p4']
        z = request.POST['p5']
        data=complaint.objects.create(username=v,name=w,mobile=x,email=y,complaint=z)
        data.save()
        return render(request, 'complaint.html')
    else:
        a1 = request.session['u_id']
        d=usertable.objects.filter(username=a1)
        return render(request, 'complaint.html',{'r':d})

#user view complaint
def viewcomp(request):
    a = request.session['u_id']
    d = complaint.objects.filter(username=a)
    return render(request, 'userviewcomp.html', {'r': d})

#admin view payment
# def adminviewpay(request):
#     d = adpay.objects.all()
#     return render(request, 'adminviewpayt.html', {'r': d})

# def adminpaytotal(request):
#     l = []
#     if request.method == 'POST':
#         v = request.POST['n1']
#         d = adpay.objects.filter(date=v)
#         for i in d:
#             a = i.amount
#             l.append(a)
#         s = sum(l)
#         return render(request, 'adpayt.html', {'s1': s, 'r': d})
#     else:
#         return render(request, 'adpayt.html')

#admin view complaints
def adminviewcomp(request):
    d = complaint.objects.all()
    return render(request, 'adminviewcomp.html', {'r': d})

def logoutt(request):
    if 'sa_id' in request.session:
        request.session.flush()
        return redirect(profile)

# def admin_view_pay(request):
#     d = payment.objects.all()
#     return render(request, 'adminviewpayt.html', {'r': d})

# def admin_view_total(request):
#     l = []
#     if request.method == 'POST':
#         v = request.POST['n1']
#         d1 = payment.objects.filter(date=v)
#         for i in d1:
#             a = i.amount
#             l.append(a)
#         s = sum(l)
#         return render(request, 'adminviewpayt.html', {'s1': s, 'r': d1})
#     else:
#         return render(request, 'adminviewpayt.html')


def userwarning(request):
        if request.method == 'POST':
            x = request.POST['b3']
            y = request.POST['b2']
            d = usertable.objects.filter(username=x, email=y)
            return render(request, 'warning1.html', {'r': d})
        else:
            return render(request, 'warning1.html')

def uwarning(request):
    if request.method=='POST':
        b = request.POST['n']
        c = request.POST['n1']
        send_mail('Warning Message', c,
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(profile)
    else:
         return render(request, 'warning1.html')

#admin delete user
def deleteuser(request):
    if request.method=='POST':
        a = request.POST['b2']
        d = usertable.objects.get(username=a)
        b=d.email
        d.delete()
        logintable.objects.filter(username=a).delete()
        send_mail('Removed', 'you are removed from  Website',
                  'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(profile)
    else:
        return render(request,'adminuser.html')

# forgot password
# @csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            u = usertable.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        ResetPassword.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot.html')

#reset password
# @csrf_exempt
def reset_password(request, token):
    # Verify token and reset the password
    password_reset = ResetPassword.objects.get(token=token)
    print(token)
    # usr = usertable.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')

        if repeat_password == new_password:
            # usr = password_reset.user.username
            # usr.save()
            u1=password_reset.user.username
            logintable.objects.filter(username=u1).update(password=new_password)

            # password_reset.user.password=new_password
            # password_reset.user.save()
            # # password_reset.delete()
            return redirect(login_details)
    return render(request, 'reset.html', {'token': token})

def adminviewcontact(request):
        d = contact.objects.all()
        print(d)
        return render(request, 'adminviewcontact.html', {'r': d})