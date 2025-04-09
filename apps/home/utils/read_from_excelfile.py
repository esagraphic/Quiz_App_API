import openpyxl

# Load the Excel file
wb = openpyxl.load_workbook('quiz_template_2_20250409_095114.xlsx')
# Check if the file was loaded successfully
ws = wb.active  # Assuming the data is in the first sheet

# Initialize the list to store the data
my_data = []

# Iterate through the rows (skip the header)
for row in ws.iter_rows(min_row=2, values_only=True):
    # Check if the question is empty or None, skip this row if true
    if not row[1]:
        continue
    
    data = {
        "question": row[1],  # Column for question
        "options": {
            "a": row[2],  # Answer 1
            "b": row[3],  # Answer 2
            "c": row[4],  # Answer 3
            "d": row[5]   # Answer 4
        },
        "correct_answer": row[6],  # Correct answer
        "explanation": row[7],  # Explanation
        "example": row[8],  # Example code
        "why_not": {
            "a": row[9],  # Why not answer a
            "b": row[10], # Why not answer b
            "c": row[11], # Why not answer c
            "d": row[12]  # Why not answer d
        }
    }
    my_data.append(data)

# Save the list as a Python file in the same directory
with open('exported.py', 'w') as file:
    file.write(f"my_data = {my_data}")
