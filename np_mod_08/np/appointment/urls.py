from django.urls import path
from .views import AppointmentView

urlpatterns=[
    path('appointment/', AppointmentView.as_view(), name='appointment'),
    #path('appointment/', AppointmentView.as_view(), name='appointment'),
    ]