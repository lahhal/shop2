from django.shortcuts import render, get_object_or_404
from blog.models import Post, Tag
# from .models import Post # 같은 폴더에 있는 models를 가져오라는 의미

def post_list(request) :  # 함수 기반 뷰
    qs = Post.objects.all()
    return render(  # 뷰가 하는 가장 중요한 일
        request,                     # 요청 정보(요청한 사람의 ip 주소, 브라우저의 종류 등등)
        'blog/post_list.html',   # 템플릿 이름
        {'post_list' : qs}      # 템플릿에 전달할 정보를 사전 형태로
    )

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    all_tag = Tag.objects.all()
    mystr = post.tagged()
    my_tag = {}
    for t in all_tag:
        # mystr에서 t.name을 발견한 위치를 my_tag 사전에 등록
        # 키는 t.name으로, 값은 (못 찾으면 -1, 찾으면 양수)
        my_tag[t.name] = str(mystr).find(t.name)
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'my_tag': my_tag})
