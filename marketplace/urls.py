from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('registration', views.registration_page, name='registration'),
    path('authorization', views.authorization_page, name='authorization'),
    path('log_out/', views.log_out, name='log_out'),
    path('book/<int:book_id>/', views.book_page, name='book'),
    path('favorites/<int:book_id>/', views.favorites, name='favorites'),
    path('del_favorites/<int:book_id>/', views.del_favorites, name='del_favorites'),
    path('category/<int:category_id>/', views.category_books_page, name='category_books'),
    path('book_search', views.search_result_page, name='book_search'),
    path('profile/<int:tab_id>/', views.user_profile_page, name='user_profile'),
    path('book_shelf', views.books_shelf_page, name='book_shelf'),
    path('book_donate', views.book_donate_page, name='book_donate'),
    path('order_book/<int:book_id>/', views.order_book_page, name='order_book'),
    path('return_to_book/<int:id>/', views.return_to_book, name='return_to_book'),

    path('page_not_found', views.not_found_page, name='page_not_found'),
    path('book_is_reserved', views.book_reserved_page, name='book_reserved'),
    path('success_order', views.order_success_page, name='order_success'),

    path('terms_of_use', views.terms_of_use_page, name='terms_of_use'),
    path('about', views.about_us_page, name='about_us'),
    path('support', views.tech_support_page, name='tech_support')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

