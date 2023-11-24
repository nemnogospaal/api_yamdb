from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

#class CommentResource(resources.ModelResource):

#    class Meta:
#        model = Comment

#@admin.register(Comment)
#class CommentAdmin(admin.ModelAdmin):
#    list_display = ('text', 'author', 'reviews')


class ReviewResource(resources.ModelResource):

    class Meta:
        model = Review

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('text', 'author', 'score')



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

    resource_classes = [ReviewResource]

admin.site.register(User, UserAdmin)

# класс обработки данных
class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category

# вывод данных на странице
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title

@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre

@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


class GenreTitleResource(resources.ModelResource):

    class Meta:
        model = GenreTitle

@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]


class UserResource(resources.ModelResource):

    class Meta:
        model = User

#@admin.register(User)
#class UserAdmin(ImportExportModelAdmin):
#    resource_classes = [UserResource]



