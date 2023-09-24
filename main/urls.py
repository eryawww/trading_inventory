from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main, name='main'),
    path('xml/', views.show_xml, name='xml'),
    path('xml/<int:id>', views.show_xmlbyid, name='xmlbyid'),
    path('json/', views.show_json, name='json'),
    path('json/<int:id>', views.show_jsonbyid, name='jsonbyid'),
    path('create/', views.create, name='create'),
    path('register', views.signup, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('add_amount/<int:id>', views.add_amount, name='add_amount'),
    path('minus_amount/<int:id>', views.minus_amount, name='minus_amount')
]