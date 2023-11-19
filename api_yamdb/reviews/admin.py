from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reviews.models import Comment, Review, User

admin.site.register(User, UserAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'review')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score')