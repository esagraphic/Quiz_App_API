from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from apps.home import views

from .views import (
    CategoryDetailView,
    CategoryViewSet,
    CatrgoryAPIView,
    CreateCategoryAPIView,
    CreateQuestionAPIView,
    CreateQuizAPIView,
    CreateSubjectAPIView,
    CustomObtainAuthToken,
    CustomUserViewSet,
    DeleteCategoryAPIView,
    DeleteQuestionAPIView,
    DeleteQuizAPIView,
    DeleteSubjectAPIView,
    QuestionAPIView,
    QuestionViewSet,
    QuizAPIView,
    QuizDetailView,
    QuizQuestionsView,
    QuizViewSet,
    SubjectListView,
    SubjectsAPIView,
    SubjectsDetailAPIView,
    SubjectViewSet,
    UpdateCategoryAPIView,
    UpdateQuestionAPIView,
    UpdateQuizAPIView,
    UpdateSubjectsAPIView,
    create_subject,
)

# Second way to implement the API
router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"quizzes", QuizViewSet, basename="quiz")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"users", CustomUserViewSet, basename="user")


urlpatterns = [
    path(
        "api-token-auth/", CustomObtainAuthToken.as_view(), name="api-token-auth"
    ),  # Add this line to get tokens via POST request
    # The home page
    # path('', views.index, name='home'),
    # Subject list page
    path("", SubjectListView.as_view(), name="subject-list"),
    path("subjects/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("category/<int:pk>/quizzes/", QuizDetailView.as_view(), name="quiz-detail"),
    path("create-subject/", create_subject, name="create_subject"),
    path("add_question/", views.add_question, name="add_question"),
    path("create_category/", views.create_category, name="create_category"),
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    # API GET
    path("lists/", SubjectsAPIView.as_view(), name="apisubject_list"),
    path("lists/<int>:pk", SubjectsDetailAPIView.as_view(), name="apisubject_datail"),
    path("lists-category/", CatrgoryAPIView.as_view(), name="apicategory_list"),
    path("list-quiz/", QuizAPIView.as_view(), name="quiz-list"),
    path(
        "quiz/<int:quiz_pk>/questions-API/",
        QuestionAPIView.as_view(),
        name="question-api-detail",
    ),
    # API Create
    path(
        "create-subject-api/", CreateSubjectAPIView.as_view(), name="create_subject_API"
    ),
    path(
        "create-category-api/",
        CreateCategoryAPIView.as_view(),
        name="create_category_API",
    ),
    path("create-quiz-api/", CreateQuizAPIView.as_view(), name="create_quiz_API"),
    path(
        "create-question-api/",
        CreateQuestionAPIView.as_view(),
        name="create_question_API",
    ),
    # API Update
    path(
        "update-subject-api/<int:pk>/",
        UpdateSubjectsAPIView.as_view(),
        name="update_subject_API",
    ),
    path(
        "update-category-api/<int:pk>/",
        UpdateCategoryAPIView.as_view(),
        name="update_category_API",
    ),
    path(
        "update-quiz-api/<int:pk>/", UpdateQuizAPIView.as_view(), name="update_quiz_API"
    ),
    path(
        "update-question-api/<int:pk>/",
        UpdateQuestionAPIView.as_view(),
        name="update_question_API",
    ),
    # API Delete
    path(
        "delete-subject-api/<int:pk>/",
        DeleteSubjectAPIView.as_view(),
        name="delete_subject_API",
    ),
    path(
        "delete-category-api/<int:pk>/",
        DeleteCategoryAPIView.as_view(),
        name="delete_category_API",
    ),
    path(
        "delete-quiz-api/<int:pk>/", DeleteQuizAPIView.as_view(), name="delete_quiz_API"
    ),
    path(
        "delete-question-api/<int:pk>/",
        DeleteQuestionAPIView.as_view(),
        name="delete_question_API",
    ),
    # Using the APIModelViewSet
    path("API-v1/", include(router.urls)),
    # Quiz questions page
    path(
        "quiz/<int:quiz_pk>/questions/",
        QuizQuestionsView.as_view(),
        name="quiz-questions",
    ),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
    # Git Token API
]
