from django.urls import path
from django.contrib.auth import views as auth_views

from backend.views import (add_quote,
                           quotes_list,
                           source_detail,
                           add_source,
                           source_success,
                           source_list,
                           quote_success,
                           register,
                           random_weighted_quote,
                           vote_quote,
                           top_quotes,
)

urlpatterns = [
    path("", quotes_list, name="quotes_list"),
    path("add/", add_quote, name="add_quote"),
    path('source/<int:source_id>/', source_detail, name='source_detail'),
    path('add-source/', add_source, name='add_source'),
    path('source-success/', source_success, name='source_success'),
    path('sources/', source_list, name='source_list'),
    path('quote-success/', quote_success, name='quote_success'),
    path('register/', register, name='register'),
    path('login/',
         auth_views.LoginView.as_view(template_name='backend/login.html'),
         name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('random/', random_weighted_quote, name='random_weighted_quote'),
    path('vote_quote/', vote_quote, name='vote_quote'),
    path('top-quotes/', top_quotes, name='top_quotes'),
]
