from django.contrib import admin
from .models import *
from .views import default_dict


# Register your models here.

class SuperAdmin(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title = default_dict['app_name']
    admin.site.index_title = f"{default_dict['app_name']}'s Admin"
    empty_value_display = '-empty-'
    
    list_per_page = 10

class RoleAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'Role')
    list_filter = list_display
    
    
class MasterAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'Email', 'Role', 'IsActive')
    list_filter = ('Role', 'IsActive')

models_list = [  Citizen, Department]
roles = ['citizen','department']
if not len(Role.objects.all()):
    for role in roles:
        Role.objects.create(Role=role)
        
for model in models_list:
    admin.site.register(model, SuperAdmin)

admin.site.register(Role, RoleAdmin)
admin.site.register(Master, MasterAdmin)




admin.site.register(Complaint)
admin.site.register(E_fir)
admin.site.register(Accident)
admin.site.register(Police_Varification)
admin.site.register(Report)
admin.site.register(Passport_Status)
admin.site.register(Lost_Parson)