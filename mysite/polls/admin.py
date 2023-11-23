from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)


# CRUD

class ChoiceInline(admin.TabularInline): #StackedInline
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('질문 섹션', {'fields': ['question_text']}),
        ('생성일', {'fields': ['pub_date'], 'classes': ['collapse']}), #숨김처리
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    readonly_fields = ['pub_date']
    inlines = [ChoiceInline]
    list_filter = ['pub_date'] #날짜는 리스트가 유리
    search_fields = ['question_text','choice__choice_text'] #텍스트는 검색이 유리

admin.site.register(Question, QuestionAdmin)