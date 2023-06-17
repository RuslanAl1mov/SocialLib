from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('book', views.book_page, name='book'),
    path('category', views.category_books_page, name='category_books'),
    path('book_search', views.search_result_page, name='book_search'),
    path('profile', views.user_profile_page, name='user_profile'),
    path('book_shelf', views.books_shelf_page, name='book_shelf'),
    path('book_donate', views.book_donate_page, name='book_donate')
]

