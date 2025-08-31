"""Вью приложения."""

import random

from django.shortcuts import (render,
                              redirect,
                              get_object_or_404,
)
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q

from backend.forms import QuoteForm, SourceForm, RegisterForm
from backend.models import Quote, Source, QuoteVote
from backend.constants import NUM_QUOTES_PER_PAGE, NUM_SOURCES_PER_PAGE

User = get_user_model()


@login_required
def add_quote(request):
    """Добавление цитаты."""
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.added_by = request.user
            quote.save()
            return redirect('quotes_list')  # или куда надо
    else:
        form = QuoteForm()
    return render(request, 'backend/add_quote.html', {'form': form})


def quotes_list(request):
    """Страница списка цитат."""
    page_number = request.GET.get("page", 1)

    quotes = Quote.objects.annotate(
        likes_count=Count('votes', filter=Q(votes__value=1)),
        dislikes_count=Count('votes', filter=Q(votes__value=-1))
    ).order_by("-id")
    paginator = Paginator(quotes, NUM_QUOTES_PER_PAGE)  # 10 цитат на страницу

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "backend/quotes_list.html",
        {
            "quotes": page_obj.object_list,
            "page_obj": page_obj,
        },
    )


def source_detail(request, source_id):
    """Страница цитат одного источника."""
    source = get_object_or_404(Source, pk=source_id)
    quotes = Quote.objects.filter(source=source)
    return render(request,
                  "backend/source_detail.html",
                  {"quotes": quotes, "source": source}
    )

@login_required
def add_source(request):
    """Добавление источника."""
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('source_success')  # или нужный вам редирект
    else:
        form = SourceForm()
    return render(request, 'backend/add_source.html', {'form': form})


def source_success(request):
    """Успех добавления источника."""
    return render(request, 'backend/source_success.html')


def source_list(request):
    """Список источников."""
    sources = Source.objects.all().order_by('name')
    paginator = Paginator(sources, NUM_SOURCES_PER_PAGE)  # Показывать по 10 источников на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'backend/source_list.html', {'page_obj': page_obj})


def quote_success(request):
    """Успех добавления цитаты."""
    return render(request, 'backend/quote_success.html')


def register(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')  # перенаправление на страницу входа
    else:
        form = RegisterForm()
    return render(request, 'backend/register.html', {'form': form})


def random_weighted_quote(request):
    """Страница случайной цитаты."""
    quotes = Quote.objects.annotate(
        likes_count=Count('votes', filter=Q(votes__value=1)),
        dislikes_count=Count('votes', filter=Q(votes__value=-1))
    )
    weighted_quotes = [
        (quote, float(quote.weight)) for quote in quotes if quote.weight > 0
    ]
    if not weighted_quotes:
        quote = None
    else:
        items, weights = zip(*weighted_quotes)
        quote = random.choices(items, weights=weights, k=1)[0]
        Quote.objects.filter(pk=quote.pk).update(views=quote.views + 1)
        quote.refresh_from_db()
    return render(request, 'backend/weighted_random.html', {'quote': quote})

@login_required
def vote_quote(request):
    """Добавление лайка или дизлайка."""
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        value = int(request.POST.get('value'))  # 1 или -1
        quote = get_object_or_404(Quote, id=quote_id)
        vote, created = QuoteVote.objects.update_or_create(
            user=request.user, quote=quote,
            defaults={'value': value}
        )
        # Подсчёт лайков и дизлайков
        likes = quote.votes.filter(value=1).count()
        dislikes = quote.votes.filter(value=-1).count()
        return JsonResponse({'likes': likes, 'dislikes': dislikes})
    return JsonResponse({'error': 'Некорректный запрос'}, status=400)


def top_quotes(request):
    """Список топ-10 цитат."""
    quotes = (
        Quote.objects.annotate(
            likes=Count('votes', filter=Q(votes__value=1))
        )
        .order_by('-likes', '-views')[:10]
        .select_related('source', 'added_by')  # для оптимизации
    )
    return render(request, 'backend/top_quotes.html', {'quotes': quotes})
