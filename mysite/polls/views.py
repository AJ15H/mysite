from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F

from .models import *
from django.http import Http404

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# 4개의 메소드 구현
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ','.join([q.question_text for q in latest_question_list])
    context = {'questions': latest_question_list}
    return render(request, 'polls/index.html', context)
    # return HttpResponse(output)
    # return HttpResponse("Hello, world.")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #500에러 처리

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # return HttpResponse(f"입력받은 id: {question_id}")
    return render(request, 'polls/detail.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #500에러 처리
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist): #아무것도 선택하지 않았을때 keyerror
        return render(request, 'polls/detail.html', {'question': question, 'error_message': f"선택이 없습니다. id={request.POST['choice']}"})
    else:
        # A 서버에서도 Votes = 1
        # B 서버에서도 Votes = 1
        # 서버에서 하는 게 아니라 DB에서 실행하면 됨, 서버는 여러개지만 디비는 하나이기 때문
        selected_choice.votes = F('votes') + 1 # F는 디비에서 votes의 값을 읽어서 거기서 1을 증가
        selected_choice.save()
        return HttpResponseRedirect(reverse('questions:result', args = (question_id,)))
    
def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user-list')
    template_name = 'registration/signup.html'