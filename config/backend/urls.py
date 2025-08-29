from django.urls import path

from backend.views import add_quote, quotes_list

urlpatterns = [
    path("", quotes_list, name="quotes_list"),
    path("add/", add_quote, name="add_quote"),
]
