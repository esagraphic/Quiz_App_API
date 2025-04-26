import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def ai_generate_quiz(subject_name, category_name, quiz_name, num_questions):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY environment variable not found.")

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"❌ Error initializing Gemini client: {e}")

    model_name = "gemini-1.5-flash"

    prompt_template = f"""
Please generate {num_questions} quiz questions based on the following specifications:

**Inputs:**
* Subject: {subject_name}
* Category: {category_name}
* Quiz Name/Topic: {quiz_name}

**Output Format:**
Generate a JSON list containing exactly {num_questions} dictionary objects. Each dictionary represents a single quiz question and must adhere to the following structure:

[
  {{
    "question": "String: The text of the quiz question.",
    "options": {{
      "a": "String: Option A",
      "b": "String: Option B",
      "c": "String: Option C",
      "d": "String: Option D"
    }},
    "correct_answer": "String: A single character ('a', 'b', 'c', or 'd') indicating the correct option.",
    "explanation": "String: A detailed explanation of why the correct answer is right.",
    "example": "String or null: If the question relates to IT or programming, provide a relevant code snippet as a string. Otherwise, provide null.",
    "why_not": {{
      "a": "String or null: Brief explanation why option A is incorrect, or null if it's the correct answer.",
      "b": "String or null: Brief explanation why option B is incorrect, or null if it's the correct answer.",
      "c": "String or null: Brief explanation why option C is incorrect, or null if it's the correct answer.",
      "d": "String or null: Brief explanation why option D is incorrect, or null if it's the correct answer."
    }}
  }}
]
"""

    contents = [types.Content(role="user", parts=[types.Part(text=prompt_template)])]

    full_response_text = ""
    try:
        stream = client.models.generate_content_stream(
            model=f"models/{model_name}",
            contents=contents
        )

        for chunk in stream:
            chunk_text = getattr(chunk, 'text', '')
            full_response_text += chunk_text

        if not full_response_text.strip():
            raise ValueError("❌ Received an empty response from the API.")

        # ✅ Clean markdown-style formatting
        cleaned_output = re.sub(r"^```json|```$", "", full_response_text.strip(), flags=re.MULTILINE).strip()

        try:
            parsed_data = json.loads(cleaned_output)

            if not isinstance(parsed_data, list):
                raise ValueError("❌ Expected a JSON list as output.")

            if len(parsed_data) != num_questions:
                print(f"⚠️ Warning: Expected {num_questions} questions, got {len(parsed_data)}")

            return parsed_data

        except json.JSONDecodeError as json_error:
            raise ValueError(f"❌ Error decoding JSON: {json_error}\n\nRaw content:\n{cleaned_output}")

    except Exception as e:
        raise RuntimeError(f"❌ An error occurred while generating content: {e}")
