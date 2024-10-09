from django.contrib import admin

from posts.models import Post,Message,Like,Activity

# Register your models here.
class PostAdmin(admin.ModelAdmin):
   pass

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
   pass

# Register your models here.
class LikeAdmin(admin.ModelAdmin):
   pass

# Register your models here.
class ActivityAdmin(admin.ModelAdmin):
   pass


admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Activity, LikeAdmin)
# admin.site.register(Favorite, Favorite)