from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
#from callboard.board.models import User

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'