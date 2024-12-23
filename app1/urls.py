from django.urls import path
from .views import *
app_name='app1'
urlpatterns=[
    path('register/',register,name='register'),
    path('loginpage/',loginpage,name='loginpage'),
    path('',homepage,name='homepage'),
    path('logout/',logout,name='logout'),
    path('lobby/',lobby,name='lobby'),
    path('deposite/',deposite,name='deposite'),
    path('withdraw/',withdraw,name='withdraw'),
    path('sendmoney/',sendmoney,name='sendmoney'),
    path('transcation/',transcation,name='transcation'),
    path('registersuccess/',registersuccess,name='registersuccess'),
    path('loginsuccess/',loginsuccess,name='loginsuccess'),
    path('depositesuccess/',depositesuccess,name='depositesuccess'),
    path('withdrawsuccess/',withdrawsuccess,name='withdrawsuccess'),
    path('sendmoneysuccess/',sendmoneysuccess,name='sendmoneysuccess'),
]