from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Intent)
admin.site.register(Example)
admin.site.register(Story)
admin.site.register(CustomAction)
admin.site.register(Responses)
admin.site.register(PolicyInformation)
admin.site.register(Entity)