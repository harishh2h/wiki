from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/",views.random_page,name="random_page"),
   
    path("edit/<str:title>",views.edit,name="edit"),
    path("createpage",views.createpage,name="createpage"),
    path("<str:title>", views.get_page, name="get_page")
]
