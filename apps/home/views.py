# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
import os
import subprocess
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView , CreateView , DetailView , UpdateView , DeleteView
from .models import Subject, Category, Quiz, Question, Answer, CustomUser   
from .forms import SubjectForm , QuestionForm , CategoryForm, QuizForm
from .serializers import SubjectSerializer, CategorySerializer, QuizSerializer,QuestionSerializer, QuestionCreateSerializer,CustomUserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import AllowCreateUser   # Import custom permission
from django.utils import timezone
from django.template.loader import render_to_string
from .utils.generate_excelfile import generate_excel_file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename
from django.http import FileResponse


@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


class SubjectListView(ListView):
    model = Subject
    template_name = "home/subject_list.html"
    context_object_name = "subjects"

    def get_queryset(self):
        # Ensure the user is authenticated
        if self.request.user.is_authenticated:
            # Filter subjects where the logged-in user is part of the users field
            return Subject.objects.filter(users=self.request.user)
        else:
            # Return empty queryset for anonymous users
            return Subject.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_question_data = []

        # Loop through the filtered subjects only
        for subject in self.get_queryset():
            # Get the number of questions related to each subject
            question_count = Question.objects.filter(quiz__category__subject=subject).count()
            subject_question_data.append((subject, question_count))

        context['subject_question_data'] = subject_question_data
        context['form'] = SubjectForm()
        return context


# Remove user from subject , category and quiz
def remove_user_from_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    # Remove the user from the subject
    subject.users.remove(request.user)

    # Remove the user from all related categories
    categories = Category.objects.filter(subject=subject)
    for category in categories:
        category.users.remove(request.user)

        # Remove the user from all related quizzes
        quizzes = Quiz.objects.filter(category=category)
        for quiz in quizzes:
            quiz.users.remove(request.user)

    return redirect('subject-list')  # Redirect to the subject list page or another appropriate page


def confirm_remove_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'home/partials/remove_subject_modal.html', {'subject': subject})


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'home/category_detail.html'
    context_object_name = 'subject'

    def get_queryset(self):
        # Ensure the user is authenticated
        if self.request.user.is_authenticated:
            # Filter subjects where the logged-in user is part of the users field
            return Subject.objects.filter(users=self.request.user)
        else:
            # Return empty queryset for anonymous users
            return Subject.objects.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(subject=self.object)
        category_question_data = []

        for category in categories:
            question_count = Question.objects.filter(quiz__category=category).count()
            category_question_data.append((category, question_count))

        context["category_question_data"] = category_question_data
        return context


class QuizDetailView(DetailView):
    model = Category
    template_name = "home/quiz_detail.html"  # The template you will create
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quizzes = Quiz.objects.filter(
            category=self.object
        )  # Get quizzes related to the selected category
        quiz_question_count = []

        for quiz in quizzes:
            question_count = (
                quiz.questions.count()
            )  # Get the number of questions for each quiz
            quiz_question_count.append((quiz, question_count))

        context["quiz_question_count"] = quiz_question_count
        return context


