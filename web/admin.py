from django.contrib import admin
from .models import ContactModel, Team,Project

admin.site.register(ContactModel)
admin.site.register(Team)
admin.site.register(Project)