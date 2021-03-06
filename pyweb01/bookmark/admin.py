from django.contrib import admin
from bookmark.models import Bookmark

# Register your models here.
# 관리자 사이트에서 Bookmark클래스 출력 모양 정의하는 코드
class BookmarkAdmin(admin.ModelAdmin):
    #관리자 화면에 출력할 필드 목록(튜플 형식)
    list_display=("title","url")
    
# Bookmark클래스와 BookmarkAdmin클래스를 등록
admin.site.register(Bookmark,BookmarkAdmin)