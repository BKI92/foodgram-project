from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("author/<str:author>/", views.author_recipes, name="author_recipes"),

    path("follows/<str:username>/", views.my_follow, name="my_follows"),

    path("recipes/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path("recipe/delete/<int:recipe_id>/", views.delete_recipe,
         name="delete_recipe"),
    path("recipe/new/", views.new_recipe, name="new_recipe"),
    path("recipe/change/<int:recipe_id>/", views.change_recipe,
         name="change_recipe"),

    path("favorite/", views.favorite, name="favorite"),
    path("favorites", views.add_favorites, name="add_favorite"),
    path("favorites/<int:recipe_id>", views.delete_favorites,
         name="delete_favorite"),

    path("shop_list/", views.shop_list, name="shop_list"),
    path("shop_list/delete/<int:recipe_id>/", views.shop_list_delete,
         name="shop_list_delete"),
    path("shop_list/get_pdf/", views.send_pdf, name="shop_list_send_pdf"),

    path("history/", views.history_view, name="history_view"),
    path("history/<int:history_id>/", views.recover_shop_list,
         name="recover_shop_list"),
    path("history/delete/<int:history_id>/", views.delete_history,
         name="delete_history"),

    path("purchases", views.add_purchases, name="add_purchases"),
    path("purchases/<int:recipe_id>", views.delete_purchases,
         name="delete_purchases"),

    path("subscriptions", views.create_subscriptions,
         name="create_subscriptions"),
    path("subscriptions/<int:author_id>", views.delete_subscriptions,
         name="delete_subscriptions"),

    path("ingredients", views.get_recipe_ingredients, name="get_recipe_ingredients"),

]
