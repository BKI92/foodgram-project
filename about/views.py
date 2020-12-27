from django.views.generic.base import TemplateView


class JustStaticPage(TemplateView):
    template_name = 'templates/just_page.html'
