BASE_PROMPT = """
You are an intelligent quiz generator.

Generate {num_questions} multiple-choice questions on the topic: "{topic}".

Return it in this exact JSON format:

{
  "question": "...",
  "options": {
    "a": "...",
    "b": "...",
    "c": "...",
    "d": "..."
  },
  "correct_answer": "a",
  "explanation": "...",
  "example": "...",
  "why_not": {
    "b": "...",
    "c": "...",
    "d": "..."
  }
}

Make sure:
Only one answer is correct.
The explanation is clear.
The JSON is valid.
"""