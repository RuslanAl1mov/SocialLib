from django.shortcuts import render

# Create your views here.


def registration_page(request):
    return render(request, 'authorization/registration.html')


def authorization_page(request):
    return render(request, 'authorization/authorization.html')

def home_page(request):
    return render(request, 'home/home.html')


def book_page(request):
    return render(request, 'book_info/book_page.html')


def category_books_page(request):
    return render(request, 'category_books_page/category_books.html')


def search_result_page(request):
    return render(request, 'search_result_page/search_result.html')


def user_profile_page(request):
    return render(request, 'account/user_account.html')


def books_shelf_page(request):
    return render(request, 'book_shelf_page/book_shelf.html')


def book_donate_page(request):
    return render(request, 'book_donate_page/book_donate.html')


def not_found_page(request):
    return render(request, 'notifications/error_404.html')


def book_reserved_page(request):
    return render(request, 'notifications/book_reserved.html')


def order_book_page(request):
    return render(request, 'order_book/order_book.html')


def order_success_page(request):
    return render(request, 'notifications/order_success.html')


def terms_of_use_page(request):
    return render(request, 'additional_content_pages/oferta.html')


def about_us_page(request):
    return render(request, 'additional_content_pages/about_us.html')


def tech_support_page(request):
    return render(request, 'additional_content_pages/tech_support.html')
