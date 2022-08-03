from django import forms
from data4u.models import Question_4, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question_4
        fields = ['subject', 'content1', 'content2', 'content3', 'content4']
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content1': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        #     'content2': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        #     'content3': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        #     'content4': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        # }
        labels = {
            'subject': '제목',
            'content1': '첫 번째 선택지',
            'content2': '두 번째 선택지',
            'content3': '세 번째 선택지',
            'content4': '네 번째 선택지',
        }  

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels ={
            'content' : '답변 내용',
        }