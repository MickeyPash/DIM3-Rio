from django.contrib import admin

# Register your models here.
from maximatch.models import Researcher, Participant, Experiment, Application

#class UserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'first_name', 'last_name', 'is_staff', \
        #'is_active')

admin.site.register(Researcher)
admin.site.register(Participant)
admin.site.register(Experiment)
admin.site.register(Application)
