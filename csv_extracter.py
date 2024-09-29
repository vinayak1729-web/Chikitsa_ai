
import csv
import os
# from gemini_ai import gemini_chat , 
def csv_to_string(file_path):
    result_string = ''
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                result_string += ', '.join(row) + '\n'  # Join row items and add newline for readability
    except FileNotFoundError:
        return f"Error: File {file_path} not found."
    return result_string

# Step 2: Access (read) the CSV content and print it
close_ended_path = 'responses/close_end_questions_responses.csv'
close_ended_response = csv_to_string(close_ended_path)
print(f"close_ended_response :\n{close_ended_response}")
open_ended_response= csv_to_string('responses/open_end_questions_responses.csv')
print(f"open_ended_response :\n{open_ended_response}")

# default_prompt=" this is my assesment of close ended questions and open ended questions , give feed back on me "

# judge_gemini = gemini_chat(default_prompt+close_ended_response+open_ended_response)