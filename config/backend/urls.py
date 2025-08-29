from django.urls import path

from backend.views import (add_quote,
                           quotes_list,
                           source_detail,
                           add_source,
                           source_success,
                           source_list,
                           quote_success,
)

urlpatterns = [
    path("", quotes_list, name="quotes_list"),
    path("add/", add_quote, name="add_quote"),
    path('source/<str:source>/', source_detail, name='source_detail'),
    path('add-source/', add_source, name='add_source'),
    path('source-success/', source_success, name='source_success'),
    path('sources/', source_list, name='source_list'),
    path('quote-success/', quote_success, name='quote_success'),
]
