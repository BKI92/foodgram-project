from about import views
from django.urls import path

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='about_author'),
    path('tech/', views.AboutTechView.as_view(), name='about_tech')

]
