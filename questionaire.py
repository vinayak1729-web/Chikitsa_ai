import numpy as np

# List of questions
questions = [
    "Have you been feeling depressed or sad lately?",
    "Do you often feel overwhelmed or anxious?",
    "Have you been experiencing difficulty sleeping or eating?",
    "Do you find yourself isolating yourself from others?",
    "Have you been having thoughts of harming yourself or others?",
    
    "Do you have any unhealthy coping mechanisms, such as substance abuse or excessive gambling?",
    "Do you engage in any self-harm behaviors?",
    "Have you tried talking to someone about your feelings?",
    "Do you practice any stress-relief techniques, such as meditation or exercise?",
    
    "Do you have a strong support system of friends and family?",
    "Do you feel comfortable talking to someone about your mental health concerns?",
    "Have you considered seeking professional help from a therapist or counselor?",
    
    "Do you often feel good about yourself?",
    "Do you believe you are capable of achieving your goals?",
    "Have you been experiencing feelings of inadequacy or worthlessness?",
    
    "Do you have healthy and supportive relationships?",
    "Are you able to express your feelings openly and honestly?",
    "Have you been experiencing conflict or difficulties in your relationships?",
    
    "Have you experienced any traumatic events in your life?",
    "Do you struggle with flashbacks or nightmares?",
    "Have you been feeling overwhelmed or stressed by recent events?",
    
    "Do you use any substances, such as alcohol or drugs?",
    "Have you noticed any negative consequences from your substance use?",
    "Have you considered seeking help for substance abuse?"
]

# Convert the list to a numpy array
questions_array = np.array(questions)

# Randomly select 10 questions from the array
random_questions = np.random.choice(questions_array, 10, replace=False)

# Print the randomly selected questions
for i, question in enumerate(random_questions, 1):
    print(f"{i}. {question}")
