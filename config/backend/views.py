"""Вью приложения."""

from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from backend.forms import QuoteForm
from backend.models import Quote
from backend.constants import NUM_QUOTES_PER_PAGE


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes_list")  # или куда нужно после добавления
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def quotes_list(request):
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
        "quotes/quotes_list.html",
        {
            "quotes": page_obj.object_list,
            "page_obj": page_obj,
            "source_query": source_query,
        },
    )
