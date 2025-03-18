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