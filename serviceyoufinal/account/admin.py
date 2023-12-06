from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Worker)
admin.site.register(Service)
admin.site.register(ServiceRequest)
admin.site.register(Payment)
admin.site.register(RateService)
admin.site.register(PostService)
# Register your models here.
