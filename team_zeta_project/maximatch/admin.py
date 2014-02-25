from django.contrib import admin

# Register your models here.
from django.contrib import admin
from maximatch.models import *

#class UserAdmin(admin.ModelAdmin):
	#list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')

admin.site.register(Researcher)
#admin.site.register(User, UserAdmin)
admin.site.register(Participant)
admin.site.register(Experiment)
admin.site.register(Application)
