from django.urls import path, re_path
from apps.home import views
from .views import  (CreateSubjectAPIView, QuizQuestionsView, SubjectListView, CategoryDetailView, QuizDetailView , create_subject,
                     SubjectsAPIView, SubjectsDetailAPIView, CatrgoryAPIView,QuizAPIView, QuestionAPIView, CreateCategoryAPIView, 
                     CreateQuizAPIView)

urlpatterns = [
    # The home page
    # path('', views.index, name='home'),
    
    # Subject list page
    path('', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/<int:pk>/quizzes/', QuizDetailView.as_view(), name='quiz-detail'),
    path('create-subject/', create_subject, name='create_subject'),
    path('add_question/', views.add_question, name='add_question'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),

    #api
    path('lists/',SubjectsAPIView.as_view(), name ='apisubject_list'),
    path('lists/<int>:pk',SubjectsDetailAPIView.as_view(), name ='apisubject_datail'),
    path('lists-category/',CatrgoryAPIView.as_view(), name ='apicategory_list'),
    path('list-quiz/', QuizAPIView.as_view(), name='quiz-list'),
    path('quiz/<int:quiz_pk>/questions/', QuestionAPIView.as_view(), name='question-api-detail'),
    
    #API CREATE
    path('create-subject-api/', CreateSubjectAPIView.as_view(), name ='create_subject_API'),
    path('create-category-api/', CreateCategoryAPIView.as_view(), name ='create_category_API'),
    path('create-quiz-api/', CreateQuizAPIView.as_view(), name ='create_quiz_API'),
    

    # Quiz questions page
    path('quiz/<int:quiz_pk>/questions/', QuizQuestionsView.as_view(), name='quiz-questions'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
