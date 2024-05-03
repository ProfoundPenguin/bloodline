from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Login)
admin.site.register(VisitorInfo)
admin.site.register(Request)
admin.site.register(RenderedTree)
