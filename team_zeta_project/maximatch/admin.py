from django.contrib import admin

# Register your models here.
from django.contrib import admin
from maximatch.models import *

admin.site.register(Researcher)
admin.site.register(Participant)
admin.site.register(Experiment)
admin.site.register(Application)