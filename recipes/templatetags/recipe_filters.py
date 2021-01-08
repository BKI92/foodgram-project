from django import template
from django.shortcuts import get_object_or_404

from recipes.models import ShopList, Follow, Favorite

register = template.Library()


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def link_generator(some_list):
    link = '&'.join([f'search={value}' for value in some_list])
    return link


@register.filter
def count_hidden_recipes(visible_recipes, all_recipes):
    if visible_recipes >= all_recipes:
        return 0
    return all_recipes - visible_recipes


@register.filter
def get_ending(visible_recipes, all_recipes):
    first_ending = ['0', '5', '6', '7', '8', '9']
    exceptions = ('11', '12', '13', '14')
    value = str(all_recipes - visible_recipes)
    if value[-1] in first_ending or value.endswith(exceptions):
        return 'ов'
    elif value.endswith('1'):
        return ''
    else:
        return 'а'


@register.filter
def count_recipes(request):
    my_shop_list = ShopList.objects.get_or_create(user=request.user)[0]
    recipes_amount = my_shop_list.recipes.count()
    return recipes_amount


@register.filter
def in_shop_list(request, recipe_id):
    is_belong = ShopList.objects.filter(user=request.user,
                                        recipes=recipe_id).exists()
    return is_belong


@register.filter
def is_subscription(request, author_id):
    status = Follow.objects.filter(user=request.user,
                                   author_id=author_id).exists()
    return status


@register.filter
def is_favorite(request, recipe_id):
    status = Favorite.objects.filter(user=request.user,
                                     recipes=recipe_id).exists()
    return status
