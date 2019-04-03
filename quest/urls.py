from django.urls import path
from . import views

aap_name = 'quest'

urlpatterns = [

    path('home/chapter/input/', views.index, name='index'),

    #/quest/output/
    path('home/chapter/input/output/', views.get, name='get'),

    path('home/',views.home, name='home'),

    path('home/chapter/',views.fli,name='fli'),

    #/quest/output/final
    path('home/chapter/input/output/final/', views.final, name='final'),
]