class QuizQuestionsView(View):
    
    def get(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        questions = quiz.questions.all()

        questions_data = []
        for question in questions:
            answers = (
                question.answers.all()
            )  # This is correct; it gives a queryset of answers
            question_data = {
                "id": question.id,
                "question_text": question.text,
                "answers": answers,  # Pass the queryset directly
                "explanation": question.explanation,  # Include explanation
                "example_code": question.example_code,  # Include example code
            }
            questions_data.append(question_data)
        
        return render(request, 'home/quiz_questions.html', {
            'quiz': quiz,
            'questions_data': questions_data,  # Pass questions_data to the template
         # Pass questions_data to the template
        })

    def post(self, request, quiz_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        questions = quiz.questions.all()

        total_points = 0
        results = []

        for question in questions:
            selected_answers = request.POST.getlist(f"question_{question.id}")
            correct_answers = question.answers.filter(is_correct=True)
            correct_answers_text = ", ".join(
                [answer.text for answer in correct_answers]
            )  # Collect correct answer texts

            if set(map(int, selected_answers)) == set(
                correct_answers.values_list("id", flat=True)
            ):
                total_points += 5
                results.append(
                    (question, "Correct", None)
                )  # No need to show correct answer if it's correct
            else:
                results.append(
                    (question, "Incorrect", correct_answers_text)
                )  # Pass correct answer text for incorrect results

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
#Update Question
class UpdateQuestionView(View):
    def get(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk)  

        form = QuestionForm(instance=question)

        return render(request, 'home/update_question.html', {
            'form': form,
            'question': question
        })  
    
    def post(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk)

        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz_questions', quiz_pk=question.quiz.pk)
        
        return render(request, 'home/update_question.html', {
            'form': form,
            'question': question
        })



def create_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['name']
            print(f"Subject name from form: '{subject_name}'")

            try:
                # Try to get the existing subject (case-insensitive match)
                subject = Subject.objects.get(name__iexact=subject_name)
                created = False  # It already exists
            except Subject.DoesNotExist:
                # If subject doesn't exist, create a new one
                subject = Subject(name=subject_name)
                subject.save()
                created = True  # Subject was created

            # Add the current logged-in user to the subject's users field
            subject.users.add(request.user)

            # Debugging output
            print(f"Created: {created}")
            print(f"Subject: {subject.name if subject else 'No subject found'}")
            print(f"User {request.user.email} added to subject '{subject.name}'")

            context = {
                'subject': subject,
                'question_count': Question.objects.filter(quiz__category__subject=subject).count(),
                'user': request.user,
                
            }
            
            response = render(request, 'home/partials/subject-rows.html', context)
            response['HX-Trigger'] = 'success'  # Trigger HTMX event
            return response

    else:
        form = SubjectForm()

    return render(request, "home/create_subject.html", {"form": form})





def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, user=request.user)  # Pass logged-in user
        
        if question_form.is_valid():
            # Save the question first
            question = question_form.save()

            # Get correct answers selected by the user
            correct_answers = question_form.cleaned_data["correct_answers"]
            for i in range(1, 5):
                answer_text = question_form.cleaned_data.get(f"answer{i}")
                is_correct = (
                    str(i) in correct_answers
                )  # Mark as correct if the answer index is selected
                answer = Answer(
                    question=question, text=answer_text, is_correct=is_correct
                )
                answer.save()

            # Check the action and redirect accordingly
            action = request.POST.get('action')
            if action == 'save_finish':
                return redirect('subject-list')  # Redirect to the subject list page
            elif action == 'save_new':
                return redirect('add_question')  # Reload the add question page for a new entry

        else:
            # If the form is invalid, re-render the form with error messages
            return render(
                request, "home/add_question.html", {"question_form": question_form}
            )

    else:
        question_form = QuestionForm(user=request.user)

    return render(request, "home/add_question.html", {"question_form": question_form})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)  # Pass logged-in user
        if form.is_valid():
            category_name = form.cleaned_data['name']
            print(f"Category name from form: '{category_name}'")

            try:
                # Try to get the existing category (case-insensitive match)
                category = Category.objects.get(name__iexact=category_name)
                created = False  # It already exists
            except Category.DoesNotExist:
                # If category doesn't exist, create a new one
                category = form.save(commit=False)
                category.subject = form.cleaned_data['subject']
                category.name = category_name
                category.save()
                created = True  # Category was created
            # Add the current logged-in user to the category's users field
            category.users.add(request.user)
            # Debugging output
            print(f"Created: {created}")    

            print(f"Category: {category.name if category else 'No category found'}")
            print(f"User {request.user.email} added to category '{category.name}'")
            # Save the category instance
            # Redirect to a success page or another view
            response = render(request, 'home/partials/category-rows.html', {'category': category})
            response['HX-Trigger'] = 'success'  # Trigger HTMX event
            return response
            
    else:
        form = CategoryForm(user=request.user) # Pass user when rendering the form

        
    categories = Category.objects.filter(users=request.user)  # Get categories for the logged-in user
    
    return render(request, 'home/create_category.html', {'form': form, 'categories': categories})

# Create a new quiz
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, user=request.user)  #  Pass 'user' to the form
        if form.is_valid():
            quiz = form.save()  #  Save the quiz instance
            quiz.users.add(request.user)  #  Link the quiz to the user
            # return redirect('add_question')  # Redirect after saving
            response = render(request, 'home/partials/quiz-rows.html', {'quiz': quiz})
            response['HX-Trigger'] = 'success'  # Trigger HTMX event
            return response

    else:
        form = QuizForm(user=request.user)  #  Pass 'user' when rendering

        
    quizs = Quiz.objects.filter(users=request.user)  # Get quizzes for the logged-in user
    print(f"user id is {request.user.id}")
    
    return render(request, 'home/create_quiz.html', {'form': form, 'quizs': quizs})



