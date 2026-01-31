from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_route, name="add_route"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name="dashboard"),
    path("clear_tree/", views.clear_tree, name="clear_tree"),
]