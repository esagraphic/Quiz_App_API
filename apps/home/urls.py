from django.urls import path, re_path, include
from apps.home import views
from .views import (
    SubjectListView,
    CategoryDetailView,
    QuizDetailView,
    QuizQuestionsView,
    create_subject,
    generate_quiz,
)

urlpatterns = [
    # Include API URLs separately
    path("api/v1/", include("apps.home.api_urls")),  # All API routes under /api/v1/

    # Web URLs
    path("", SubjectListView.as_view(), name="subject-list"),
    path("subjects/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("category/<int:pk>/quizzes/", QuizDetailView.as_view(), name="quiz-detail"),
    path("create-subject/", create_subject, name="create_subject"),
    path("add_question/", views.add_question, name="add_question"),
    path("create_category/", views.create_category, name="create_category"),
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    
    # Quiz questions page
    path("quiz/<int:quiz_pk>/questions/", QuizQuestionsView.as_view(), name="quiz-questions"),
    
    #excel file 
     path('generate_quiz/', generate_quiz, name='generate_quiz'),
    # Matches any HTML file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
