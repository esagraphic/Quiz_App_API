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

class QuestionCreateSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['quiz', 'text', 'explanation', 'example_code', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')  # Extract answers data
        question = Question.objects.create(**validated_data)  # Create the question