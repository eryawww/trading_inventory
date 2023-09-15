from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'),
    path('xml/', views.show_xml, name='xml'),
    path('xml/<int:id>', views.show_xmlbyid, name='xmlbyid'),
    path('json/', views.show_json, name='json'),
    path('json/<int:id>', views.show_jsonbyid, name='jsonbyid'),
    path('create/', views.create, name='create')
]