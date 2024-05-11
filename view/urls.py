from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:parameter>/', views.index, name='index_with_parameter'),
    path('lab', views.lab),
    path('modify', views.modify),
    path('logout', views.signout),
    path('login', views.adminlogin),
    path('request', views.request),
    # path('print', views.print_children)
]
