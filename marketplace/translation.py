from modeltranslation.translator import register, TranslationOptions
from .models import Genres, Keywords, Author, Books, Quotes, CustomUser, \
    DepositUser, DonateBook, History_User_Book


@register(Genres)
class GenresTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Keywords)
class KeywordsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Books)
class BooksTranslationOptions(TranslationOptions):
    fields = ('full_name','short_name','caption',)


@register(Quotes)
class QuotesTranslationOptions(TranslationOptions):
    fields = ('text', 'author',)
