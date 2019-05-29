from django.db import models

# Create your models here.
# django의 Model 클래스 상속받음
# 테이블 생성
class Bookmark(models.Model):
    # 필드 선언, blank 빈값 허용, null허용
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField("url", unique=True)  # unique는 primary key
    
    # 객체를 문자열로 표현하는 함수
    def __str__(self):
        return self.title