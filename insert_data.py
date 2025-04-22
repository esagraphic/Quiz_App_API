import os
import django
from data  import my_data

# Set up Django environment
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.home.models import Quiz, Question, Answer

# Create a new quiz
quiz = Quiz.objects.create(
    category_id=15,  # Set category ID
    name="Forms and Auth",  # Set quiz name
    is_private=False
)

# Define questions and insert them

django_quiz = my_data


for data in django_quiz:
    explanation_text = f"{data['explanation']}\n\nWhy Not Others?\n"
    for key, reason in data["why_not"].items():
        explanation_text += f"- {key}: {reason}\n"

    question = Question.objects.create(
        quiz=quiz,
        text=data["question"],
        explanation=explanation_text,
        example_code=data["example"]
    )

    for key, answer_text in data["options"].items():
        Answer.objects.create(
            question=question,
            text=answer_text,
            is_correct=(key == data["correct_answer"])
        )

print("Quiz, questions, and answers inserted successfully!")
