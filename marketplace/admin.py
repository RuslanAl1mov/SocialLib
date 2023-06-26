from django.contrib import admin

from .models import Genres, Keywords, Author, Books, Quotes, CustomUser, \
    DepositUser, DonateBook, History_User_Book
from modeltranslation.admin import TranslationAdmin

class GenresAdmin(TranslationAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }



class KeywordsAdmin(TranslationAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }



class AuthorAdmin(TranslationAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


class BooksAdmin(TranslationAdmin):
    list_display = ('short_name', 'caption', 'level', 'is_occupied', 'is_removed', 'language')
    list_filter = ('is_occupied', 'is_removed', 'level', 'language')
    list_editable = ('is_occupied', 'is_removed',)
    search_fields = ('short_name', 'full_name', 'genre__name', 'keyword__name', 'author__name')


class QuotesAdmin(TranslationAdmin):
    list_display = ('text', 'author', 'is_removed')
    list_filter = ('author',)
    list_editable = ('is_removed',)
    search_fields = ('author', 'text',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone_number', 'get_email')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = 'Full Name'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'



class DepositUserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'amount', 'date')
    search_fields = ('get_full_name', 'amount', 'date')

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = 'Full Name'



class DonateBookAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'date')
    search_fields = ('first_name', 'last_name')
    list_filter = ('date',)


class History_User_BookAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'number_phone', 'address', 'get_book_id', 'get_book_short_name', 'status', 'date_sending', 'date_deadline',)
    list_filter = ('status', 'is_expired')
    list_editable = ('status', 'date_sending', 'date_deadline',)
    search_fields = ('first_name', 'last_name', 'book__short_name', 'address', 'number_phone')

    def get_book_short_name(self, obj):
        return obj.book.short_name

    def get_book_id(self, obj):
        return obj.book.id

    get_book_id.short_description = 'ID Книги'
    get_book_short_name.short_description = 'Наименование книги'



admin.site.register(Genres, GenresAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(Quotes, QuotesAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DepositUser, DepositUserAdmin)
admin.site.register(DonateBook, DonateBookAdmin)
admin.site.register(History_User_Book, History_User_BookAdmin)

