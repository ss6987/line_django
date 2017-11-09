from django.contrib import admin
from line_app.models import Relationship,User,Room,Talk
# Register your models here.
admin.site.register(Relationship)
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Talk)
