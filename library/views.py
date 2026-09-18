from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
    books = Book.objects.select_related('author').prefetch_related('categories', 'publication_set__publisher').all()
    return render(request, 'library/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related('author', 'author__profile').prefetch_related(
            'categories', 'publication_set__publisher'
        ),
        pk=pk
    )
    return render(request, 'library/book_detail.html', {'book': book})
