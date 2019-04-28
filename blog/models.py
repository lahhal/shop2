from django.db import models
from pytz import timezone  # 현지 시각 출력을 위하여
from django.conf import settings
from django.urls import reverse


def local_time(input_time):
    fmt = '%Y-%m-%d %H:%M'
    my_zone = timezone(settings.TIME_ZONE)
    my_local_time = input_time.astimezone(my_zone)
    return my_local_time.strftime(fmt)


class Post(models.Model):  # Post 클래스와 Comment 클래스는 일대다  # Post라고 지었지만 admin 화면에선 Posts로 나옴
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 'django.contrib.auth.models.User'보다 강추
        on_delete=models.CASCADE,
        # related_name='post_set',  # 기본 설정과 동일하므로 주석 처리
        related_name='posts',
        verbose_name='게시자',
    )
    # verbose_name: 관리자 화면 등에서 열 제목으로 사용될 속성
    # 관계 필드에서 첫 인자는 관계 대상 모델, verbose_name 키워드 인자로 처리
    # 관계 필드가 아닌 일반 필드의 (생략 가능한) 첫 인자는 verbose_name
    title = models.CharField('제목', max_length=100)
    content = models.TextField('내용')
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 등록(추가)된 시간을 자동으로 지정해 줌
    updated_at = models.DateTimeField(auto_now=True)  # 현재 시각을 자동으로 넣어 줌  // 여기까지 하고 makemigrations 후 migrate
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags')  # tag_set 아니고, tags

    class Meta:
        ordering = ['-id']  # Post 객체의 기본 정렬 순서 지정(최근 것 먼저)

    def __str__(self): # __str__() 함수를 만들면 객체를 만들 때 기본적으로 뭘 보여줄지를 지정 가능 # str 지정 안하면 object 1 이런식으로 나옴
        return self.title

    def short_content(self):
        if self.content:
            t = self.content[:20] + '...'   # content 속성의 일부만 반환
        else:
            t = '(내용 없음)'
        return t
    short_content.short_description = '간략 내용'

    def tagged(self):
        ts = self.tags.all()
        return '{' + ', '.join(map(str, ts)) + '}'  # 아래 주석과 같음
        # return ', '.join(ts)  # 이건 에러(왜 에러인지 모르겠음)
        # if ts:
        #     tag_string = '{'
        #     for t in ts:  # M2M 속성은 관리자이지, 쿼리셋이 아님
        #         tag_string += t.name + ', '  # t가 아니라 t.name
        #     tag_string = tag_string[:len(tag_string)-2] + '}'
        #     # tag_string 후미 ', '를 '}'으로 치환
        # else:
        #     tag_string = '{ }'
        # return tag_string
    tagged.short_description = '태그 집합'
    # 클래스 메소드로 속성을 대신할 때, verbose_name 대신에 short_description

    def updated(self):
        return local_time(self.updated_at)
    updated.short_description = '수정 일시'

    def get_absolute_url(self):
        # return reverse('blog:post_detail', args=[self.pk])
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

class Comment(models.Model):  # Comment라고 지었지만 admin 화면에선 Comments로 나옴
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='게시물')  # 장고 2.x 버전부터 on_delete는 꼭 밝혀야 함
    message = models.TextField('댓글')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-post__id', '-id']  # '-post__id', '-id'

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
