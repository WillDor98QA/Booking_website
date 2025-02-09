

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, redirect
from django.template import loader


from .models import *
from datetime import datetime , date
from django.utils import timezone
from django.utils.timezone import now

from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


#global variables
currentYear = datetime.now().strftime("%Y")
currentDate = datetime.today().strftime("%Y-%m-%d")
currentTimestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")





@login_required
def dashboard(request):
    template = loader.get_template('AdminTemplates/dashboard.html')
    appointments = Appointments.objects.all()
    
    pending_count   =  Appointments.objects.filter(status='pending').count() 
    confirmed_count = Appointments.objects.filter(status='confirmed').count()
    cancelled_count =  Appointments.objects.filter(status='cancelled').count() 
    completed_count =  Appointments.objects.filter(status='completed').count() 
    pending_List    =  Appointments.objects.all()
    
    
    
    
    context = {
        "appointments" : pending_List,
        "pending_count" :pending_count,
        "confirmed_count" : confirmed_count,
        "cancelled_count" : cancelled_count,
        "completed_count" : completed_count,
    }
    return HttpResponse(template.render(context, request))



@login_required
def pendingBookings(request):
    template = loader.get_template('AdminTemplates/pending.html')
    
    
    pending_List  = Appointments.objects.filter(status='pending')
    context = {
    
        "appointments" : pending_List,
        
    }
    return HttpResponse(template.render(context, request))

@login_required
def confirmedBookings(request):
    template = loader.get_template('AdminTemplates/confirmed.html')
    confirmed_list =  Appointments.objects.filter(status='confirmed')
    context = {
        "appointments" : confirmed_list,
        
    }
    return HttpResponse(template.render(context, request))


@login_required
def completedBookings(request):
    
    template = loader.get_template('AdminTemplates/completed.html')
    
    completed_count = Appointments.objects.filter(status='completed')
    context = {
        
        "appointments" : completed_count,
        
    }
    return HttpResponse(template.render(context, request))


@login_required
def cancelledBookings(request):
    template = loader.get_template('AdminTemplates/cancelled.html')
    cancelled_count =Appointments.objects.filter(status='cancelled')
    context = {
        "appointments" : cancelled_count,
    }
    return HttpResponse(template.render(context, request))


