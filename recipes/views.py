from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from recipes.models import Recipe, Follow, User


def index(request):
    recipes = Recipe.objects.all().order_by('-pub_date')
    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  template_name='index.html',
                  context={'page': page,
                           'paginator': paginator},
                  )


@login_required
def my_follow(request, username):
    follows = Follow.objects.filter(user=request.user)
    follow_recipes = [[follow.author, Recipe.objects.filter(author=follow.author).order_by('-pub_date')] for follow in follows]
    paginator = Paginator(follow_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        template_name='MyFollow.html',
        context={'follow_recipes': follow_recipes, 'page': page, 'paginator': paginator},
    )
