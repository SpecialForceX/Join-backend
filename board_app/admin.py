from django.contrib import admin
from .models import Contact, Task, SubTask, LoginData

admin.site.register(Contact)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(LoginData)
