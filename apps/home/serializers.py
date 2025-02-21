from rest_framework import serializers
from .models import Subject, Category, Quiz, Question, Answer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'subject']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['category','name','is_private']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields =['quiz','text','explanation','example_code','created_at']
        
        