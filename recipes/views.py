import datetime as dt
import io
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import VISIBLE_RECIPES
from recipes.forms import RecipeForm
from recipes.handlers import (generate_pdf, generate_tag_links,
                              get_form_ingredients, get_recipe_ingredients,
                              tags_handler)
from recipes.models import (Favorite, Follow, History, Ingredient,
                            IngredientAmount, Recipe, ShopList, Tag, User)


def index(request):
    search = request.GET.getlist('search')
    tags = Tag.objects.all()
    passed_tags = tags_handler(search)
    tags_links = generate_tag_links(passed_tags)
    tags_id = tags.filter(slug__in=passed_tags).values_list('id', flat=True)
    recipes = Recipe.objects.filter(tags__in=tags_id).distinct()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        template_name='index.html',
        context={
            'passed_tags': passed_tags,
            'tags_links': tags_links,
            'page': page,
            'paginator': paginator
        },
    )


@login_required
def my_follow(request, username):
    follows = Follow.objects.filter(user=request.user)
    paginator = Paginator(follows, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='MyFollow.html',
        context={
            'visible': VISIBLE_RECIPES,
            'page': page,
            'paginator': paginator
        },
    )


def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_form_ingredients(request)
    if form.is_valid() and ingredients:
        recipe = form.save(commit=False)
        recipe.author = request.user
        form.save()
        passed_tags = request.POST.getlist('tags')
        for tag_id in passed_tags:
            tag = get_object_or_404(Tag, id=tag_id)
            recipe.tags.add(tag)

        for title, amount in ingredients.items():
            ingredient = Ingredient.objects.get_or_create(
                title=title, dimension='шт')[0]
            new_ingredient = IngredientAmount.objects.get_or_create(
                ingredient=ingredient,
                amount=amount)[0]
            recipe.ingredients.add(new_ingredient)
        form.save_m2m()
        return redirect('index')
    if request.method == 'POST' and not ingredients:
        form.add_error(None, 'Обязательное поле.')
    return render(
        request,
        template_name='FormRecipe.html',
        context={
            'form': form,
        }
    )


