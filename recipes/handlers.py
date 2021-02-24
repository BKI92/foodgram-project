from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import Tag


def tags_handler(search):
    saved_tags = []
    default_slugs = Tag.objects.values_list('slug', flat=True)
    if search:
        saved_tags.clear()
        for tag_slug in search:
            if tag_slug in saved_tags:
                saved_tags.remove(tag_slug)
            else:
                saved_tags.append(tag_slug)
        return saved_tags
    if saved_tags:
        return saved_tags
    return default_slugs


def generate_tag_links(tags_list):
    default_slugs = Tag.objects.values_list('slug', flat=True)
    links = {}
    for tag in default_slugs:
        if tag in tags_list:
            links[tag] = '&'.join(
                [f'search={new_tag}' for new_tag in tags_list if
                 new_tag != tag])
            if not links[tag]:
                links[tag] = f'search= '
        else:
            links[tag] = '&'.join(
                [f'search={new_tag}' for new_tag in default_slugs if
                 new_tag in tags_list or new_tag == tag])
    return links


def get_recipe_ingredients(recipes):
    final_dict = {}
    for recipe in recipes:
        for ing in recipe.ingredients.all():
            title = ing.ingredient.title
            dimension = ing.ingredient.dimension
            amount = ing.amount
            if title in final_dict and dimension == final_dict[title][1]:
                final_dict[title][0] += amount
            else:
                final_dict[title] = [amount, dimension]
    return final_dict


def generate_pdf(ingredients, buffer):
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('FreeSansOblique', 'static/FreeSansOblique.ttf'))
    p.setFont('FreeSansOblique', 20)
    header = "Список ингредиентов:"
    x, y = 30, 800
    p.drawString(x, y, header)
    p.setFont('FreeSansOblique', 15)
    x1, y1 = 50, 790
    for index, ing in enumerate(ingredients):
        text = f"{index + 1}) {ing} - {ingredients[ing][0]} " \
               f"{ingredients[ing][1]}."
        y1 -= 25
        p.drawString(x1, y1, text)
    p.showPage()
    p.save()


def get_form_ingredients(request):
    ingredients = {}
    for key, value in request.POST.items():
        if 'nameIngredient' in key:
            ing_id = key.split('_')[-1]
            name = value
            ingredients[ing_id] = [name]
        if 'valueIngredient' in key:
            ing_id = key.split('_')[-1]
            amount = value
            ingredients[ing_id].append(amount)
        if 'unitsIngredient' in key:
            ing_id = key.split('_')[-1]
            units = value
            ingredients[ing_id].append(units)
    return ingredients
