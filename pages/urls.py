from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),  
    path('clothing-catalogue/', views.clothing_catalogue, name='clothing_catalogue'),
    path('case_study/', views.case_study, name='case_study'),
    path('faq/', views.faq, name='faq'),
]
