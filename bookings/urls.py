from . import views, adminView
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns=[
     path('',views.bookings,name='bookings'), #bookings page
    
    
    # Admin functionalities
    path('accounts/login',views.Login,name='Login'), #admin login
    path('logout_user/', views.logout_user, name="logout_user"),  #User logout
    
    # URL for Admin 
	path('dashboard/', adminView.dashboard, name="dashboard"), 
	path('dashboard/pendingBookings/', adminView.pendingBookings, name="pendingBookings"),
	path('dashboard/confirmedBookings/', adminView.confirmedBookings, name="confirmedBookings"),
	path('dashboard/completeBookings/', adminView.completedBookings, name="completedBookings"),
	path('dashboard/cancelledBookings/', adminView.cancelledBookings, name="cancelledBookings"),
 

    
    path("dashboard/update-appointment/<int:appointment_id>/<str:action>/", adminView.update_appointment_status, name="update_appointment"),
    path("dashboard/complete-appointment/<int:appointment_id>/<str:action>/", adminView.complete_appointment, name="complete_appointment"),
    

 
    
]



# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']