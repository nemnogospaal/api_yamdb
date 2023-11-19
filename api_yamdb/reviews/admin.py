from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reviews.models import Comment, Review, User


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'reviews')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'score')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    list_display_links = ('pk', 'username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('role', 'first_name', 'last_name')
    list_filter = ('role',)
