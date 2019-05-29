from django.shortcuts import render, render_to_response
from bookmark.models import Bookmark

# Create your views here.
def home(request):
    # select * from bookmark_bookmark order by title
    # Bookmark의 오브젝트를 title로 정렬(오름차순)
    urlList = Bookmark.objects.order_by("title")
    # select count(*) from bookmark_bookmark
    # Bookmark의 모든 오브젝트의 개수 가져와서 urlCount에 저장
    urlCount = Bookmark.objects.all().count()
    
    # list.html 페이지로 넘어가서 출력
    # rander_to response("url",{"변수명","변수명"}) 딕셔너리형태로 보내줌
    # 파이썬에서 두문장을 연결하기위해 '\' 입력
    return render_to_response("list.html", \
                              {"urlList":urlList, "urlCount":urlCount})

def detail(request):
    # get 방식 변수 받아오기 requeset.GET["변수명"]
    # post 방식 변수 받아오기 request.POST["변수명"]
    addr = request.GET["url"]
    # select * from bookmark_bookmark where url=".."
    dto = Bookmark.objects.get(url=addr)
    
    # detail.html로 포워딩
    return render_to_response("detail.html", {"dto":dto})
