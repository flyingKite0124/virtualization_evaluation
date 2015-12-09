from django.contrib import admin
from ves_ihep.models import *
# Register your models here.

admin.site.register(Scene)
admin.site.register(Script)
admin.site.register(Host)
admin.site.register(Activity)
admin.site.register(SceneHistory)
admin.site.register(ActivityHistory)