# api
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
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionAPIView(ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_pk = self.kwargs["quiz_pk"]
        return Question.objects.filter(quiz_id=quiz_pk).prefetch_related("answers")


class CreateSubjectAPIView(CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CreateCategoryAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CreateQuizAPIView(CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class CreateQuestionAPIView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer


class UpdateSubjectsAPIView(UpdateAPIView):
    queryset = Subject.objects.all()
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


# ModelViewSet


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
        if self.action in ["list", "retrieve"]:
            return QuestionSerializer  # Read-only with answers
        return QuestionCreateSerializer  # Writable with nested answers

    def get_queryset(self):
        """Filter by quiz ID if provided"""
        quiz_pk = self.request.query_params.get("quiz_pk")
        if quiz_pk:
            return Question.objects.filter(quiz_id=quiz_pk).prefetch_related("answers")
        return super().get_queryset()


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowCreateUser]  # Apply the custom permission


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Ensure only active users can get a token
        if not user.is_active:
            return Response({"error": "User account is disabled."}, status=403)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

  
class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'home/partials/update-subject-modal.html'

    def form_valid(self, form):
        # Save the subject
        subject = form.save()

        # Render the updated subject row for HTMX
        context = {
            'subject': subject,
            'question_count': Question.objects.filter(quiz__category__subject=subject).count()
        }
        html= render(self.request, 'home/partials/subject-rows.html', context)
        response = HttpResponse(html)
        response['HX-Trigger'] = 'subjectUpdated'  # Trigger HTMX event
        return response
    

       

    # def get_success_url(self):
        # You can redirect to a success page or return an empty response
        # return reverse_lazy('subject-list')
    
    
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'home/partials/category-update-modal.html'
    form_class = CategoryForm
    # success_url = reverse_lazy('create_category') 

    def form_valid(self, form):
       
        # Save the category
        category = form.save()

        # Render the updated category row for HTMX
        context = {
            'category': category,
        }
        response = render(self.request, 'home/partials/category-rows.html', context)
        response['HX-Trigger'] = 'categoryUpdated'
        return response

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Category.objects.filter(users=self.request.user)
        else:
            return Category.objects.none()
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form
        kwargs['user'] = self.request.user
        return kwargs
    
class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'home/partials/update-quiz-modal.html'
    form_class = QuizForm
    
    def form_valid(self, form):
        # Save the quiz
        quiz = form.save()

        # Render the updated quiz row for HTMX
        context = {
            'quiz': quiz,
        }
        response = render(self.request, 'home/partials/quiz-rows.html', context)
        response['HX-Trigger'] = 'quizUpdated'
        return response

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Quiz.objects.filter(users=self.request.user)
        else:
            return Quiz.objects.none()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form
        kwargs['user'] = self.request.user
        return kwargs
    
class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'home/delete-quiz.html'
    form_class = QuizForm
    success_url = reverse_lazy('create_quiz') 

def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = list(question.answers.all().order_by('id'))  # Make sure to preserve order

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question , user=request.user)  # Pass logged-in user
        if form.is_valid():
            form.save()

            correct_answers = form.cleaned_data['correct_answers'] 
            
            for i in range(4):
                answer = answers[i]
                answer.text = form.cleaned_data[f'answer{i+1}']
                answer.is_correct = str(i+1) in correct_answers
                answer.save()

            return redirect('quiz-questions', quiz_pk=question.quiz.pk)
    else:
        initial_data = {
            'answer1': answers[0].text if len(answers) > 0 else '',
            'answer2': answers[1].text if len(answers) > 1 else '',
            'answer3': answers[2].text if len(answers) > 2 else '',
            'answer4': answers[3].text if len(answers) > 3 else '',
            'correct_answers': [str(i+1) for i, a in enumerate(answers) if a.is_correct],
        }
        form = QuestionForm(instance=question, initial=initial_data , user=request.user)  # Pass logged-in user
    return render(request, 'home/update_question.html', {'question_form': form, 'question': question})


def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        question.delete()
        return redirect('quiz-questions', quiz_pk=question.quiz.id)
    
    return render(request, 'home/partials/confirm_delete_modal.html', {'question': question})
