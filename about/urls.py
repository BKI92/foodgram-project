from about import views
from django.urls import path

urlpatterns = [
    path('author/', views.JustStaticPage.as_view(), name='about_author'),
    path('tech/', views.JustStaticPage.as_view(), name='about_tech')

]
