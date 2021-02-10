from django.forms import ModelForm
from .models import Appointment


class MakeForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'client_name', 'message']