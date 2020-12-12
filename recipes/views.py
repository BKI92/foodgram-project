from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from recipes.forms import RecipeForm
from recipes.handlers import tags_handler, generate_tag_links
from recipes.models import Recipe, Follow, User, Tag


def index(request):
    search = request.GET.getlist('search')

    tags = Tag.objects.all()
    tags_list = tags_handler(search)
    tags_links = generate_tag_links(tags_list)
    tags_id_list = [tag.id for tag in tags.filter(slug__in=tags_list)]
    recipes = Recipe.objects.filter(tags__in=tags_id_list).distinct().order_by('-pub_date')

    paginator = Paginator(recipes, 2)
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
    paginator = Paginator(follow_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='MyFollow.html',
        context={'follow_recipes': follow_recipes,
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
def favorites(request):
    tags = Tag.objects.all()
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    return render(
        request,
        template_name='favorite.html',
        context={
            'recipes': recipes,
            'tags': tags
        }
    )
