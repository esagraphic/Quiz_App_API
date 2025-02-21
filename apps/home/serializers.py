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
        fields = ['id','category','name','is_private']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        
        model= Question
        fields =['quiz','text','explanation','example_code','created_at','answers']
        
        
# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Answer
#         fields =['question','text','is_correct ']
