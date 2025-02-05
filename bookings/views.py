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
            return redirect('login')




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
        
        
        # Get the service instance
        service = get_object_or_404(Services, pk=service)

        # Validate required fields
        if not (firstname and lastname and email and phone and appoint_date and appoint_time):
            return HttpResponse("Missing required fields.", status=400)

        # Create an appointment entry
        try:
            Appointments.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                phoneNumber=phone,
                serviceID=service,
                # size=size,
                appointment_date=appoint_date,
                appointment_time=currentTimestamp,
                created_at=now(),
                status=default_bk_status
            )
            
            message = "Booking created successfully!"
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
        template2 = loader.get_template('AdminTemplates/dashboard.html')
        # return redirect('dashboard')
        return HttpResponse(template2.render(context, request))
        
        
        
        
        
    return HttpResponse(template.render(context, request))



# logout functionality
# @login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('accounts/login')

