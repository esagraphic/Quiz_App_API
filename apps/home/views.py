# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import ListView , CreateView , DetailView
from .models import Subject, Category, Quiz, Question, Answer, CustomUser   
from .forms import SubjectForm , QuestionForm , CategoryForm, QuizForm
from .serializers import SubjectSerializer, CategorySerializer, QuizSerializer,QuestionSerializer, QuestionCreateSerializer,CustomUserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class SubjectListView(ListView):
    model = Subject
    template_name = 'home/subject_list.html'
    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_question_data = []

        for subject in Subject.objects.all():
            question_count = Question.objects.filter(quiz__category__subject=subject).count()
            subject_question_data.append((subject, question_count))

        context['subject_question_data'] = subject_question_data
        return context


class CategoryDetailView(DetailView):
    model = Subject
    template_name = 'home/category_detail.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(subject=self.object)
        category_question_data = []

        for category in categories:
            question_count = Question.objects.filter(quiz__category=category).count()
            category_question_data.append((category, question_count))

        context['category_question_data'] = category_question_data
        return context
    


class QuizDetailView(DetailView):
    model = Category
    template_name = 'home/quiz_detail.html'  # The template you will create
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quizzes = Quiz.objects.filter(category=self.object)  # Get quizzes related to the selected category
        quiz_question_count = []

        for quiz in quizzes:
            question_count = quiz.questions.count()  # Get the number of questions for each quiz
            quiz_question_count.append((quiz, question_count))

        context['quiz_question_count'] = quiz_question_count
        return context


class QuizQuestionsView(View):
    def get(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        questions = quiz.questions.all()
        
        questions_data = []
        for question in questions:
            answers = question.answers.all()  # This is correct; it gives a queryset of answers
            question_data = {
                'id': question.id,
                'question_text': question.text,
                'answers': answers,  # Pass the queryset directly
                'explanation': question.explanation,  # Include explanation
                'example_code': question.example_code,  # Include example code
            }
            questions_data.append(question_data)
        
        return render(request, 'home/quiz_questions.html', {
            'quiz': quiz,
            'questions_data': questions_data  # Pass questions_data to the template
        })

    def post(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        questions = quiz.questions.all()

        total_points = 0
        results = []

        for question in questions:
            selected_answers = request.POST.getlist(f'question_{question.id}')
            correct_answers = question.answers.filter(is_correct=True)
            correct_answers_text = ', '.join([answer.text for answer in correct_answers])  # Collect correct answer texts

            if set(map(int, selected_answers)) == set(correct_answers.values_list('id', flat=True)):
                total_points += 5
                results.append((question, 'Correct', None))  # No need to show correct answer if it's correct
            else:
                results.append((question, 'Incorrect', correct_answers_text))  # Pass correct answer text for incorrect results

        total_questions = len(questions)
        total_possible_score = total_questions * 5
        score_percentage = (total_points / total_possible_score) * 100

        return render(request, 'home/quiz_questions.html', {
            'quiz': quiz,
            'questions_data': questions,
            'results': results,
            'score': total_points,
            'score_percentage': round(score_percentage, 2),
            'total_possible_score': total_possible_score,
        })




def create_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')  # Redirect to the subject list or another page
    else:
        form = SubjectForm()

    return render(request, 'home/create_subject.html', {'form': form})




def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            # Save the question first
            question = question_form.save()

            # Get correct answers selected by the user
            correct_answers = question_form.cleaned_data['correct_answers']
            for i in range(1, 5):
                answer_text = question_form.cleaned_data.get(f'answer{i}')
                is_correct = str(i) in correct_answers  # Mark as correct if the answer index is selected
                answer = Answer(question=question, text=answer_text, is_correct=is_correct)
                answer.save()

            return redirect('subject-list')  # Redirect to the question list page or success page
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'home/add_question.html', {'question_form': question_form})

    else:
        question_form = QuestionForm()

    return render(request, 'home/add_question.html', {'question_form': question_form})




def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_quiz')  # Redirect to a category listing page or success page
    else:
        form = CategoryForm()
    return render(request, 'home/create_category.html', {'form': form})

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_question')  # Redirect to a quiz listing page or success page
    else:
        form = QuizForm()
    return render(request, 'home/create_quiz.html', {'form': form})



#api
class SubjectsAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    
class SubjectsDetailAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    

class CatrgoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class QuizAPIView(ListAPIView):
    queryset= Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionAPIView(ListAPIView):
    
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        quiz_pk = self.kwargs['quiz_pk']
        return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('answers')
    
class CreateSubjectAPIView(CreateAPIView):
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer
    
class CreateCategoryAPIView(CreateAPIView):
    queryset= Category.objects.all()
    serializer_class = CategorySerializer
    
class CreateQuizAPIView(CreateAPIView):
    queryset=Quiz.objects.all()
    serializer_class = QuizSerializer
    
class CreateQuestionAPIView(CreateAPIView):
    queryset= Question.objects.all()
    serializer_class = QuestionCreateSerializer

class UpdateSubjectsAPIView(UpdateAPIView):
    queryset= Subject.objects.all()
    serializer_class = SubjectSerializer

class UpdateCategoryAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UpdateQuizAPIView(UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class UpdateQuestionAPIView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer

class DeleteSubjectAPIView(DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class DeleteCategoryAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DeleteQuizAPIView(DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class DeleteQuestionAPIView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer


#ModelViewSet

class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    
    def get_serializer_class(self):
        """Use different serializer for list/retrieve and create/update"""
        if self.action in ['list', 'retrieve']:
            return QuestionSerializer  # Read-only with answers
        return QuestionCreateSerializer  # Writable with nested answers

    def get_queryset(self):
        """Filter by quiz ID if provided"""
        quiz_pk = self.request.query_params.get('quiz_pk')
        if quiz_pk:
            return Question.objects.filter(quiz_id=quiz_pk).prefetch_related('answers')
        return super().get_queryset()
    
    
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Ensure only active users can get a token
        if not user.is_active:
            return Response({"error": "User account is disabled."}, status=403)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    