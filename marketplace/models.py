from django.contrib.auth.models import User
from django.db import models, transaction


class Genres(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField()
    is_removed = models.BooleanField(verbose_name='Удален ли')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Keywords(models.Model):
    name = models.CharField(max_length=200, verbose_name='Keyword')
    slug = models.SlugField()
    is_removed = models.BooleanField(verbose_name='Удалено ли')

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Ключевые слова'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name='Автор')
    slug = models.SlugField()
    is_removed = models.BooleanField(verbose_name='Удален ли')

    class Meta:
        verbose_name = 'автора'
        verbose_name_plural = 'Авторы книг'

    def __str__(self):
        return self.name


class Books(models.Model):
    LANGUAGE_CHOICES = (
        ('ru', 'Русский'),
        ('uz', "O'zbek"),
        ('en', 'English'),
    )
    genre = models.ManyToManyField(Genres, verbose_name='Жанры')
    keyword = models.ManyToManyField(Keywords, verbose_name='Ключевые слова')
    full_name = models.CharField(max_length=700, verbose_name='Полное Название')
    short_name = models.CharField(max_length=700, verbose_name='Просто Название')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во книг')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name='Язык')
    year = models.IntegerField(verbose_name="Год издания", null=True, blank=True)
    publications = models.IntegerField(verbose_name="Издания", null=True, blank=True)
    author = models.ManyToManyField(Author, verbose_name='Автор')
    caption = models.TextField(verbose_name='Аннотация к книге', null=True, blank=True)
    img = models.ImageField(upload_to='covers/', verbose_name='270x210', null=True, blank=True)
    price = models.IntegerField(verbose_name="Стоимость", null=True, blank=True)
    level = models.IntegerField(verbose_name="Уровень", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления", null=True, blank=True)
    is_occupied = models.BooleanField(verbose_name='Занята ли')
    is_removed = models.BooleanField(verbose_name='Удалена ли')
    is_paper = models.BooleanField(verbose_name='Бумажная книга')
    is_eBook = models.BooleanField(verbose_name='Электронная книга')
    is_audio = models.BooleanField(verbose_name='АудиоКнига')

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Коллекция книг'

    def __str__(self):
        return self.short_name


class Quotes(models.Model):
    text = models.TextField(verbose_name='Цитата', null=True, blank=True)
    author = models.CharField(max_length=700, verbose_name='Автор')
    is_removed = models.BooleanField(verbose_name='Удалено ли')

    class Meta:
        verbose_name = 'цитату'
        verbose_name_plural = 'Цитаты дня'

    def __str__(self):
        return self.author


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    img = models.ImageField(upload_to='covers/', verbose_name='Аватарка', null=True, blank=True)
    phone_number = models.BigIntegerField(verbose_name="Телефон")

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Кастомные пользователи'

    def __str__(self):
        return str(self.phone_number)


class DepositUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Сумма депозита')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата", null=True, blank=True)

    class Meta:
        verbose_name = 'депозит'
        verbose_name_plural = 'Депозиты пользователей'

    def __str__(self):
        return f"Депозит от {self.user.username}"


class DonateBook(models.Model):
    first_name = models.CharField(max_length=700, verbose_name='Имя')
    last_name = models.CharField(max_length=700, verbose_name='Фамилия')
    email = models.CharField(max_length=700, verbose_name='Почта')
    phone_number = models.BigIntegerField(verbose_name="Телефон")
    donateBookList = models.TextField(verbose_name='Информация о книгах', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления", null=True, blank=True)

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Книжные донаты'

    def __str__(self):
        return self.first_name


class History_User_Book(models.Model):
    STATUS_CHOICES = (
        ('1', 'Книга на полке пользователя'),
        ('2', "Ожидает звонка на отправку"),
        ('3', 'Пользователь читает'),
        ('4', 'Ожидает звонка на возврат'),
        ('5', 'Пользователь прочёл'),
    )
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name='Книга', null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='Статус книги')
    first_name = models.CharField(max_length=200, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', null=True, blank=True)
    email = models.CharField(max_length=200, verbose_name='Почта', null=True, blank=True)
    number_phone = models.BigIntegerField(verbose_name="Телефон", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='Адрес', null=True, blank=True)
    date_statement = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки", null=True, blank=True)
    date_sending = models.DateTimeField(verbose_name="Дата отправки", null=True, blank=True)
    date_deadline = models.DateTimeField(verbose_name="Конечная Дата", null=True, blank=True)
    date_return = models.DateTimeField(verbose_name="Дата Возврата", null=True, blank=True)
    user_feedback = models.TextField(verbose_name='Отзыв о пользователе', null=True, blank=True)
    send_quality = models.IntegerField(verbose_name="Качество книги перед отправкой", null=True, blank=True)
    expire_quality = models.IntegerField(verbose_name="Качество книги после возврата", null=True, blank=True)
    is_expired = models.BooleanField(verbose_name='Вернули ?', null=True, blank=True)

    class Meta:
        verbose_name = 'историю'
        verbose_name_plural = 'Читательские истории пользователей'

    def __str__(self):
        return self.first_name
