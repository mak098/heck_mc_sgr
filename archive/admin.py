from django.contrib import admin
from .models import Folder,Letter

class FoldeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Folder,FoldeAdmin)
class FileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Letter, FileAdmin)
