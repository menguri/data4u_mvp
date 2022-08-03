from django.contrib import admin
from .models import Question_4, Answer
# Register your models here.

# 질문 검색 기능
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question_4, QuestionAdmin)
admin.site.register(Answer)