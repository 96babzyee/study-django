from django.db import models

# Create your models here.
# 설문 문항 클래스
class Survey(models.Model):
    # 설문 인덱스
    survey_idx = models.AutoField(primary_key=True)
    # 문제, NOT NULL설정
    question = models.TextField(null=False)
    # 답 1-4
    ans1 = models.TextField(null=True)
    ans2 = models.TextField(null=True)
    ans3 = models.TextField(null=True)
    ans4 = models.TextField(null=True)
    # 설문진행상태(y=진행중, n=종료)
    status = models.CharField(max_length=1, default='y')

# 설문 응답 클래스
class Answer(models.Model):
    # 응답 아이디(자동증가 필드)
    answer_idx = models.AutoField(primary_key=True)
    # 설문 아이디(servey_idx 필드 참조 Foreign key)
    survey_idx = models.IntegerField()
    # 응답 번호
    num = models.IntegerField()
