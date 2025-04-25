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
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView , CreateView , DetailView , UpdateView , DeleteView
from .models import Subject, Category, Quiz, Question, Answer, CustomUser, Group, GroupInvitation, GroupQuiz , UserQuizResult
from .forms import SubjectForm , QuestionForm , CategoryForm, QuizForm , GroupForm , GroupInvitationForm , GroupQuizForm
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
from apps.home.utils.ai_quiz import ai_generate_quiz 


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
         # Check if quiz is part of any group
        group_quiz = GroupQuiz.objects.filter(quiz=quiz).first()
        if group_quiz:
            user_result, created = UserQuizResult.objects.get_or_create(
                group_quiz=group_quiz,
                user=request.user
            )

            if not user_result.is_answered:
                user_result.score = total_points
                user_result.is_answered = True
                user_result.save()

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
        subject = self.get_object()
        current_user = self.request.user

        # Check if other users are using this subject
        other_users = subject.users.exclude(id=current_user.id)

        if other_users.exists():
            # Detach current user from the shared subject
            subject.users.remove(current_user)

            # Create a new subject with updated values
            new_subject = form.save(commit=False)
            new_subject.pk = None  # So it will create a new object
            new_subject.save()
            new_subject.users.add(current_user)
            subject = new_subject  # Use the new subject for rendering
        else:
            # Safe to update the subject since it's only used by this user
            subject = form.save()

        # Count related questions
        question_count = Question.objects.filter(quiz__category__subject=subject).count()

        context = {
            'subject': subject,
            'question_count': question_count
        }

        html = render(self.request, 'home/partials/subject-rows.html', context).content
        response = HttpResponse(html)
        response['HX-Trigger'] = 'subjectUpdated'
        return response

    

       

    # def get_success_url(self):
        # You can redirect to a success page or return an empty response
        # return reverse_lazy('subject-list')
    
    
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'home/partials/category-update-modal.html'
    form_class = CategoryForm

    def form_valid(self, form):
        category = self.get_object()
        current_user = self.request.user

        # Check if other users are using this category
        other_users = category.users.exclude(id=current_user.id)

        if other_users.exists():
            # Detach current user from the shared category
            category.users.remove(current_user)

            # Create a new category with the updated values
            new_category = form.save(commit=False)
            new_category.pk = None  # Forces creation of new object
            new_category.save()
            new_category.users.add(current_user)
            category = new_category  # For rendering
        else:
            # Safe to update directly
            category = form.save()

        # Render updated row
        context = {'category': category}
        response = render(self.request, 'home/partials/category-rows.html', context)
        response['HX-Trigger'] = 'categoryUpdated'
        return response

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Category.objects.filter(users=self.request.user)
        return Category.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    
class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = 'home/partials/update-quiz-modal.html'
    form_class = QuizForm

    def form_valid(self, form):
        quiz = self.get_object()
        current_user = self.request.user

        # Check if other users are using this quiz
        other_users = quiz.users.exclude(id=current_user.id)

        if other_users.exists():
            # Detach current user from the shared quiz
            quiz.users.remove(current_user)

            # Create a new quiz with the updated values
            new_quiz = form.save(commit=False)
            new_quiz.pk = None  # Force creation of a new object
            new_quiz.save()
            new_quiz.users.add(current_user)
            quiz = new_quiz  # Use new quiz for rendering
        else:
            # Safe to update directly
            quiz = form.save()

        context = {'quiz': quiz}
        response = render(self.request, 'home/partials/quiz-rows.html', context)
        response['HX-Trigger'] = 'quizUpdated'
        return response

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Quiz.objects.filter(users=self.request.user)
        return Quiz.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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


