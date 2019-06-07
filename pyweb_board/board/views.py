import os
import math
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from board.models import Board, Comment
from django.utils.http import urlquote
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

UPLOAD_DIR = 'c:/upload/'
# Create your views here.


@csrf_exempt
def list(request):
    try:
        search_option = request.POST["search_option"]
    except:
        search_option = "writer"
    
    try:
        search = request.POST["search"]
    except:
        search = ""
    
    print("search_option:", search_option)
    print("search:", search)
    
    # select count(*) from board_board'''
    # boardCount=Board.objects.count()
    if search_option == "all":  # 이름+제목+내용
        boardCount = Board.objects.filter(\
Q(writer__contains=search) | Q(title__contains=search) | \
Q(content__contains=search)).count()
    elif search_option == "writer":  # 이름
        boardCount = Board.objects.filter(\
writer__contains=search).count()                                          
    elif search_option == "title":  # 제목
        boardCount = Board.objects.filter(\
title__contains=search).count()           
    elif search_option == "content":  # 내용
        boardCount = Board.objects.filter(\
content__contains=search).count()          
    
    print("레코드 개수:", boardCount)
    
    '''limit start, 레코드 개수'''
    try:
        start = int(request.GET['start'])
    except:
        start = 0
    page_size = 5;  # 페이지당 게시물수
    page_list_size = 5;  # 한 화면에 표시할 페이지의 갯수
    end = start + page_size
    # 전체 페이지 갯수 , math.ceil() 올림함수
    total_page = math.ceil(boardCount / page_size)
    # start 레코드시작번호 => 페이지번호
    current_page = math.ceil((start + 1) / page_size)
    # 페이지 블록의 시작번호, math.floor() 버림함수
    start_page = math.floor(
(current_page - 1) / page_list_size) * page_list_size + 1;
    # 페이지 블록의 끝번호
    end_page = start_page + page_list_size - 1;
    # 마지막 페이지가 범위를 초과하지 않도록 처리
    if total_page < end_page:
        end_page = total_page
    # 1 ~ 10
    # [이전] 11 ~ 20
    if start_page >= page_list_size:
        prev_list = (start_page - 2) * page_size;
    else:
        prev_list = 0
    # 91 ~ 100 
    # 81 ~ 90 [다음]
    if total_page > end_page:
        next_list = end_page * page_size
    else:
        next_list = 0
    
    print("start_page:", start_page)
    print("end_page:", end_page)
    print("page_list_size:", page_list_size)
    print("total_page:", total_page)
    print("prev_list:", prev_list)
    print("next_list:", next_list)  
    
    '''select * from board_board order by idx desc'''
    # boardList=Board.objects.all().order_by('-idx')[start:end]
    
    if search_option == "all":
        boardList = Board.objects.filter(
            Q(writer__contains=search) | 
            Q(title__contains=search) | 
            Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(
            writer__contains=search).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(
            title__contains=search).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(
            content__contains=search).order_by("-idx")[start:end]
        
    print("board type", type(boardList))
    
    links = []
    for i in range(start_page, end_page + 1):
        page = (i - 1) * page_size
        links.append("<a href='?start=" + str(page) + "'>" + str(i) + "</a>")
        
    return render_to_response('list.html',
        {"boardCount":boardCount,
         "boardList":boardList,
         "search_option": search_option,
         "search": search,
         "range":range(start_page - 1, end_page),
         "start_page":start_page,
         "end_page":end_page,
         "page_list_size":page_list_size,
         "total_page":total_page,
         "prev_list":prev_list,
         "next_list":next_list,
         "links":links})
    

def write(request):
    return render_to_response("write.html")


@csrf_exempt
def insert(request):
    fname = ""
    fsize = 0
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file._name
        fsize = file.size
        
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
        # fsize=os.path.getsize(UPLOAD_DIR+fname)
    
    '''insert into board_board(writer,title,content,flename,filesize)
    values(....)'''
    dto = Board(writer=request.POST["writer"],
                 title=request.POST["title"],
                 content=request.POST["content"],
                 filename=fname,
                 filesize=fsize)
    '''insert 실행'''
    dto.save()
    print(dto)
    return redirect("/")


def download(request):
    id = request.GET['idx']
    # idx로 게시물 가져오기
    '''select * from board_board where idx=id'''
    dto = Board.objects.get(idx=id)  # 
    path = UPLOAD_DIR + dto.filename
    print("path:", path)
    # 디렉토리를 제외한 파일 이름 
    filename = os.path.basename(path)  # 수수 파일명 가져옴
    # file명 인코딩 방식
    # filename = filename.encode("utf-8")
    filename = urlquote(filename)  # url에 포함된 특수문자 처리
    print("pfilename:", os.path.basename(path))
    with open(path, 'rb') as file:  # 바이너리 타입 읽기모드로 파일 오픈
        # 서버의 파일을 읽음, 파일의 종류가 다양함으로 octet-stream으로 선택
        response = HttpResponse(file.read(), content_type="application/octet-stream") 
        # 첨부파일의 이름(한글이름이 깨지지 않도록 처리
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{0}".format(filename) 
        dto.down_up()  # 다운로드의 수를 1증가 함
        dto.save()  # update 쿼리 실행
        return response  # 첨부파일 client에게 전송함

    
def detail(request):
    id = request.GET["idx"]  # 게시물 번호
    '''select * from board_board where idx=id'''
    dto = Board.objects.get(idx=id)
    '''조회수 증가 처리'''
    dto.hit_up()
    dto.save()  # update query 호출
    # 첨부파일의 크기
    filesize = "{0:.2f}".format(dto.filesize / 1024)
    
    # 댓글 목록 select * from board_comment where board_idx=id    
    commentList = Comment.objects.filter(board_idx=id).order_by("-idx")
    
    # detail.html 페이지로 넘어가는 출력값
    return render_to_response("detail.html",
        {"dto":dto, "filesize":filesize, "commentList":commentList})


@csrf_exempt
def update(request):
    id = request.POST["idx"]  # 글번호
    # select * from board_board where idx=id
    dto_src = Board.objects.get(idx=id) 
    fname = dto_src.filename  # 기존 첨부파일 이름
    print("filename:", fname)
    fsize = dto_src.filesize  # 기존 첨부파일 크기
    if "file" in request.FILES:  # 새로운 첨부파일이 있으면
        file = request.FILES["file"]
        fname = file.name  # 새로운 첨부파일의 이름
        fsize = file.size
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)  # 파일 저장
        fp.close()
        # 첨부파일의 크기(업로드완료 후 계산
        # fsize=os.path.getsize(UPLOAD_DIR+fname)
    # 수정 후 board의 내용
    dto_new = Board(idx=id, writer=request.POST["writer"],
                    title=request.POST['title'],
                    content=request.POST["content"],
                    hit=dto_src.hit,
                    down=dto_src.down,
                    post_date=dto_src.post_date,
                    filename=fname,
                    filesize=fsize)
    dto_new.save()  # update query 호출
    return redirect("/")  # 시작 페이지로 이동  


@csrf_exempt
def delete(request):
    id = request.POST["idx"]  # 삭제할 게시물의 번호
    Board.objects.get(idx=id).delete()  # 레코드 삭제
    return redirect("/")  # 시작 페이지로 이동  


@csrf_exempt
def reply_insert(request):
    id = request.POST["idx"]  # 게시물 번호
    # 댓글 객체 생성
    dto = Comment(board_idx=id, writer=request.POST["writer"], content=request.POST["content"])
    # insert query 실행
    dto.save()
    # detail?idx=글번호 페이지로 이동
    return HttpResponseRedirect("detail?idx=" + id)
