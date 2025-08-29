"""Вью приложения."""

from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from backend.forms import QuoteForm, SourceForm
from backend.models import Quote, Source
from backend.constants import NUM_QUOTES_PER_PAGE


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
    source_query = request.GET.get("source", "")
    page_number = request.GET.get("page", 1)

    if source_query:
        quotes = Quote.objects.filter(source__icontains=source_query).order_by("-id")
    else:
        quotes = Quote.objects.all().order_by("-id")
    paginator = Paginator(quotes, NUM_QUOTES_PER_PAGE)  # 10 цитат на страницу

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "backend/quotes_list.html",
        {
            "quotes": page_obj.object_list,
            "page_obj": page_obj,
            "source_query": source_query,
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
    return render(request, 'add_source.html', {'form': form})


def source_success(request):
    return render(request, 'source_success.html')


def source_list(request):
    """Список источников."""
    sources = Source.objects.all()
    return render(request, 'source_list.html', {'sources': sources})


def quote_success(request):
    return render(request, 'quote_success.html')
