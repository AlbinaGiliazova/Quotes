"""Вью приложения."""

from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from backend.forms import QuoteForm, SourceForm
from backend.models import Quote, Source
from backend.constants import NUM_QUOTES_PER_PAGE, NUM_SOURCES_PER_PAGE


def add_quote(request):
    """Страница добавления цитаты"""
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quote_success")  
    else:
        form = QuoteForm()
    return render(request,
                  "backend/add_quote.html",
                  {"form": form})


def quotes_list(request):
    """Страница списка цитат."""
    page_number = request.GET.get("page", 1)

    quotes = Quote.objects.all().order_by("-id")
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


def source_detail(request, source):
    """Страница цитат одного источника."""
    quotes = Quote.objects.filter(source=source)
    if not quotes.exists():
        # Можно вернуть 404, если такого источника нет вообще
        return render(request, "backend/source_not_found.html", {"source": source})
    return render(request, "backend/source_detail.html", {"quotes": quotes, "source": source})


def add_source(request):
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('source_success')  # или нужный вам редирект
    else:
        form = SourceForm()
    return render(request, 'backend/add_source.html', {'form': form})


def source_success(request):
    return render(request, 'backend/source_success.html')


def source_list(request):
    sources = Source.objects.all().order_by('name')
    paginator = Paginator(sources, NUM_SOURCES_PER_PAGE)  # Показывать по 10 источников на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'backend/source_list.html', {'page_obj': page_obj})


def quote_success(request):
    return render(request, 'backend/quote_success.html')