def generate_quiz(request):
    context = {}
    question_form = QuestionForm(request.POST, user=request.user)

    if request.method == "POST":
        if "save_db" in request.POST:
            selected_quiz_id = request.POST.get("quiz")
            my_data = request.session.get("parsed_output")

            if not selected_quiz_id or not my_data:
                return HttpResponse("❌ Quiz ID or parsed data is missing.")

            quiz = get_object_or_404(Quiz, id=selected_quiz_id)

            for data in my_data:
                explanation_text = f"{data['explanation']}\n\nWhy Not Others?\n"
                for key, reason in data["why_not"].items():
                    explanation_text += f"- {key}: {reason or 'Not provided'}\n"

                question = Question.objects.create(
                    quiz=quiz,
                    text=data["question"],
                    explanation=explanation_text,
                    example_code=data.get("example")
                )

                correct_key = data["correct_answer"].lower()
                for key, answer_text in data["options"].items():
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=(key.lower() == correct_key)
                    )

            
            return redirect("quiz-questions", quiz_pk=selected_quiz_id)

        elif "upload_excel" in request.POST:
            try:
                uploaded_file = request.FILES["quiz_file"]
                if not uploaded_file.name.endswith(".xlsx"):
                    return HttpResponse("❌ Only .xlsx files are allowed.")

                sanitized_filename = get_valid_filename(uploaded_file.name)
                sanitized_filename = os.path.basename(sanitized_filename)
                relative_path = os.path.join("user_uploads", sanitized_filename)
                default_storage.save(relative_path, ContentFile(uploaded_file.read()))

                context["upload_success"] = True
                context["uploaded_path"] = os.path.join(settings.MEDIA_URL, relative_path)

                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                script_path = os.path.join(settings.BASE_DIR, "apps", "home", "utils", "read_from_excelfile.py")

                result = subprocess.run(["python", script_path, file_path], capture_output=True, text=True)
                if result.returncode != 0:
                    return HttpResponse(f"❌ Error running script: {result.stderr}")

                try:
                    parsed_output = json.loads(result.stdout)
                except json.JSONDecodeError as e:
                    return HttpResponse(f"❌ Failed to parse script output as JSON: {str(e)}")

                context["script_output"] = parsed_output
                request.session["parsed_output"] = parsed_output
                print(f"Parsed Output: {parsed_output}")

            except Exception as e:
                return HttpResponse(f"❌ Upload Error: {e}")

        elif "generate_excel" in request.POST:
            try:
                num_questions = int(request.POST["num_questions"])
                user_id = request.user.id
                filename = generate_excel_file(user_id, num_questions)
                file_path = os.path.join(settings.MEDIA_ROOT, "exports", filename)
                context["filename"] = filename
            except Exception as e:
                return HttpResponse(f"❌ Error: {e}")

    context["question_form"] = question_form
    return render(request, "home/generate_quiz.html", context)


