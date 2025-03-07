from django import template
from ..models import *

register = template.Library()






@register.filter
def get_service_details(service_id):
    try:
        # Fetch service and return the serviceName
        appointment = Services.objects.get(serviceID=service_id)
        return appointment.serviceID.serviceName
    except appointment.DoesNotExist:
        return "Service not found"


@register.filter
def get_appointment_time(phone, appoint_time):
    try:
        appoint_time = appointment_time.objects.get(phoneNumber=phone)
        return appoint_time.status
    except ObjectDoesNotExist:
        return "Appointment time not found"
