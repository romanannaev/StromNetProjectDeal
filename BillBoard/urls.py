from django.urls import path
from .views import *

app_name = 'BillBoard'
urlpatterns = [
    path('', render_base_template, name='main'),
    path('<str:page>/', other_page, name='other'),
]