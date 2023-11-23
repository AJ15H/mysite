from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

# Create your tests here.

# 시리얼라이저 테스트

# class QuestionSerializerTestCase(TestCase):
#     def test_with_valid_data(self):
#         serializer = QuestionSerializer(data={'question_text': 'abc'})
#         self.assertEqual(serializer.is_valid(), True)
#         new_question = serializer.save()
#         self.assertIsNotNone(new_question.id)
        
#     def test_with_invalid_data(self):
#         serializer = QuestionSerializer(data={'question_text': ''})
#         self.assertEqual(serializer.is_valid(), False)

class VoteSerializerTest(TestCase):
    # 각 테스트 실행 전 한번 반복하기 때문에 한번만 셋업에 써주면 됨, 
    # 각 테스트 후 초기화 되고 다시 다른 테스트가 실행되기 전 또 실행됨
    # 즉, 두번에 테스트에 사용된다고 두번의 유저가 생성되어 있지 않음
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text='1'
        )    
        
    def test_vote_serializer(self):
        self.assertEqual(User.objects.all().count(),1)
        data={
            'question':self.question.id,
            'choice':self.choice.id,
            'voter':self.user.id
        }
        serializer=VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote=serializer.save()
        
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)
        
    
        
    # def test_vote_serializer(self):
    #     self.assertEqual(User.objects.all().count(),1)
        

    def test_vote_serializer_with_duplicate_vote(self):
        # user = User.objects.create(username='testuser')
        # question = Question.objects.create(
        #     question_text='abc',
        #     owner=user,
        # )
        # choice = Choice.objects.create(
        #     question=question,
        #     choice_text='1'
        # )
        self.assertEqual(User.objects.all().count(),1)
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text='2'
        )
        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)
        data={
            'question':self.question.id,
            'choice':self.choice1.id,
            'voter':self.user.id
        }
        serializer=VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # vote=serializer.save()
        
        
        # self.assertEqual(User.objects.all().count, 1)
        # choice1=Choice.objects.create(
        #     question=self.question,
        #     choice_text='2'
        # )
        # Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)
        # data={
        #     'question':self.question.id,
        #     'choice':self.choice.id,
        #     'voter':self.user.id
        # }
        # serializer=VoteSerializer(data=data)
        # self.assertTrue(serializer.is_valid())

    def test_vote_serilaizer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text='abc',
            owner=self.user,
        )
    
        choice2 = Choice.objects.create(
            question=question2,
            choice_text='1'
        )
        data = {
            'question': self.question.id,
            'choice': choice2.id,
            'voter': self.user.id
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
        
# 뷰 테스트

class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data={'question_text':'some question'}
        self.url = reverse('question-list')

    def test_create_question(self):
        user = User.objects.create(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question=Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertLess((timezone.now()-question.pub_date).total_seconds(), 1)

    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_question(self):
        question=Question.objects.create(question_text='Question1')
        choice=Choice.objects.create(question=question, choice_text='choice1')
        Question.objects.create(question_text='Question2')
        response=self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        # print(f'$$$$$$$$${response.data}\n')
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)
        # [OrderedDict([('id', 1), ('question_text', 'Question1'), ('pub_date', '2023-11-05T10:23:03.376521Z'), ('choices', [OrderedDict([('choice_text', 'choice1'), ('votes_count', 0)])])]), OrderedDict([('id', 2), ('question_text', 'Question2'), ('pub_date', '2023-11-05T10:23:03.376678Z'), ('choices', [])])]