from django.contrib import admin

from reviews.models import Comment, Raiting, Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'reviews')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'raiting')


@admin.register(Raiting)
class RaitingAdmin(admin.ModelAdmin):
    list_display = ('raiting', 'author', 'title')
