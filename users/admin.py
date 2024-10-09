from django.contrib import admin

from users.models import User
from users.models.user import Follower, FolowerActivity

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields if field.name != 'password']

# Register your models here.
class FollowerAdmin(admin.ModelAdmin):
   pass
# Register your models here.
class FollowerActivityAdmin(admin.ModelAdmin):
   pass

admin.site.register(FolowerActivity, FollowerActivityAdmin)
admin.site.register(Follower, FollowerAdmin)