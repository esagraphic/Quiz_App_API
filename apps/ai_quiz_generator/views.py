from home.models import Category
from apps.home.forms import QuestionForm
from django.shortcuts import render
from apps.ai_quiz_generator.ai.generators import generate_quiz_question

def generate_quiz_by_ai_view(request):
    generated_questions = []
    # context = {}
    question_form = QuestionForm()
    # categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        num_questions = int(request.POST.get("num_questions", 3))

        if category_id:
            category = Category.objects.get(id=category_id)
            topic = category.name  # Gemini will use this category name as the topic
            generated_questions = generate_quiz_question(topic, num_questions)

    # context['question_form'] = question_form
    return render(request, "home/generate_quiz_by_ai.html", {
        "categories": categories,
        "generated_questions": generated_questions,
        'question_form': question_form,
    })