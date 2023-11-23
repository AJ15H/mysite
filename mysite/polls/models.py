from django.db import models
from django.contrib import admin
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# Create your models here.
# 1. 모델 생성
# 2. 모델을 테이블에 써 주기 위한 마이그레이션이라는 걸 만들다.
# 3. 모델에 맞는 테이블 생성
# 질문: 여름에 놀러간다면 어디로 갈래?
# 산
# 강
# 바다
# 도심 호캉스

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일') #auto_now_add=True
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True) #User를 참조하는 외래키 생성

    # is_something = models.BooleanField(default=False)
    # average_score = models.FloatField(default=0.0)
    # score = models.FloatField(default=0)
    # is_something = models.BooleanField(default=False)
    # json_field = models.JSONField(default=dict)

    @admin.display(boolean=True, description='최근생성(하루기준)') 
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) #어제보다 더 최근에 만들어졌다면

    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE) #참조키를 만들었기 때문에 인덱싱
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.question.question_text}]  {self.choice_text}'

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions')
        ]