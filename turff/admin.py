
# Register your models here.

from .models import *
from django.contrib import admin


  # Replace the default admin site with your custom admin site
admin.site.register(GameCatagory)
admin.site.register(TurfCatagory)

from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomAdminSite(admin.AdminSite):
    def logout(self, request):
        logout(request)
        return redirect('home')  # Assuming 'home' is the name of your home page URL

admin.site.logout = CustomAdminSite().logout
