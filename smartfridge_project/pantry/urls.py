from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_view, name='inventory'),
    path('api/add/', views.add_item_api, name='add_item_api'),
    path('api/delete/<int:item_id>/', views.delete_item_api, name='delete_item_api'),
    path('recipes/', views.recipe_matcher_view, name='recipes'),
]
