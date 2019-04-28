from django.shortcuts import render, get_object_or_404
from shop.models import Item, Tag
# from .models import Item # 같은 폴더에 있는 models를 가져오라는 의미
from django.http import HttpResponse
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pandas as pd                           # 엑셀 요청 처리
from urllib.parse import quote

def response_excel(request):
    df = pd.DataFrame([
        [100, 110, 120],
        [200, 210, 220],
    ])

    io = BytesIO()
    df.to_excel(io)
    io.seek(0)

    encoded_filename = quote('pandas.xlsx')     # '.xls'가 아니라 '.xlsx'
    response = HttpResponse(io, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = \
        "attachment; filename*=utf-8''{}".format(encoded_filename)
    return response

def response_image(request):
    ttf_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우, 맥: '/Library/Fonts/AppleGothic.ttf'

    # 이미지 파일 다운로드 혹은 로컬 디스크 상의 이미지 직접 열기
    image_url = 'http://www.flowermeaning.com/flower-pics/Calla-Lily-Meaning.jpg'
    res = requests.get(image_url)  # 서버로 HTTP GET 요청하여, 응답 획득
    io = BytesIO(res.content)  # 응답의 Raw Body 메모리 파일 객체 BytesIO 인스턴스 생성
    io.seek(0)  # 파일의 처음으로 커서를 이동

    canvas = Image.open(io).convert('RGBA')  # 이미지 파일을 열고, RGBA 모드로 변환
    font = ImageFont.truetype(ttf_path, 40)  # 지정 경로의 TrueType 폰트, 폰트 크기40
    draw = ImageDraw.Draw(canvas)  # canvas에 대한 ImageDraw 객체 획득

    text = 'Smart IT, by logistex'
    left, top = 300, 400
    margin = 10
    width, height = font.getsize(text)
    right = left + width + margin
    bottom = top + height + margin
    draw.rectangle((left, top, right, bottom), (255, 255, 224))
    draw.text((left+5, top+5), text, font=font, fill=(20, 20, 20))

    response = HttpResponse(content_type='image/png')
    canvas.save(response, format='PNG')  # HttpResponse의 유사 파일 객체 특성 활용
    return response

def year_archive(request, year):
    if year is not None:
        return HttpResponse('{}년도 자료입니다.'.format(year))
    else:
        return HttpResponse('해당 연도 자료는 없습니다.')

def my_sum(request, x, y):
    result = x + y
    output = '{} = {} + {}'.format(result, x, y)
    return HttpResponse(output)

def item_list(request):  # 함수 기반 뷰
    items = Item.objects.all()
    # return render(  # 뷰가 하는 가장 중요한 일 # render를 부르면 최종적으론 HttpResponse가 작동
    #     request,                     # 요청 정보(요청한 사람의 ip 주소, 브라우저의 종류 등등)
    #     'shop/item_list.html',   # 템플릿 이름
    #     {'item_list' : items}      # 템플릿에 전달할 정보를 사전 형태로
    # )
    # request.GET 객체에게 키 값이 'q'로 지정된 값을 요구해서 변수 q에 저장
    q = request.GET.get('q', '')  # 키 값이 'q'로 지정된 값이 없으면 None이 반환됨
    if q: # q가 널 아니면 qs에 filter 조건 추가
        items = items.filter(name__icontains=q)
    return render(request, 'shop/item_list.html', {
        'item_list': items,
        'q': q,
    })

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    all_tag = Tag.objects.all()
    mystr = item.tagged()
    my_tag = {}
    for t in all_tag:
        # mystr에서 t.name을 발견한 위치를 my_tag 사전에 등록
        # 키는 t.name으로, 값은 (못 찾으면 -1, 찾으면 양수)
        my_tag[t.name] = str(mystr).find(t.name)
    return render(request, 'shop/item_detail.html',
                  {'item': item, 'my_tag': my_tag})

class MyClass:
    x = 10
    y = 20

def test_templates(requset):
    from django.template import Context, Template
    import datetime       # USE_TZ = True
    from django.utils import timezone   # TIME_ZONE = 'Asia/Seoul'
    from dateutil.parser import parse

    # 맥락 변수 사전
    my_dict = {'first_name': 'haewoong', 'last_name': 'Shin'}
    my_obj = MyClass()
    my_list = [1, 2, 3, 4]
    my_date = datetime.datetime.now()
    local_time = timezone.localtime()
    my_b_date1 = datetime.date(2019, 12, 29)
    my_b_date2 = parse('2010-12-29')
    my_b_datetime = datetime.datetime(2010, 12, 29, 17, 34, 56)
    my_string = '사랑하지 않으려면 떠나라. Love it or leave it.'

    context = Context({'my_dict': my_dict, 'my_obj': my_obj, 'my_list': my_list,
                       'my_date': my_date, 'local_time': local_time,
                       'my_b_date1': my_b_date1, 'my_b_date2': my_b_date2,
                       'my_b_datetime': my_b_datetime, 'my_string': my_string,
                       })
    template = Template(
        "사전 < my_dict.last_name >: {{ my_dict.last_name }} <br/>"
        + "객체 < my_obj.x >: {{ my_obj.x }} {{ my_obj.y }} <br/>"
        + "리스트 < my_list.0 >: {{ my_list.0 }} {{ my_list.2 }}: {{ my_list.2 }} <br/>"
        + "< my_dict.first_name|title >: {{ my_dict.first_name|title }} <br/>"
        + "{% verbatim myblock %}{% now 'Y-m-d H:i:s' %}"
        + "{% endverbatim myblock %} : {% now 'Y-m-d H:i:s' %} <br/>"
        + "< my_date > : {{ my_date }} <br/>"
        + "< local_time >: {{ local_time }} <br/>"
        + "< my_b_date1 >: {{ my_b_date1 }} <br/>"
        + "< my_b_date2 >: {{ my_b_date2 }} <br/>"
        + "< my_b_date1|date:'SHORT_DATE_FORMAT' >: {{ my_b_date1|date:'SHORT_DATE_FORMAT' }} <br/>"
        + "(마지막에 점이 찍힘!! 필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
        + "< my_b_date1|date:'Y년 m월 d일' >: {{ my_b_date1|date:'Y년 m월 d일' }} <br/>"
        # + "< my_b_date|date:'LONG_DATE_FORMAT' >(???)': {{ my_b_date|date:'LONG_DATE_FORMAT' }} <br/>"
        # + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>" # 오류!!
        + "< my_b_datetime >: {{ my_b_datetime }} <br/>"
        + "< my_b_datetime|date:'Y년 m월 d일' > < my_b_datetime|time:'H시 i분 s초' >: "
        + "{{ my_b_datetime|date:'Y년 m월 d일' }}  {{ my_b_datetime|time:'H시 i분 s초' }} <br/>"
        + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
        + "< my_string|lower|truncatewords:'4' >: {{ my_string|lower|truncatewords:'4' }} <br/>"
        # 수업 규칙 : 숫자 앞뒤에 불필요한 따옴표는 안하기로 정함!
        + "< my_string|lower|truncatewords:4 >: {{ my_string|lower|truncatewords:4 }} <br/>"
        + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
        + "< my_string|lower|truncatechars:'12' >: {{ my_string|lower|truncatechars:'12' }} <br/>"
        +"(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
    )
    content = template.render(context)

    return HttpResponse(content)
