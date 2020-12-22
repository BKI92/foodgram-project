import datetime as dt
import io

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from recipes.forms import RecipeForm
from recipes.handlers import tags_handler, generate_tag_links, get_ingredients, \
    generate_pdf
from recipes.models import Recipe, Follow, Tag, Favorite, ShopList, User, \
    History
from foodgram.settings import VISIBLE_RECIPES


def index(request):
    search = request.GET.getlist('search')
    tags = Tag.objects.all()
    tags_list = tags_handler(search)
    tags_links = generate_tag_links(tags_list)
    tags_id_list = [tag.id for tag in tags.filter(slug__in=tags_list)]
    recipes = Recipe.objects.filter(tags__in=tags_id_list).distinct().order_by(
        '-pub_date')

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        template_name='index.html',
        context={'tags': tags,
                 'tags_list': tags_list,
                 'tags_links': tags_links,
                 'page': page,
                 'paginator': paginator
                 },
    )


@login_required
def my_follow(request, username):
    follows = Follow.objects.filter(user=request.user)
    follow_recipes = [[follow.author,
                       Recipe.objects.filter(author=follow.author).order_by(
                           '-pub_date')] for follow in follows]
    paginator = Paginator(follow_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='MyFollow.html',
        context={'follow_recipes': follow_recipes,
                 'visible': VISIBLE_RECIPES,
                 'page': page,
                 'paginator': paginator
                 },
    )


def new_recipe(request):
    tags = Tag.objects.all()
    form = RecipeForm()
    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            form.save()
            return redirect('index.html')
    return render(
        request,
        template_name='FormRecipe.html',
        context={
            'form': form,
            'tags': tags
        }
    )


@login_required
def favorite(request):
    search = request.GET.getlist('search')

    fav_recipes_ids = [fav.id for fav in
                       Favorite.objects.filter(user=request.user)]
    favorite_recipes = Recipe.objects.filter(id__in=fav_recipes_ids)

    tags = Tag.objects.all()
    tags_list = tags_handler(search)
    tags_links = generate_tag_links(tags_list)
    tags_id_list = [tag.id for tag in tags.filter(slug__in=tags_list)]

    result_recipes = favorite_recipes.filter(
        tags__in=tags_id_list).distinct().order_by('-pub_date')

    paginator = Paginator(result_recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='favorite.html',
        context={'tags': tags,
                 'tags_list': tags_list,
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
    my_shop_list = ShopList.objects.filter(user=user.id).first()
    current_recipe = get_object_or_404(Recipe, id=recipe_id)
    my_shop_list.recipes.remove(current_recipe)
    return redirect('shop_list')


@login_required
def send_pdf(request):
    my_shop_list = get_object_or_404(ShopList, user=request.user)
    recipes = my_shop_list.recipes.all()
    ingredients = get_ingredients(recipes)
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


@login_required
def author_recipes(request, author):
    search = request.GET.getlist('search')
    tags = Tag.objects.all()
    tags_list = tags_handler(search)
    tags_links = generate_tag_links(tags_list)
    tags_id_list = [tag.id for tag in tags.filter(slug__in=tags_list)]
    author_id = get_object_or_404(User, username=author)
    recipes = Recipe.objects.filter(author=author_id).filter(
        tags__in=tags_id_list).distinct().order_by(
        '-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        template_name='index.html',
        context={'tags': tags,
                 'tags_list': tags_list,
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
