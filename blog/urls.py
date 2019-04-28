from django.urls import path
from blog import views  # blog에 있는 views를 갖고 옴
# from . import views  # . : 같은 폴더

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'), # 넘어온 게 아무것도 안 남아있으면 item_list를 보여주겠다는 의미
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
