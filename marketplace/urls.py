from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('registration', views.registration_page, name='registration'),
    path('authorization', views.authorization_page, name='authorization'),
    path('book/<int:book_id>/', views.book_page, name='book'),
    path('category', views.category_books_page, name='category_books'),
    path('book_search', views.search_result_page, name='book_search'),
    path('profile', views.user_profile_page, name='user_profile'),
    path('book_shelf', views.books_shelf_page, name='book_shelf'),
    path('book_donate', views.book_donate_page, name='book_donate')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
