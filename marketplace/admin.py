from django.contrib import admin
from .models import Genres, Keywords, Author, Books, Quotes


class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class KeywordsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class BooksAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'caption', 'level', 'is_occupied', 'is_removed', 'language')
    list_filter = ('is_occupied', 'is_removed', 'level', 'language')
    list_editable = ('is_occupied', 'is_removed',)
    search_fields = ('short_name', 'full_name', 'genre__name', 'keyword__name', 'author__name')


class QuotesAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'is_removed')
    list_filter = ('author',)
    list_editable = ('is_removed',)
    search_fields = ('author', 'text',)


admin.site.register(Genres, GenresAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Quotes, QuotesAdmin)
