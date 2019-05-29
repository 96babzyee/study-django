from django.shortcuts import render, render_to_response
# csrf(Cross Site Request Forgery)
from django.views.decorators.csrf import csrf_exempt  # 크로스 사이트 요청 위조
from survey.models import Survey, Answer  # 설문테이블, 응답테이블 import


# Create your views here.
# localhost(시작페이지)
def survey_list(request):
    # filter => where
    # order_by("필드") 오름차순, order_by("-필드") 내림차순
    # select * from servey_servey where status='y'
    surveyList = Survey.objects.filter(status='y').order_by("-survey_idx")
    
    return render_to_response("survey_List.html", {'surveyList':surveyList})


def survey_item(request):
    idx=request.GET["survey_idx"]
    survey=Survey.objects.get(survey_idx=idx)
    
    return render_to_response("survey_item.html", {'survey':survey})
    
    
@csrf_exempt
def save_survey(request):
    # survey_idx : 설문문항 코드
    # num : 사용자가 선택한 번호
    dto = Answer(survey_idx=request.POST["survey_idx"], num=request.POST["num"])
    dto.save()  # insert query 실행
    
    # success.html로 이동
    return render_to_response("success.html")


def show_result(request):
    idx = request.GET["survey_idx"]
    ans = Survey.objects.get(survey_idx=idx)
    answer = [ans.ans1, ans.ans2, ans.ans3, ans.ans4]
    surveyList = Survey.objects.raw("""
        select
            survey_idx, num, count(num) sum_num,
            round((select count(*) from survey_answer
                where survey_idx=a.survey_idx and num=a.num)*100.0 /
                (select count(*) from survey_answer
                    where survey_idx=a.survey_idx),1) rate
        from survey_answer a
        where survey_idx=%s
    group by survey_idx,num
    order by num
    """, idx)
    surveyList = zip(surveyList, answer)
    print("surveyList:", surveyList)
    print("answer:", answer)
    # select count(*) from survey_answer
    count=Answer.objects.all().count()
    
    return render_to_response('result.html', {'surveyList':surveyList, "count" : count})
