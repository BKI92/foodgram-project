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
    recipes = Recipe.objects.filter(author__in=follows.all().values_list(
        'author_id')).order_by('-pub_date')
    return render(
        request,
        template_name='MyFollow.html',
        context={'username': username,
                 'follows': follows,
                 'recipes': recipes}
    )
