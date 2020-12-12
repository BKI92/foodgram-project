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
