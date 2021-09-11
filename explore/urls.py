from django.urls import path

from . import views

urlpatterns = [
    path('', views.explore, name='explore'),
    path('update_prof', views.update_prof, name='update_prof'),
    path('<str:user_name>', views.profile, name='profile'),
]