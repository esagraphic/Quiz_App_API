from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="subjects" )  


    def __str__(self):
        return self.name

class Category(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="category" )  


    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="quizzes")
    name = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="quiz" )  


    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    example_code = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"
    



class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_groups")
    

    # Invited users through GroupInvitation
    invited_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='GroupInvitation',
        related_name="invitations"
    )

    def __str__(self):
        return self.name

class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    

    def accept_invitation(self):
        self.is_accepted = True
        self.save()

    def decline_invitation(self):
        self.is_accepted = False
        self.save()

    def __str__(self):
        return f"Invitation to {self.user.email} for {self.group.name}"
    
class GroupQuiz(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="quizzes")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name} - {self.quiz.name}"
    


class UserQuizResult(models.Model):
    group_quiz = models.ForeignKey(GroupQuiz, on_delete=models.CASCADE, related_name="user_results")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_answered = models.BooleanField(default=False)
    

    def submit(self, score, time_taken):
        self.score = score
        self.time_taken = time_taken
        self.is_answered = True
        self.save()

    def __str__(self):
        return f"Result of {self.user.email} for {self.group_quiz.quiz.name}"