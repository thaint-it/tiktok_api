from django.contrib import admin

from users.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields if field.name != 'password']

admin.site.register(User, UserAdmin)