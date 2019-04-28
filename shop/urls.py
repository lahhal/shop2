from django.urls import path, register_converter
from shop import views  # shop에 있는 views를 갖고 옴
# from . import views  # . : 같은 폴더
from shop import converters

app_name = 'shop'

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('excel/', views.response_excel, name='response_excel'),
    path('image/', views.response_image, name='response_image'),
    path('mysum/<int:x>/<int:y>/', views.my_sum, name='my_sum'),
    path('archives/<yyyy:year>/', views.year_archive, name='year_archive'),
    path('', views.item_list, name='item_list'), # 넘어온 게 아무것도 안 남아있으면 item_list를 보여주겠다는 의미
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('test_templates/', views.test_templates, name='test_templates'),
]
