import random
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Genres, Keywords, Author, Books, Quotes


def registration_page(request):
    return render(request, 'authorization/registration.html')


def authorization_page(request):
    return render(request, 'authorization/authorization.html')


def home_page(request):
    unique_books = []
    seen_names = set()

    template = "home/home.html"
    all_quotes = Quotes.objects.all()
    quote_count = all_quotes.count()
    if quote_count >= 4:
        random_quotes = all_quotes.order_by('?')[:4]
    else:
        random_quotes = all_quotes
    all_books = Books.objects.all().filter(is_occupied=0, is_removed=0).order_by('-date')
    for book in all_books:
        if book.full_name not in seen_names:
            unique_books.append(book)
            seen_names.add(book.full_name)

    context = {
        "new_books": unique_books[:10],
        "main_books": unique_books[:16],
        'quotes': random_quotes,
    }
    return render(request, template, context)


def book_page(request, book_id):
    template = 'book_info/book_page.html'
    unique_author_books = []
    seen_author_books = set()
    unique_similar_books = []
    seen_similar_books = set()

    book_info = get_object_or_404(Books, pk=book_id)

    author_books = Books.objects.filter(author__in=book_info.author.all(), is_occupied=0, is_removed=0).exclude(
        pk=book_info.pk)
    for book in author_books:
        if book.full_name not in seen_author_books:
            unique_author_books.append(book)
            seen_author_books.add(book.full_name)

    similar_books = Books.objects.filter(genre__in=book_info.genre.all(), is_occupied=0, is_removed=0).exclude(
        pk=book_info.pk)
    for book in similar_books:
        if book.full_name not in seen_similar_books:
            unique_similar_books.append(book)
            seen_similar_books.add(book.full_name)

    context = {
        "book_info": book_info,
        "author_books": unique_author_books,
        "similar_books": unique_similar_books
    }
    return render(request, template, context)


def category_books_page(request):
    return render(request, 'category_books_page/category_books.html')


def search_result_page(request):
    unique_books = []
    seen_books = set()
    template = 'search_result_page/search_result.html'
    context = {}
    if request.method == "POST":
        search_value = str(request.POST["search_value"]).replace(",", "")
        search_books = Books.objects.filter(
            is_occupied=False,
            is_removed=False,
        ).filter(
            Q(genre__name__icontains=search_value) |
            Q(keyword__name__icontains=search_value) |
            Q(full_name=search_value) |
            Q(short_name=search_value) |
            Q(author__name__icontains=search_value) |
            Q(caption__icontains=search_value)
        )
        for book in search_books:
            if book.full_name not in seen_books:
                unique_books.append(book)
                seen_books.add(book.full_name)
        context['search_books'] = unique_books
        context['search_value'] = search_value
    elif request.method == "GET":
        search_value = request.GET.get('search_value')
        sort_param = request.GET.get('sort')
        search_books = Books.objects.filter(
            is_occupied=False,
            is_removed=False,
        ).filter(
            Q(genre__name__icontains=search_value) |
            Q(keyword__name__icontains=search_value) |
            Q(full_name=search_value) |
            Q(short_name=search_value) |
            Q(author__name__icontains=search_value) |
            Q(caption__icontains=search_value)
        ).order_by(sort_param)
        for book in search_books:
            if book.full_name not in seen_books:
                unique_books.append(book)
                seen_books.add(book.full_name)
        context['search_books'] = unique_books
        context['search_value'] = search_value
    return render(request, template, context)


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
