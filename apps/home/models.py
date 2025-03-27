from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
