from django.contrib import admin

from .models import Account, Profile

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username','employee_id', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_active']
    # exclude = ('password',)
    search_fields = ('employee_id',)

admin.site.register(Profile)

