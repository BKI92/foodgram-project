from django.contrib import admin

from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Follow, \
    Favorite


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
