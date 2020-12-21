from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import Tag


def tags_handler(search, tags_list=[]):
    default_slugs = [tag.slug for tag in Tag.objects.all()]
    if search:
        tags_list.clear()
        for tag_slug in search:
            if tag_slug in tags_list:
                tags_list.remove(tag_slug)
            else:
                tags_list.append(tag_slug)
        return tags_list
    if tags_list:
        return tags_list
    return default_slugs


def generate_tag_links(tags_list):
    default_slugs = [tag.slug for tag in Tag.objects.all()]
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


def get_ingredients(recipes):
    final_dict = {}
    for recipe in recipes:
        for ing in recipe.ingredients.all():
            if ing.ingredient.title in final_dict and ing.ingredient.dimension == \
                    final_dict[ing.ingredient.title][1]:
                final_dict[ing.ingredient.title][0] += ing.amount
            else:
                final_dict[ing.ingredient.title] = [ing.amount,
                                                    ing.ingredient.dimension]
    return final_dict


def generate_pdf(ings_dict, buffer):
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        TTFont('FreeSansOblique', 'static/FreeSansOblique.ttf'))
    p.setFont('FreeSansOblique', 20)
    header = "Список ингредиентов:"
    x, y = 30, 800
    p.drawString(x, y, header)
    p.setFont('FreeSansOblique', 15)
    x1, y1 = 50, 790
    for index, ing in enumerate(ings_dict):
        text = f"{index + 1}) {ing} - {ings_dict[ing][0]} {ings_dict[ing][1]}."
        y1 -= 25
        p.drawString(x1, y1, text)
    p.showPage()
    p.save()
