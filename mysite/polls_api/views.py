from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins,generics, permissions
from polls.models import Question, Choice, Vote
from polls_api.serializers import QuestionSerializer, UserSerializer, RegisterSerializer, VoteSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter
from rest_framework import status

# class based view

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)
    
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, serializer):
    #     serializer.save(voter=self.request.user)
        
class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsVoter]

class QuestionList(generics.ListCreateAPIView): 
    # APIView 
    # mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    # mixins
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
        
    # class based
    #  def get(self, request):
    #     questions = Question.objects.all()
    #     serializer = QuestionSerializer(questions, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = QuestionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    # APIView
    # mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    
    # mixins
    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
        
    
    
    # class based
    # def get(self, request, id):
    #     question = get_object_or_404(Question, pk=id)
    #     serializer = QuestionSerializer(question)
    #     return Response(serializer.data)
    
    # def put(self, request, id):
    #     question = get_object_or_404(Question, pk=id)
    #     serializer = QuestionSerializer(question, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:    
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # def delete(self, request, id):
    #     question = get_object_or_404(Question, pk=id)
    #     question.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
        

# 데코레이터 구현
# @api_view(['GET', 'POST']) # 아무것도 안들어가면 GET
# def question_list(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True) # 여러개로 줄때
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET', 'PUT', 'DELETE'])
# def question_detail(request, id):
#     question = get_object_or_404(Question, pk=id)
    
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:    
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer