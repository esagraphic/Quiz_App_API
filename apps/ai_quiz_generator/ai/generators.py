import google.generativeai as genai
from django.conf import settings
from .prompts import BASE_PROMPT

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_quiz_question(category, num_of_questions):
    model = genai.GenerativeModel('gemini-pro')
    prompt = BASE_PROMPT.format(category=category, num_of_questions=num_of_questions)

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Gemini will return the JSON as a string — use eval or json.loads if safe
        quiz_data = eval(response_text)  # You can replace with json.loads if format is strict

        return quiz_data
    except Exception as e:
        return {"error": str(e)}