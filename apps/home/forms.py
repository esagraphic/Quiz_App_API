from django import forms
from .models import Subject , Category , Quiz , Question , Answer

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['subject', 'name']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['category', 'name', 'is_private']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'text', 'explanation', 'example_code']

    # Create 4 separate answer fields in the form
    answer1 = forms.CharField(max_length=255, label="Answer 1", required=True)
    answer2 = forms.CharField(max_length=255, label="Answer 2", required=True)
    answer3 = forms.CharField(max_length=255, label="Answer 3", required=True)
    answer4 = forms.CharField(max_length=255, label="Answer 4", required=True)

    correct_answers = forms.MultipleChoiceField(
        choices=[('1', 'Answer 1'), ('2', 'Answer 2'), ('3', 'Answer 3'), ('4', 'Answer 4')],
        widget=forms.CheckboxSelectMultiple,
        label="Select Correct Answers",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quiz'].queryset = Quiz.objects.all()