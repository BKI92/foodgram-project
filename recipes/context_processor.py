from recipes.models import Tag


def get_tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return context