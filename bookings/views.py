from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.template import loader


from .models import *
from .adminView import *

from datetime import datetime , date
from django.utils import timezone
from django.utils.timezone import now

from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

import json

from django.shortcuts import get_object_or_404




#global variables
currentYear = datetime.now().strftime("%Y")
currentDate = datetime.today().strftime("%Y-%m-%d")
currentTimestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")







class CsrfMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            # Redirect to login page if a CSRF error occurs
            return redirect('Login')

# check if booking already exists
def validate_booking(phone):
    

    # Check if phone no. has booked today
    has_been_booked_today = Appointments.objects.filter(phoneNumber=phone, creation_date=currentDate).exists()



    if has_been_booked_today:
        message = "THIS USER HAS ALREADY BOOKED TODAY!"
        return ("BOOKED", message)
    
    else:
        return ("UNUSED", "USER IS UNBOOKED")


# booking functionality
def bookings(request):
    
    currentYear = now().year  # Get the current year 

    default_bk_status = "Pending"
    
    # template = loader.get_template('index.html')
    template = "index.html"
    
    


    

    if request.method == "POST":
        
        #get data from POST request
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        size = request.POST.get('size')
        appoint_date = request.POST.get('date')
        appoint_time = request.POST.get('time')
        
        appointm_date = datetime.strptime(appoint_date, '%Y-%m-%d')
        
        # weeekend verification
        appoint_day = appointm_date.strftime("%A")
        if appointm_date.weekday() < 5:
            messages.error(request, "Appointment Date must be weekend!")
            return redirect(reverse('bookings'))
        
       
        if appoint_date <= date.today().strftime("%Y-%m-%d"):
            messages.error(request, "Appointment Date must be later than current Date!")
            return redirect(reverse('bookings'))

        else:
            # appoint_date = datetime.strptime(appoint_date, "%Y-%m-%d").date() 
            # Get the service instance
            service = get_object_or_404(Services, pk=service)

            # Validate required fields
            if not (firstname and lastname and email and phone and appoint_date and appoint_time):
                return HttpResponse("Missing required fields.", status=400)

            # Check phone number
            status, message = validate_booking(phone)
            
            
            # If the phone has already booked used, add a message and return status
            if status == "BOOKED":
                messages.error(request, message)
                return redirect('bookings')

            # If the phone number has not booked, add it to the appointments table
            if status == "UNUSED":
                # messages.success(request, "PHONE NUMBER HAS NOT BOOKED")
   

        
        
                # Create an appointment entry
                try:
                    Appointments.objects.create(
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        phoneNumber=phone,
                        serviceID=service,
                        # size=size,
                        appointment_date=appointm_date,
                        appointment_time=appoint_time,
                        created_at=now(),
                        creation_date = currentDate,
                        status=default_bk_status
                    )
                    
                    
                    print(appointm_date)
                    print(appoint_time)

                    messages.success(request,"Booking created successfully!")
                except Exception as e:
                    return HttpResponse(f"Error creating booking: {e}", status=500)

    # Context data for rendering the template
    bookings = Appointments.objects.all()
    
    context = {
        'currentYear': currentYear,
        'bookings': bookings
    }
    # print(appoint_time)
    return render(request,template,context)
        
            
        






# begin Admin functionalities #

# login
def Login(request):
    
    
        
    template = loader.get_template('registration/login.html')
    context = {
       
    }
    if request.method == "POST":
    #get data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid email entered...please try again")
            return redirect(Login)
        
        user = authenticate(request,username=username,password=password)
        
        if user is None:
            messages.error(request, "user does not exist!!!")
            return redirect('Login')
        
        login(request,user)
        
        return redirect('/dashboard/')
        
        
        
        
        
        
    return HttpResponse(template.render(context, request))



# logout functionality
# @login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse(Login))

