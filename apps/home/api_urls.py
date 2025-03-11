from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CustomObtainAuthToken,
    CustomUserViewSet,
    QuestionViewSet,
    QuizViewSet,
    SubjectViewSet,
    SubjectsAPIView,
    SubjectsDetailAPIView,
    CatrgoryAPIView,
    QuizAPIView,
    QuestionAPIView,
    CreateSubjectAPIView,
    CreateCategoryAPIView,
    CreateQuizAPIView,
    CreateQuestionAPIView,
    UpdateSubjectsAPIView,
    UpdateCategoryAPIView,
    UpdateQuizAPIView,
    UpdateQuestionAPIView,
    DeleteSubjectAPIView,
    DeleteCategoryAPIView,
    DeleteQuizAPIView,
    DeleteQuestionAPIView,
)

# API Router
router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"quizzes", QuizViewSet, basename="quiz")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"users", CustomUserViewSet, basename="user")

# API URL patterns
urlpatterns = [
    # Token Authentication
    path("api-token-auth/", CustomObtainAuthToken.as_view(), name="api-token-auth"),
    
    # API GET Requests
    path("lists/", SubjectsAPIView.as_view(), name="apisubject_list"),
    path("lists/<int:pk>/", SubjectsDetailAPIView.as_view(), name="apisubject_detail"),
    path("lists-category/", CatrgoryAPIView.as_view(), name="apicategory_list"),
    path("list-quiz/", QuizAPIView.as_view(), name="quiz-list"),
    path("quiz/<int:quiz_pk>/questions/", QuestionAPIView.as_view(), name="question-api-detail"),
    
    # API Create
    path("create-subject/", CreateSubjectAPIView.as_view(), name="create_subject_API"),
    path("create-category/", CreateCategoryAPIView.as_view(), name="create_category_API"),
    path("create-quiz/", CreateQuizAPIView.as_view(), name="create_quiz_API"),
    path("create-question/", CreateQuestionAPIView.as_view(), name="create_question_API"),
    
    # API Update
    path("update-subject/<int:pk>/", UpdateSubjectsAPIView.as_view(), name="update_subject_API"),
    path("update-category/<int:pk>/", UpdateCategoryAPIView.as_view(), name="update_category_API"),
    path("update-quiz/<int:pk>/", UpdateQuizAPIView.as_view(), name="update_quiz_API"),
    path("update-question/<int:pk>/", UpdateQuestionAPIView.as_view(), name="update_question_API"),
    
    # API Delete
    path("delete-subject/<int:pk>/", DeleteSubjectAPIView.as_view(), name="delete_subject_API"),
    path("delete-category/<int:pk>/", DeleteCategoryAPIView.as_view(), name="delete_category_API"),
    path("delete-quiz/<int:pk>/", DeleteQuizAPIView.as_view(), name="delete_quiz_API"),
    path("delete-question/<int:pk>/", DeleteQuestionAPIView.as_view(), name="delete_question_API"),

    # DRF Router
    path("", include(router.urls)),  # API-v1/
]
