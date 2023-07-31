from django.contrib import admin
from .models import CustomUser, Ticket
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
   add_fieldsets = (
    (None, {
        'classes':('wide',),
        'fields':('username', 'password1', 'password2', 'role')
    })
   ), 

# admin.site.register(CustomUser, UserAdmin)
admin.site.register(Ticket)
