from django.db import models

# class Clients(models.Model):
#     clientid = models.AutoField(db_column='clientID', primary_key=True)
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     email = models.EmailField(unique=True, max_length=50)
#     phonenumber = models.CharField(db_column='phoneNumber', max_length=10, null=True, blank=True)
#     datecreated = models.DateTimeField(db_column='dateCreated', auto_now_add=True)

#     def __str__(self):
#         return f"{self.firstname} {self.lastname}"

#     class Meta:
#         managed = False
#         db_table = 'Clients'


class Services(models.Model):
    serviceid = models.AutoField(db_column='serviceID', primary_key=True)
    servicename = models.CharField(db_column='serviceName', max_length=100)
    servicedescription = models.CharField(db_column='serviceDescription', max_length=250, null=True, blank=True)
    active = models.BooleanField(default=True)
    size_options = models.CharField(
        max_length=50,
        choices=[
            ('Extra Small', 'Extra Small'),
            ('Small', 'Small'),
            ('Medium', 'Medium'),
            ('Jumbo', 'Jumbo')
        ],
        default='Medium'
    )
    duration_minutes = models.IntegerField()

    def __str__(self):
        return self.servicename

    class Meta:
        managed = False
        db_table = 'Services'


    

class Appointments(models.Model):
    appointmentid = models.AutoField(db_column='appointmentID', primary_key=True)
    clientid = models.IntegerField(db_column='clientID')
    serviceID = models.ForeignKey(Services, on_delete=models.CASCADE, db_column='serviceID')
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField( max_length=50)
    phoneNumber = models.CharField(db_column='phoneNumber', max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)
    appointment_time = models.DateTimeField()
    
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Cancelled', 'Cancelled'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Appointment {self.appointmentid}"
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        managed = False
        db_table = 'Appointments'


class Timeslots(models.Model):
    timeslotid = models.AutoField(db_column='timeslotID', primary_key=True)
    appointmentid = models.ForeignKey(Appointments, on_delete=models.CASCADE, db_column='appointmentID')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    slot_date = models.DateField()

    def __str__(self):
        return f"Timeslot {self.timeslotid}"

    class Meta:
        managed = False
        db_table = 'Timeslots'




class ConfirmedBookings(models.Model):
    appointmentID = models.OneToOneField('Appointments', on_delete=models.CASCADE, primary_key=True)
    clientID = models.IntegerField()
    serviceID = models.ForeignKey('Services', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phoneNumber = models.CharField(max_length=10, null=True, blank=True)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('Confirmed', 'Confirmed')], default='Confirmed')

    class Meta:
        verbose_name_plural = "Confirmed Bookings"

