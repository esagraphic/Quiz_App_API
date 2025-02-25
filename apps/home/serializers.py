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
        fields =['id','quiz','text','explanation','example_code','created_at','answers']

class QuestionCreateSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)  # Remove read_only=True to allow updates

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'explanation', 'example_code', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])  # Extract answers data
        question = Question.objects.create(**validated_data)  # Create the question

        # Create answers linked to this question
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question  # ✅ Must return the created question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', [])  # Extract new answers data
        instance.quiz = validated_data.get('quiz', instance.quiz)
        instance.text = validated_data.get('text', instance.text)
        instance.explanation = validated_data.get('explanation', instance.explanation)
        instance.example_code = validated_data.get('example_code', instance.example_code)
        instance.save()

        # ✅ Update or Replace Existing Answers
        instance.answers.all().delete()  # Remove old answers
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)  # Add new answers

        return instance  # ✅ Must return the updated question
