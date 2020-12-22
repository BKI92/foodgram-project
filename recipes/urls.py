from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:username>/follows/", views.my_follow, name="my_follow"),
    path("new/", views.new_recipe, name="new"),
    path("favorite/", views.favorite, name="favorite"),
    path("shop_list/", views.shop_list, name="shop_list"),
    path("shop_list/delete/<int:recipe_id>/", views.shop_list_delete,
         name="shop_list_delete"),
    path("shop_list/get_pdf/", views.send_pdf, name="shop_list_send_pdf"),
    path("author/<str:author>/", views.author_recipes, name="author_recipes"),
    path("recipes/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path("history/", views.history_view, name="history_view"),
    path("history/<int:history_id>/", views.recover_shop_list,
         name="recover_shop_list"),
    path("history/delete/<int:history_id>/", views.delete_history,
         name="delete_history"),
]