@login_required
def change_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    author = recipe.author
    if user != author:
        return redirect('recipe_view', recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    ingredients = get_form_ingredients(request)
    if form.is_valid():
        form.save()
        recipe.ingredients.clear()
        for title, amount in ingredients.items():
            ingredient = Ingredient.objects.get_or_create(
                title=title, dimension='шт.')[0]
            new_ingredient = IngredientAmount.objects.get_or_create(
                ingredient=ingredient,
                amount=amount)[0]
            recipe.ingredients.add(new_ingredient)

        return redirect('recipe_view', recipe_id=recipe_id)

    if request.method == 'POST' and not ingredients:
        form.add_error(None, 'Обязательное поле.')
    recipe_tags = recipe.tags.all()
    ingredients = recipe.ingredients.all()
    return render(request, 'formChangeRecipe.html', {
        'form': form,
        'recipe': recipe,
        'ingredients': ingredients,
        'recipe_tags': recipe_tags
    })


@login_required
def delete_recipe(request, recipe_id):
    Recipe.objects.filter(author=request.user, id=recipe_id).delete()
    return redirect('index')


@login_required
def favorite(request):
    search = request.GET.getlist('search')

    fav_recipes_ids = Favorite.objects.values_list('id', flat=True)
    favorite_recipes = Recipe.objects.filter(id__in=fav_recipes_ids)

    tags = Tag.objects.all()
    passed_tags = tags_handler(search)
    tags_links = generate_tag_links(passed_tags)
    tags_id = tags.filter(slug__in=passed_tags).values_list('id', flat=True)

    result_recipes = favorite_recipes.filter(
        tags__in=tags_id).distinct().order_by('-pub_date')

    paginator = Paginator(result_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='favorite.html',
        context={
            'passed_tags': passed_tags,
            'tags_links': tags_links,
            'page': page,
            'paginator': paginator
        },
    )


@login_required
def shop_list(request):
    user = request.user
    my_shop_list = ShopList.objects.filter(user=user.id).first()
    if my_shop_list:
        recipes = my_shop_list.recipes.all()
    else:
        recipes = None
    return render(
        request,
        template_name='shopList.html', context={'recipes': recipes})


@login_required
def shop_list_delete(request, recipe_id):
    user = request.user
    my_shop_list = ShopList.objects.get_or_create(user=user.id)[0]
    current_recipe = get_object_or_404(Recipe, id=recipe_id)
    my_shop_list.recipes.remove(current_recipe)
    return redirect('shop_list')


@login_required
def send_pdf(request):
    my_shop_list = get_object_or_404(ShopList, user=request.user)
    recipes = my_shop_list.recipes.all()
    ingredients = get_recipe_ingredients(recipes)
    buffer = io.BytesIO()
    generate_pdf(ingredients, buffer)
    buffer.seek(0)
    date_str = dt.datetime.now().strftime('%d-%m-%Y_%H-%M')
    if recipes:
        my_history = History.objects.create(user=request.user)
        for recipe in recipes:
            my_history.recipes.add(recipe)
        my_shop_list.recipes.clear()
    return FileResponse(buffer, as_attachment=True,
                        filename=f'shoplist_{date_str}')


def author_recipes(request, author):
    search = request.GET.getlist('search')
    tags = Tag.objects.all()
    passed_tags = tags_handler(search)
    tags_links = generate_tag_links(passed_tags)
    tags_id = tags.filter(slug__in=passed_tags).values_list('id', flat=True)
    author = get_object_or_404(User, username=author)
    recipes = Recipe.objects.filter(author=author).filter(
        tags__in=tags_id).distinct().order_by(
        '-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        template_name='authorRecipe.html',
        context={
            'author': author,
            'passed_tags': passed_tags,
            'tags_links': tags_links,
            'page': page,
            'paginator': paginator
        },
    )


@login_required
def recipe_view(request, recipe_id):
    current_recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(
        request,
        template_name='singlePage.html',
        context={'recipe': current_recipe,
                 },
    )


@login_required
def history_view(request):
    my_history = History.objects.filter(user=request.user.id).order_by(
        '-pub_date')
    paginator = Paginator(my_history, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='History.html',
        context={'page': page,
                 'paginator': paginator
                 },
    )


@login_required
def recover_shop_list(request, history_id):
    my_history = get_object_or_404(History, pk=history_id)
    my_shop_list = get_object_or_404(ShopList, user=request.user)
    for recipe in my_history.recipes.all():
        my_shop_list.recipes.add(recipe)
    return redirect(
        'shop_list'
    )


@login_required
def delete_history(request, history_id):
    my_history = get_object_or_404(History, pk=history_id)
    my_history.delete()
    return redirect(
        'history_view'
    )


@login_required
def add_purchases(request):
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        my_shop_list = ShopList.objects.get_or_create(user=request.user)[0]
        my_shop_list.recipes.add(recipe)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def delete_purchases(request, recipe_id):
    if request.method == "DELETE":
        my_shop_list = get_object_or_404(ShopList, user=request.user)
        my_shop_list.recipes.remove(recipe_id)
        return JsonResponse(
            {'success': True}) if my_shop_list else JsonResponse(
            {'success': False})
    return JsonResponse({'success': True})


@login_required
def create_subscriptions(request):
    if request.method == "POST":
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        if request.user != author:
            Follow.objects.get_or_create(user=request.user, author=author)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def delete_subscriptions(request, author_id):
    if request.method == "DELETE":
        follow = get_object_or_404(Follow, user=request.user, author=author_id)
        if follow:
            follow.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def get_ingredients(request):
    text = request.GET.get('query').rstrip('/')
    data = []
    ingredients = Ingredient.objects.filter(
        title__startswith=text).all()
    for ingredient in ingredients:
        data.append(
            {'title': ingredient.title, 'dimension': ingredient.dimension})

    return JsonResponse(data, safe=False)


@login_required
def add_favorites(request):
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        my_favorite = Favorite.objects.get_or_create(user=request.user)[0]
        my_favorite.recipes.add(recipe)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def delete_favorites(request, recipe_id):
    if request.method == "DELETE":
        my_favorite = get_object_or_404(Favorite, user=request.user)
        if my_favorite:
            my_favorite.recipes.remove(recipe_id)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
