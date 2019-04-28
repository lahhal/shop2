from django.db import models
from pytz import timezone  # 현지 시각 출력을 위하여
from django.conf import settings
from django.urls import reverse

def local_time(input_time):
    fmt = '%Y-%m-%d %H:%M'
    my_zone = timezone(settings.TIME_ZONE)
    my_local_time = input_time.astimezone(my_zone)
    return my_local_time.strftime(fmt)

class Item(models.Model) :
    name = models.CharField(max_length=20)
    desc = models.TextField(blank=True)
    photo = models.ImageField()  # blank=True 지정하지 않은 경우
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 등록(추가)된 시간을 자동으로 지정해 줌
    updated_at = models.DateTimeField(auto_now=True)  # 현재 시각을 자동으로 넣어 줌  // 여기까지 하고 makemigrations 후 migrate
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags')  # tag_set 아니고, tags

    class Meta:
        ordering = ['-id']  # Item 객체의 기본 정렬 순서 지정(최근 것 먼저)

    def __str__(self): # __str__() 함수를 만들면 객체를 만들 때 기본적으로 뭘 보여줄지를 지정 가능 # str 지정 안하면 object 1 이런식으로 나옴
        return self.name

    def short_desc(self):
        if self.desc:
            t = self.desc[:20] + '...'   # desc 속성의 일부만 반환
        else:
            t = '(내용 없음)'
        return t
    short_desc.short_description = '간략 내용'

    def tagged(self):
        ts = self.tags.all()
        return '{' + ', '.join(map(str, ts)) + '}'
    tagged.short_description = '태그 집합'
    # 클래스 메소드로 속성을 대신할 때, verbose_name 대신에 short_description

    def updated(self):
        return local_time(self.updated_at)
    updated.short_description = '수정 일시'

    def get_absolute_url(self):
        return reverse('shop:item_detail', kwargs={'pk': self.pk})


# 리뷰라는 클래스 만들고 Item과 일대다로 만들어 보기
class Review(models.Model):  # Review라고 지었지만 admin 화면에선 Reviews로 나옴
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='reviews', verbose_name='상품')  # 장고 2.x 버전부터 on_delete는 꼭 밝혀야 함
    message = models.TextField('리뷰')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-item__id', '-id']  # '-post__id', '-id'

    def __str__(self):  # __str__() 함수를 만들면 객체를 만들 때 기본적으로 뭘 보여줄지를 지정 가능
        return self.message

    def updated(self):
        return local_time(self.updated_at)
    updated.short_description = '수정 일시'


class Tag(models.Model):
    name = models.CharField('태그', max_length=100, unique=True)

    class Meta:
        ordering = ['-id']  # Tag 객체의 기본 정렬 순서 지정

    def __str__(self):
        return self.name
