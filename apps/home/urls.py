from django.urls import path, re_path, include
from apps.home import views
from .views import (
    SubjectListView,
    CategoryDetailView,
    QuizDetailView,
    QuizQuestionsView,
    UpdateQuestionView,

    create_subject,
    remove_user_from_subject,
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


     # Update Button
    path('quiz/<int:quiz_pk>/', QuizQuestionsView.as_view(), name='quiz_questions'),
    path('quiz/questions/<int:question_pk>/update/', UpdateQuestionView.as_view(), name='update_question'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),


    # Quiz questions page
    path("quiz/<int:quiz_pk>/questions/", QuizQuestionsView.as_view(), name="quiz-questions"),
    
    # Remove the current logged-in user from the ManyToManyField
    path('subjects/remove/<int:subject_id>/', remove_user_from_subject, name='remove_subject'),
    # Matches any HTML file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
