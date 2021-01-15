from django.contrib import admin

from recipes.models import (Favorite, Follow, History, Ingredient,
                            IngredientAmount, Recipe, ShopList, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'pub_date', 'duration',)
    search_fields = ('title', 'description')
    list_filter = ('pub_date',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'style', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension',)
    search_fields = ('title',)
    list_filter = ('title', 'dimension')


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user')
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(ShopList)
class ShopListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user',)
    search_fields = ('user',)
    list_filter = ('user',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'pub_date')
    search_fields = ('user',)
    list_filter = ('user', 'pub_date')
