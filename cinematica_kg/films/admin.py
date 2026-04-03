from django.contrib import admin
from .models import Film , Genre , Director , Rview

# Register your models here.
admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Rview)