from django.contrib import admin

# Register your models here.
from AcademicWriting.models import Articles, Group, Task, Work

admin.site.register(Articles)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(Work)