def download_quiz_file(request):
    # Get the filename from the GET request
    filename = request.GET.get("filename")

    # Construct the full path to the file
    file_path = os.path.join(settings.MEDIA_ROOT, "exports", filename)

    # Ensure the file exists
    if os.path.exists(file_path):
        # Open the file and serve it as a download response
        with open(file_path, "rb") as file:
            response = HttpResponse(
                file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("❌ File not found.")



def insert_question_method(request):
    return render(request, "home/insert_question_method.html")




def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            return render(request, 'home/partials/group-row.html', {'group': group})
        else:
            return HttpResponseBadRequest("Invalid data")
    else:
        form = GroupForm()
        return render(request, 'home/partials/group-modal.html', {'form': form})


def group_list(request):
    if request.user.is_authenticated:
        groups = Group.objects.filter(created_by=request.user)
    else:
        groups = Group.objects.none()
        
    print(f"Groups: {groups}")
    form= GroupForm()
    group_quiz_form = GroupQuizForm(user=request.user)  # If you filtered groups in the form's __init__

    return render(request, 'home/group-list.html', {'groups': groups , 'form': form , 'group_quiz_form': group_quiz_form})


def list_groups_members(request, group_id):
    # Get the group object by its ID
    group = get_object_or_404(Group, id=group_id)
    
    # Fetch all group invitations for this group, and get the users and their invitation statuses
    invitations = GroupInvitation.objects.filter(group=group)
    
    # Create a list of tuples containing user and their invitation status
    members = [(invitation.user, invitation.is_accepted) for invitation in invitations]
    form = GroupInvitationForm()
    return render(request, 'home/list-group-member.html', {'group': group, 'members': members , 'form': form})


def list_my_invited_group(request):
    if request.user.is_authenticated:
        invitations = GroupInvitation.objects.filter(user=request.user)
    else:
        invitations = GroupInvitation.objects.none()
        
    return render(request, 'home/list-my-invited-group.html', {'invitations': invitations})


def accept_invitation_view(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, user=request.user)
    invitation.accept_invitation()
    return redirect('invited_group')


def decline_invitation_view(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id, user=request.user)
    invitation.decline_invitation()
    return redirect('invited_group')




def user_group_quizzes(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    quizzes = GroupQuiz.objects.filter(group=group).select_related('quiz')

    user_results = UserQuizResult.objects.filter(user=request.user).select_related('group_quiz__quiz', 'group_quiz__group')

    print("User Results:")
    for result in user_results:
        print(f"Quiz: {result.group_quiz.quiz.name}, Group: {result.group_quiz.group.name}, Score: {result.score}, Answered: {result.is_answered}")

    return render(request, 'home/user-group-quizzes.html', {
        'group': group,
        'quizzes': quizzes,
        'user_results': user_results
    })




def group_quiz_results(request, group_id, quiz_id):
    group = get_object_or_404(Group, id=group_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    group_quiz = get_object_or_404(GroupQuiz, group=group, quiz=quiz)

    results = UserQuizResult.objects.filter(group_quiz=group_quiz).select_related('user')

    return render(request, 'home/group-quiz-results.html', {
        'group': group,
        'quiz': quiz,
        'results': results,
    })

def group_add_user(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == "POST":
        form = GroupInvitationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['email']
            invitation = form.save(commit=False)
            invitation.user = user
            invitation.group = group
            invitation.invited_by = request.user
            invitation.save()

            # Get the added user and their acceptance status
            members = [(invitation.user, invitation.is_accepted)]
            
            # Render just the row for the new user
            return render(request, 'home/partials/member-row.html', {'members': members, 'group': group})
        else:
            return HttpResponseBadRequest("Invalid data")
    else:
        form = GroupInvitationForm()
        return render(request, 'home/partials/group-user-modal.html', {'form': form, 'group': group})
    
def create_group_quiz(request):
    if request.method == "POST":
        form = GroupQuizForm(request.POST, user=request.user)
        if form.is_valid():
            group_quiz = form.save()
            return render(request, 'home/partials/group-quiz-row.html', {'group_quiz': group_quiz})
        else:
            return render(request, 'home/partials/group-quiz-modal.html', {'form': form})
    else:
        form = GroupQuizForm(user=request.user)
        return render(request, 'home/partials/group-quiz-modal.html', {'form': form})



def generate_quiz_ai(request):
    context = {}
    question_form = QuestionForm(request.POST, user=request.user)

    if request.method == "POST":
        if "save_db" in request.POST:
            # Same logic to save the questions to the database after reviewing them
            selected_quiz_id = request.POST.get("quiz")
            my_data = request.session.get("parsed_output")

            if not selected_quiz_id or not my_data:
                return HttpResponse("❌ Quiz ID or parsed data is missing.")

            quiz = get_object_or_404(Quiz, id=selected_quiz_id)

            for data in my_data:
                explanation_text = f"{data['explanation']}\n\nWhy Not Others?\n"
                for key, reason in data["why_not"].items():
                    explanation_text += f"- {key}: {reason or 'Not provided'}\n"

                question = Question.objects.create(
                    quiz=quiz,
                    text=data["question"],
                    explanation=explanation_text,
                    example_code=data.get("example")
                )

                correct_key = data["correct_answer"].lower()
                for key, answer_text in data["options"].items():
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=(key.lower() == correct_key)
                    )

            return redirect("quiz-questions", quiz_pk=selected_quiz_id)

        elif "generate_ai_quiz" in request.POST:
            try:
                selected_quiz_id = request.POST.get("quiz")
                num_questions = int(request.POST.get("num_questions"))

                # Fetch quiz details
                quiz = get_object_or_404(Quiz, id=selected_quiz_id)
                print(f"Selected Quiz ID: {selected_quiz_id}")
                print(f"Number of Questions: {num_questions}")
                subject_name = quiz.category.subject.name
                print(f"Subject Name: {subject_name}")
                category_name = quiz.category.name
                print(f"Category Name: {category_name}")
                quiz_name = quiz.name
                print(f"Quiz Name: {quiz_name}")

                
                # print("iam here ")
                quiz_data = ai_generate_quiz(subject_name, category_name, quiz_name, num_questions)
                # print(f"Quiz Data: {quiz_data}")
                try:
                    parsed_output = quiz_data
                except json.JSONDecodeError as e:
                    return HttpResponse(f"❌ Failed to parse script output as JSON: {str(e)}")

                context["script_output"] = parsed_output
                request.session["parsed_output"] = parsed_output

            except Exception as e:
                return HttpResponse(f"❌ Error: {e}")

    context["question_form"] = question_form
    return render(request, "home/generate_quiz_ai.html", context)