from django.contrib import admin
from django.urls import path, include
from django.conf import settings                         # 추가 1
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')), # shop에 있는 urls로 떠넘기겠다는 의미(shop/ 까지는 끝내고 나머지 부분을 넘김!)
    path('weblog/', include('blog.urls')),  # blog에 있는 urls로 떠넘기겠다는 의미(blog/ 까지는 끝내고 나머지 부분을 넘김!)
    path('pizzas/', include('pizzas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # db에 있는 media 파일 사진의 깨짐을 없애기 위해

if settings.DEBUG:                                       # 추가 2
    import debug_toolbar                                 # 추가 2
    urlpatterns += [                                     # 추가 2
        path('__debug__/', include(debug_toolbar.urls)), # 추가 2
    ]                                                    # 추가 2
