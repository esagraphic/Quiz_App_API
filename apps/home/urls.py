from django.urls import path, re_path, include
from apps.home import views
from .views import (
    SubjectListView,
    CategoryDetailView,
    QuizDetailView,
    QuizQuestionsView,
    UpdateQuestionView,
    SubjectUpdateView,
    create_subject,
    CategoryUpdateView,
    QuizUpdateView,
    QuizDeleteView,
    update_question,
    delete_question,
    remove_user_from_subject,
    confirm_remove_subject,
    generate_quiz,
    download_quiz_file,
    insert_question_method,
    create_group,
    group_list,
    list_groups_members,
    list_my_invited_group,
    group_quiz_results,
    create_group,
    )

urlpatterns = [
    # Include API URLs separately
    path("api/v1/", include("apps.home.api_urls")),  # All API routes under /api/v1/

    # Web URLs
    path("subject-list", SubjectListView.as_view(), name="subject-list"),
    path("subjects/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("category/<int:pk>/quizzes/", QuizDetailView.as_view(), name="quiz-detail"),
    path("create-subject/", create_subject, name="create_subject"),
    path("add_question/", views.add_question, name="add_question"),
    path("create_category/", views.create_category, name="create_category"),
    path("create_quiz/", views.create_quiz, name="create_quiz"),


     # Update Button
    path('quiz/<int:quiz_pk>/', QuizQuestionsView.as_view(), name='quiz_questions'),
    path('quiz/questions/<int:question_pk>/update/', UpdateQuestionView.as_view(), name='update_question'),
    path('subjects/edit/<int:pk>/', SubjectUpdateView.as_view(), name='update_subject'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('quiz/edit/<int:pk>/', QuizUpdateView.as_view(), name='update_quiz'),
    
    #Delete Button
    path('quiz/delete/<int:pk>/', QuizDeleteView.as_view(), name='delete_quiz'),

    #Questions Update Button
    path('question/<int:question_id>/update/', views.update_question, name='update-question'),
    
    #question delete Button
    path('question/<int:question_id>/delete/', delete_question, name='delete-question'),
    
    # Quiz questions page
    path("quiz/<int:quiz_pk>/questions/", QuizQuestionsView.as_view(), name="quiz-questions"),
    
    # Remove the current logged-in user from the ManyToManyField
    path('subjects/remove/<int:subject_id>/', remove_user_from_subject, name='remove_subject'),
    path('subject/<int:subject_id>/confirm-remove/',confirm_remove_subject, name='confirm_remove_subject'),
    #excel file 
    path('generate_quiz/', generate_quiz, name='generate_quiz'),
    path('download_quiz_file/', download_quiz_file, name='download_quiz_file'),
    path("insert-question-method/", insert_question_method, name="insert_question_method"),


    path("groups_list/", group_list, name="group_list"),
    path("groups/create/", create_group, name="create_group"),

    path("group_members/<int:group_id>/", list_groups_members, name="group_members"),
    path("invited-group/", list_my_invited_group, name="invited_group"),
    path('invitation/<int:invitation_id>/accept/', views.accept_invitation_view, name='accept_invitation'),
    path('invitation/<int:invitation_id>/decline/', views.decline_invitation_view, name='decline_invitation'),
    path('group/<int:group_id>/quizzes/', views.user_group_quizzes, name='group_quizzes'),
    path('group/<int:group_id>/quiz/<int:quiz_id>/results/', group_quiz_results, name='group-quiz-results'),
    path('groups/<int:group_id>/add-user/', views.group_add_user, name='group_add_user'),
    path('group-quiz/create/', views.create_group_quiz, name='create_group_quiz'),
    path('generate-quiz-ai/', views.generate_quiz_ai, name='generate-quiz-ai'),






    # Matches any HTML file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
