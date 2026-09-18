from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True)
    birth_place = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'author profiles'

    def __str__(self):
        return f'Perfil de {self.author}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    language = models.CharField(max_length=50, default='Español')
    publication_date = models.DateField()
    categories = models.ManyToManyField(Category, related_name='books', blank=True)
    publishers = models.ManyToManyField(Publisher, through='Publication', related_name='books')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Publication(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    edition = models.CharField(max_length=50)

    class Meta:
        unique_together = ('book', 'publisher')

    def __str__(self):
        return f'{self.book} - {self.publisher} ({self.edition})'
