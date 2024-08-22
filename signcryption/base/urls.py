from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register', user_register, name='user_register'),
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name='user_logout'),
    path('tfa', tfa, name='tfa'),
    path('new', make_transaction, name='new_transaction'),
    path('list', list_transactions, name='list_transaction')
]
