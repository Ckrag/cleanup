from django.contrib import admin

# Register your models here.
from public.models import CleanRoute, CleanNode

admin.site.register(CleanRoute)
admin.site.register(CleanNode)
