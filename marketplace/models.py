from django.contrib.auth.models import User
from django.db import models


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

    def save(self, *args, **kwargs):
        super(Books, self).save(*args, **kwargs)

        # Создаем дополнительные записи на основе значения quantity
        for _ in range(self.quantity - 1):
            book_copy = Books.objects.create(
                full_name=self.full_name,
                short_name=self.short_name,
                quantity=1,
                language=self.language,
                year=self.year,
                publications=self.publications,
                caption=self.caption,
                img=self.img,
                price=self.price,
                level=self.level,
                is_occupied=self.is_occupied,
                is_removed=self.is_removed,
                is_paper=self.is_paper,
                is_eBook=self.is_eBook,
                is_audio=self.is_audio
            )
            book_copy.save()
            book_copy.genre.set(self.genre.all())
            book_copy.keyword.set(self.keyword.all())
            book_copy.author.set(self.author.all())


    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Книги в едином экз'

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
