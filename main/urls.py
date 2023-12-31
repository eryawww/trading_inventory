from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('add_data_flutter', views.add_data_flutter, name='add_data_flutter'),
    path('get_my_data', views.get_my_data, name='add_data_flutter'),
    path('register_flutter', views.register_flutter, name='register_flutter'),

    path('', views.main, name='main'),
    path('xml/', views.show_xml, name='xml'),
    path('xml/<int:id>', views.show_xmlbyid, name='xmlbyid'),
    path('json/', views.show_json, name='json'),
    path('json/<int:id>', views.show_jsonbyid, name='jsonbyid'),
    path('create/', views.create, name='create'),
    path('register/', views.signup, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('add_amount/<int:id>', views.add_amount, name='add_amount'),
    path('minus_amount/<int:id>', views.minus_amount, name='minus_amount'),
    path('delete/<int:id>', views.delete, name='minus_amount'),

    path('get/<str:pk>', views.get_data, name='get_js'),
    path('subs/<str:inc>', views.edit_data, name='edit_js'),
    path('remove/<int:pk>', views.remove_data, name='remove_js'),
    path('create-ajax/', views.add_product_ajax, name='add_product')
]