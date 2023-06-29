import random, telebot
from decimal import Decimal
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Genres, Keywords, Author, Books, Quotes, CustomUser, DonateBook, History_User_Book, DepositUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


token = "6163259210:AAFHkTsuNjxty3wQNSZUdQDd3oO83i7hvqU"
bot = telebot.TeleBot(token)


def registration_page(request):
    template = 'authorization/registration.html'
    if request.method == "POST":
        user_check = User.objects.filter(username=request.POST["email"]).exists()
        if user_check:
            return redirect('authorization')
        else:
            user = User.objects.create_user(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                username=request.POST["email"],
                email=request.POST["email"],
                password=request.POST["password"]
            )
            user.save()
            custom_user = CustomUser(user=user, phone_number=request.POST['phone_number'])
            custom_user.save()
            user = authenticate(username=request.POST["email"], password=request.POST["password"])
            login(request, user)
            text = f"‼️ #Новая_Регистрация ‼️ \n\n"
            text += f"🆔 ФИО: {request.POST['first_name']} {request.POST['last_name']}\n"
            text += f"☎️Номер телефона: {request.POST['phone_number']}\n"
            bot.send_message(-983213057, text)
            return redirect('home')
    else:
        return render(request, template)


def authorization_page(request):
    template = 'authorization/authorization.html'
    if request.method == "POST":
        user = authenticate(username=request.POST["email"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, template)
    else:
        return render(request, template)


def log_out(request):
    logout(request)
    return redirect('home')


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
        'list_category': Genres.objects.all()
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
    books_being_read = History_User_Book.objects.filter(status='3', book__full_name=book_info.full_name)
    count_being_read = books_being_read.count()
    books_already_read = History_User_Book.objects.filter(status='5', book__full_name=book_info.full_name)
    count_already_read = books_already_read.count()
    book_count = Books.objects.filter(full_name=book_info.full_name).count()

    context = {
        "book_info": book_info,
        "books_currently_reading": count_being_read,
        "books_already_read": count_already_read,
        "total_books": book_count,
        "list_category": Genres.objects.all(),
        "author_books": unique_author_books,
        "similar_books": unique_similar_books
    }
    return render(request, template, context)


def favorites(request, book_id):
    book_info = get_object_or_404(Books, pk=book_id)
    user = request.user
    custom_user = get_object_or_404(CustomUser, user=user)
    order_info = History_User_Book.objects.filter(book__full_name=book_info.full_name, status=1,
                                               first_name=user.first_name,
                                               last_name=user.last_name, email=user.email)
    if order_info:
        pass
    else:
        new_history = History_User_Book(
            book = book_info,
            status = 1,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            number_phone = custom_user.phone_number)
        new_history.save()
    return redirect('book_shelf')

def del_favorites(request, book_id):

    user = request.user
    custom_user = get_object_or_404(CustomUser, user=user)
    new_history = get_object_or_404(History_User_Book,
                                    book = get_object_or_404(Books, pk=book_id),
                                    status = 1,
                                    first_name = user.first_name,
                                    last_name = user.last_name,
                                    email = user.email,
                                    number_phone = custom_user.phone_number)
    new_history.delete()
    return redirect('book_shelf')


def category_books_page(request, category_id):
    template = 'category_books_page/category_books.html'
    unique_books = []
    seen_books = set()
    list_books = Books.objects.filter(genre__id=category_id, is_occupied=0, is_removed=0)
    if request.method == "GET":
        sort_param = request.GET.get('sort')
        if sort_param:
            list_books = Books.objects.filter(genre__id=category_id, is_occupied=0, is_removed=0).order_by(sort_param)

    for book in list_books:
        if book.full_name not in seen_books:
            unique_books.append(book)
            seen_books.add(book.full_name)
    context = {
        "books_list": unique_books,
        'list_category': Genres.objects.all(),
        'name_category': Genres.objects.get(id=category_id)
    }
    return render(request, template, context)


def search_result_page(request):
    unique_books = []
    seen_books = set()
    template = 'search_result_page/search_result.html'
    context = {'list_category': Genres.objects.all(),}
    if request.method == "POST":
        search_value = str(request.POST["search_value"]).replace(",", "")
        search_type = request.POST["search_type"] if "search_type" in request.POST else ""
        if search_type == "" or search_type == "Все":
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
        elif search_type == "Название":
            search_books = Books.objects.filter(
                is_occupied=False,
                is_removed=False,
            ).filter(
                Q(full_name=search_value) |
                Q(short_name=search_value))
        elif search_type == "Жанр":
            search_books = Books.objects.filter(
                is_occupied=False,
                is_removed=False,
            ).filter(
                Q(genre__name__icontains=search_value) |
                Q(keyword__name__icontains=search_value))
        elif search_type == "Автор":
            search_books = Books.objects.filter(
                is_occupied=False,
                is_removed=False,
            ).filter(
                Q(author__name__icontains=search_value))

        for book in search_books:
            if book.full_name not in seen_books:
                unique_books.append(book)
                seen_books.add(book.full_name)
        context['search_books'] = unique_books
        context['search_value'] = search_value
        context['search_quantity'] = len(unique_books)
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
        context['search_quantity'] = len(unique_books)
    context['list_category'] = Genres.objects.all()
    return render(request, template, context)


def user_profile_page(request, tab_id):
    template = 'account/user_account.html'
    user = request.user
    read_book_count = History_User_Book.objects.filter(status=5, first_name=user.first_name,
                                                  last_name=user.last_name, email=user.email).count()

    donate_book = DonateBook.objects.filter(first_name=user.first_name, last_name=user.last_name).count()

    deposit_user = DepositUser.objects.filter(user=user)
    total_amount = 0

    for deposit in deposit_user:
        total_amount += deposit.amount

    min_value = -165
    max_value = 403
    num_levels = 15
    step = (max_value - min_value) / num_levels

    level = int(total_amount / 100000)

    bottom = int(min_value + level * step) + 15
    tipa_water = level * 38 +15

    context = {"tab": tab_id,
               'list_category': Genres.objects.all(),
               "read_books": read_book_count,
                "help_pro": donate_book,
               'bottom':bottom,
               'tipa_water':tipa_water,
               'level': level,
               'total_amount': total_amount}

    if request.method == "POST":
        user = request.user
        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.username = request.POST['email']
            user.save()
            custom_user = get_object_or_404(CustomUser, user=user)
            custom_user.phone_number = request.POST['phone_number']
            if 'user_avatar' in request.FILES:
                custom_user.img = request.FILES['user_avatar']
            custom_user.save()
        elif 'past_password' in request.POST:
            if user.check_password(request.POST['past_password']) and request.POST['new_password'] == request.POST[
                'new_password_replay']:
                user.set_password(request.POST['new_password'])
                user.save()
            else:
                context["tab"] = 2
                return render(request, template, context)

    return render(request, template, context)


def withdraw_money(request):
    user = request.user
    custom_user = get_object_or_404(CustomUser, user=user)

    text = f"‼️ #Обнулил_Депозит ‼️ \n\n"
    text += f"🆔 ФИО: {user.first_name} {user.last_name}\n"
    text += f"☎️Номер телефона: {custom_user.phone_number}\n"
    text += f"ℹ️️У меня бешеное желание обнулить депозит\n"
    bot.send_message(-983213057, text)
    return redirect('home')


def books_shelf_page(request):
    template = 'book_shelf_page/book_shelf.html'
    user = request.user

    context = {
        'list_category': Genres.objects.all(),
    "stat_1_books" : History_User_Book.objects.all().filter(status=1, first_name=user.first_name, last_name=user.last_name, email=user.email),
    "stat_2_books" : History_User_Book.objects.all().filter(status=2, first_name=user.first_name, last_name=user.last_name, email=user.email),
    "stat_4_books" : History_User_Book.objects.all().filter(status=4, first_name=user.first_name, last_name=user.last_name, email=user.email),
    "stat_3_books" : History_User_Book.objects.all().filter(status=3, first_name=user.first_name, last_name=user.last_name, email=user.email),
    "stat_5_books" : History_User_Book.objects.all().filter(status=5, first_name=user.first_name, last_name=user.last_name, email=user.email)
               }
    return render(request, template, context)


def book_donate_page(request):
    template = 'book_donate_page/book_donate.html'
    context = {'list_category': Genres.objects.all(),}
    if request.method == "POST":
        donate = DonateBook(
            first_name= request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            phone_number = request.POST['phone_number'],
            donateBookList = request.POST['product_keywords_ru']
        )
        donate.save()
        text = f"‼️ #Новый_Донат ‼️ \n\n"
        text += f"🆔 ФИО: {request.POST['first_name']} {request.POST['last_name']}\n"
        text += f"☎️Номер телефона: {request.POST['phone_number']}\n"
        text += f"ℹ️️Информация о книгах: {request.POST['product_keywords_ru']}\n"
        bot.send_message(-983213057, text)

    return render(request, template, context)


def not_found_page(request):
    return render(request, 'notifications/error_404.html', {'list_category': Genres.objects.all(),})


def book_reserved_page(request):
    return render(request, 'notifications/book_reserved.html')


def order_book_page(request, book_id):
    if request.method == "POST" and request.POST['order_id'] != "None": # Оформление книги
        order_info = get_object_or_404(History_User_Book, id=int(request.POST['order_id'])) # Информация о брони книги со стороны пользователя
        if order_info.book.is_occupied: # Если занята
            new_book_info = Books.objects.all().filter(is_occupied=0, is_removed=0, full_name=order_info.book.full_name).first()
            if new_book_info:  # Поиск такой же книги (свободной) в базе
                order_info.book = new_book_info
                order_info.status = 2
                order_info.first_name = request.POST['first_name']
                order_info.last_name = request.POST['last_name']
                order_info.number_phone = request.POST['phone_number']
                order_info.address = request.POST['address']
                order_info.save()
                text = f"‼️ #Забрать_Книгу ‼️ \n\n"
                text += f"🆔 ФИО: {request.POST['first_name']} {request.POST['last_name']}\n"
                text += f"☎️Номер телефона: {request.POST['phone_number']}\n"
                text += f"🌍️ Адрес: {request.POST['address']}\n"
                text += f"📚 Книга: {order_info.book.full_name}\n"
                bot.send_message(-983213057, text)
                return redirect("order_success")
            else:
                return redirect("book_reserved")
        elif order_info.book.is_removed: # Если книги удалена
            return redirect("book_reserved")
        else: # Книги свободна и не удалена при оформлении
            order_info.status = 2
            order_info.first_name = request.POST['first_name']
            order_info.last_name = request.POST['last_name']
            order_info.number_phone = request.POST['phone_number']
            order_info.address = request.POST['address']
            order_info.save()
            text = f"‼️ #Забрать_Книгу ‼️ \n\n"
            text += f"🆔 ФИО: {request.POST['first_name']} {request.POST['last_name']}\n"
            text += f"☎️Номер телефона: {request.POST['phone_number']}\n"
            text += f"🌍️ Адрес: {request.POST['address']}\n"
            text += f"📚 Книга: {order_info.book.full_name}\n"
            bot.send_message(-983213057, text)
            return redirect("order_success")

    else: # Просто страница оформления
        template = 'order_book/order_book.html'
        previous_page = request.META.get('HTTP_REFERER', None)


        book_info = get_object_or_404(Books, pk=book_id)
        books_being_read = History_User_Book.objects.filter(status='3', book__full_name=book_info.full_name)
        count_being_read = books_being_read.count()
        books_already_read = History_User_Book.objects.filter(status='5', book__full_name=book_info.full_name)
        count_already_read = books_already_read.count()
        book_count = Books.objects.filter(full_name=book_info.full_name).count()
        context = {'previous_page': previous_page,
                   'list_category': Genres.objects.all(),
                   "books_currently_reading": count_being_read,
                   "books_already_read": count_already_read,
                   "total_books": book_count,
                   }
        user = request.user
        user_booked_book = History_User_Book.objects.filter(first_name=user.first_name,
                                                   last_name=user.last_name, email=user.email,
                                                         status__in=['2', '3', '4'])
        if user_booked_book:
            return render(request, 'notifications/user_booked_book.html')
        else:
            order_info = History_User_Book.objects.get(book__full_name=book_info.full_name, status=1, first_name=user.first_name,
                                                       last_name=user.last_name, email=user.email)
            if book_info.is_occupied == 0  and book_info.is_removed == 0: # Книга свободна и не занята
                context["book_info"] = book_info
                context["order_id"] = order_info.id
                return render(request, template, context)
            else: # Книга либо занята либо удалена, страница заявки (поведение страницы)
                new_book_info = Books.objects.all().filter(is_occupied=0, is_removed=0, full_name=book_info.full_name).first()
                if new_book_info: # Если такая же книга есть в базе
                    context["book_info"] = new_book_info
                    context["order_id"] = order_info.id
                    return render(request, template, context)
                else:
                    return redirect("book_reserved")





def return_to_book(request, id):
    order_info = get_object_or_404(History_User_Book, pk=id)
    order_info.status = 4
    order_info.save()
    text = f"‼️ #Возврат_Книги ‼️ \n\n"
    text += f"🆔 ФИО: {order_info.first_name} {order_info.last_name}\n"
    text += f"☎️Номер телефона: {order_info.number_phone}\n"
    text += f"🌍️ Адрес: {order_info.address}\n"
    text += f"📚 Книга: {order_info.book.full_name}\n"
    bot.send_message(-983213057, text)
    return render(request, 'notifications/return_success.html', {'list_category': Genres.objects.all(),})




def order_success_page(request):
    return render(request, 'notifications/order_success.html', {'list_category': Genres.objects.all(),})


def terms_of_use_page(request):
    return render(request, 'additional_content_pages/oferta.html', {'list_category': Genres.objects.all(),})


def about_us_page(request):
    return render(request, 'additional_content_pages/about_us.html', {'list_category': Genres.objects.all(),})


def tech_support_page(request):
    return render(request, 'additional_content_pages/tech_support.html', {'list_category': Genres.objects.all(),})
