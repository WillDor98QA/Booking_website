import random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=Appointments)
def generate_clientID(sender, instance, **kwargs):
    if not instance.clientid:
        while True:
            newID = str(random.randint(100000000, 999999999))  # Generate a 9-digit number
            if not Appointments.objects.filter(clientID=newID).exists():
                instance.clientID = newID
                break