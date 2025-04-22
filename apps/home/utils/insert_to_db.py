import os
import django
import sys
import ast  # Import ast to safely parse the input data

# Set up Django environment
sys.path.append('/System/Volumes/Data/Dci Programing /Django /Lessons/All excersize /quiz_with_postgressql/Quiz_App_API')  # Add project root to Python path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Ensure 'core' is the correct settings module
django.setup()

from apps.home.models import Quiz, Question, Answer

# Specify the quiz ID you want to use
quiz_id = sys.argv[1]
print(f"Quiz ID: {quiz_id}")

# Try to fetch the existing quiz by ID
try:
    quiz = Quiz.objects.get(id=quiz_id)
except Quiz.DoesNotExist:
    print(f"Quiz with ID {quiz_id} does not exist.")
    exit()  # Exit if the quiz is not found

# Parse the input data (string) into a Python object
try:
    django_quiz = ast.literal_eval(sys.argv[2])  # Safely parse the input string
    if not isinstance(django_quiz, list):
        raise ValueError("Parsed data is not a list.")
except (ValueError, SyntaxError) as e:
    print(f"Error parsing input data: {e}")
    exit()

# Insert questions and answers into the database
for data in django_quiz:
    explanation_text = f"{data['explanation']}\n\nWhy Not Others?\n"
    for key, reason in data["why_not"].items():
        explanation_text += f"- {key}: {reason}\n"

    question = Question.objects.create(
        quiz=quiz,  # Use the existing quiz object
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

print("Questions and answers inserted successfully!")
