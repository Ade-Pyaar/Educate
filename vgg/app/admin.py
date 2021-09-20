from django.contrib import admin
# from django.contrib.auth.models import Permission

from .models import *




admin.site.register(Account)
admin.site.register(Test)
admin.site.register(Materials)
admin.site.register(Course)
admin.site.register(Question)

admin.site.register(JWT)