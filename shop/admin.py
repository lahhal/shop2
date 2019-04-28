from django.contrib import admin
from .models import Item, Review, Tag  # .models : 같은 폴더에 있는 models

# admin.site.register(Item)

@admin.register(Item)  # 아래 클래스가 Post 모델을 관리하는 클래스임
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_desc',   # short desc
                    'tagged',                                   # tagged
                    'updated',  # 'updated_at',
                    ]
    # 위에서 'tags'로 하면 'must not be a ManyToManyField'라고 오류
    list_display_links = ['id', 'name', ]
    list_filter = ['created_at', 'updated_at', 'tags', ]
    search_fields = ['name', 'desc', ]  # 자식 객체에서 부모 객체를 선택 가능하도록


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'message', 'updated', ]
    list_display_links = ['id', 'message', ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]
