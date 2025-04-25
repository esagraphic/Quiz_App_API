from django import forms
from .models import Subject , Category , Quiz , Question , Answer ,   Group , GroupInvitation , GroupQuiz  , CustomUser

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['subject', 'name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract 'user' from kwargs
        super().__init__(*args, **kwargs)  # Initialize the form

        if user:
            self.fields['subject'].queryset = Subject.objects.filter(users=user)  # Filter subjects


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['category', 'name', 'is_private']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract 'user' from kwargs
        super().__init__(*args, **kwargs)  # Initialize the form

        if user:
            self.fields['category'].queryset = Category.objects.filter(users=user)  # ✅ Filter only user's categories


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
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent constructor
        
        # ✅ Correct filtering for ManyToManyField
        if user:
            self.fields['quiz'].queryset = Quiz.objects.filter(users__in=[user])
        else:
            self.fields['quiz'].queryset = Quiz.objects.none()  # Default to empty queryset

        # ✅ Add Tailwind CSS classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'mt-2'})
            else:
                field.widget.attrs.update({'class': 'w-full p-2 border rounded-md mt-1'})

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']


class GroupInvitationForm(forms.ModelForm):
    email = forms.EmailField(label='User Email')  # Instead of selecting user, we'll take email as input

    class Meta:
        model = GroupInvitation
        fields = ['email', 'is_accepted']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = CustomUser.objects.get(email=email)  # Fetch the user based on the email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No user found with this email address.")
        return user  # Return the user object to associate it with the invitation
    

class GroupQuizForm(forms.ModelForm):
    class Meta:
        model = GroupQuiz
        fields = ['group', 'quiz']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupQuizForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['group'].queryset = Group.objects.filter(created_by=user)
            self.fields['quiz'].queryset = Quiz.objects.filter(users=user)
        else:
            self.fields['group'].queryset = Group.objects.none()
            self.fields['quiz'].queryset = Quiz.objects.none()
