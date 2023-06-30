from modeltranslation.translator import register, TranslationOptions
from .models import Genres, Keywords, Author, Quotes, CustomUser, \
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



@register(Quotes)
class QuotesTranslationOptions(TranslationOptions):
    fields = ('text', 'author',)
