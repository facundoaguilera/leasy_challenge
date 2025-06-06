from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import EmailAuthenticationForm
from django.urls import reverse
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = EmailAuthenticationForm
    def get_success_url(self):
        user = self.request.user
        # if user.groups.filter(name='ventas').exists():
        #     return reverse('ventas-dashboard')
        # elif user.groups.filter(name='operaciones').exists():
        #     return reverse('operaciones-dashboard')
        # elif user.groups.filter(name='cobranzas').exists():
        #     return reverse('cobranzas-dashboard')
        return reverse('default-dashboard')
class CustomLogoutView(LogoutView):
    next_page = 'login'
