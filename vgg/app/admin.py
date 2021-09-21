from django.contrib import admin
# from django.contrib.auth.models import Permission

from .models import *




admin.site.register(Account)
admin.site.register(Test)
admin.site.register(Materials)
admin.site.register(Course)
<<<<<<< HEAD
admin.site.register(Expert_support)
=======
admin.site.register(Question)
>>>>>>> 5df31354b485560559c873ebb472bf87da323a2d

admin.site.register(JWT)