from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PostModel, FollowUnFollowModel, CommentModel, LikeModel
from .models import GeneralInfoModel

@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'date_updated')
    search_fields = ('title', 'body')
    list_filter = ('date_updated', 'date_created')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('creator',)

admin.site.register(FollowUnFollowModel)

@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_created')
    list_filter = ('date_created',)
    raw_id_fields = ('user', 'post', 'reply')

admin.site.register(LikeModel)

class GIModelInline(admin.StackedInline):
    model = GeneralInfoModel
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (GIModelInline,)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)