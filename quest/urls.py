from django.urls import path
from . import views

aap_name = 'quest'

urlpatterns = [

    path('', views.index, name='index'),

    path('output/', views.get, name='get'),
    # path('', views.IndexView.as_view(), name='index'),
]