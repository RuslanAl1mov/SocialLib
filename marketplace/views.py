from django.shortcuts import render

# Create your views here.


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
