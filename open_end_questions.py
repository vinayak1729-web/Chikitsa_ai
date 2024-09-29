import numpy as np

# List of questions
questions = [

"What is the most interesting thing you heard this week?",
"What’s the one thing you really want to do but have never done, and why?",
"Would you take a shot if the chance of failure and success is 50-50?",
"Which one would you prefer; taking a luxurious trip alone or having a picnic with people you love?",
"If your life was a book, what would the title be?",
"If you could be any animal, what would you be and why?",
"What is your favorite day of the week and why?",
"What do you do when you’re bored?",
"Shoe size?",
"Favorite color?",
"Favorite band (or artist)?",
"Favorite animal?",
"Favorite food?",
"One food you dislike?",
"Favorite condiment?",
"Favorite movie?",
"Last movie you saw in a theater?",
"Last book read?",
"Best vacation?",
"Favorite toy as a child?",
"One item you should throw away, but probably never will?",
"Superman, Batman, Spiderman, or Wonder Woman?",
"Chocolate or vanilla?",
"Morning person or night owl?",
"Cats or dogs?",
"Sweet or salty?",
"Breakfast or dinner?",
"Coffee or tea?",
"American food, Italian food, Mexican food, Chinese food, or other?",
"Clean or messy?",
"What is your favorite breakfast food?",
"What vegetable would you like to grow in a garden?",
"Tell about a childhood game you loved.",
"What’s your favorite dessert?",
"What’s your favorite month of the year and why?",
"Who is your favorite celebrity?",
"Which celebrity do you most resemble?",
"If you could go anywhere in the world, where would you go and why?",
"Share about one of your hobbies.",
"What’s a unique talent that you have?",
"Introvert or extrovert?",
"Describe yourself in three words.",
"Tell about a happy childhood memory.",
"Name three things (or people) that make you smile.",
"Are you doing what you truly want in life?",
"What are your aspirations in life?",
"How many promises have you made this past year and how many of them have you fulfilled?",
"Are you proud of what you’re doing with your life or what you’ve done in the past? Explain.",
"Have you ever abandoned a creative idea that you believed in because others thought you were a fool? Explain.",
"What would you prefer? Stable but boring work or interesting work with lots of workload?",
"Are you making an impact or constantly being influenced by the world?",
"Which makes you happier, to forgive someone or to hold a grudge? Explain.",
"Who do you admire and why?",
"What are your strengths?",
"What are your weaknesses?",
"Are you doing anything that makes you and people around you happy?",
"Tell about a short-term goal you have.",
"Tell about a health goal you have.",
"Tell about a long-term goal you have.",
"Tell about a value that is currently important to you.",
"What do you like most about yourself?",
"What do you like least about yourself?",
"What in life brings you joy?",
"What are you grateful for?",
"Who is the most influential person in your life and why?",
"Tell about one dream you have always had, but are too afraid to chase.",
"What is something you want to change about yourself and what are two things you can do to accomplish this?",
"Describe your perfect world. (Who would be in it, what would you be doing, etc.)",
"Where were you one year ago, where are you now, and where do you want to be a year from today?",
"Share about a character flaw you have.",
"What kind of a person do you want to be?",
"When is the last time you helped someone and what did you do?",
"Tell about a problem you have right now. What can you do to solve it?",

"Have you ever failed anyone who you loved or loved you? Explain.",
"Who is your favorite person?",
"What was it like growing up in your family?",
"What makes someone a good friend?",
"What happens when you’re rejected?",
"What makes a relationship healthy or unhealthy?",
"Would you rather break someone’s heart or have your heart broken?",

"As a child, what did you want to be when you grew up?",
"Tell about something you do well.",
"What’s your dream job?",
"What are your career goals?",
"What classes would you be most interested in taking?",
"Tell about a job you would hate doing.",
"Would you prefer to work with people or by yourself?",
"Would you ever do a job that was dangerous if it paid a lot of money?",
"Would you still work if you didn’t have to?",
"What do you want to do when you retire?",
"If you have a job, what do you like about it? Dislike?",
"How do you deal with difficult co-workers?",
"What qualities would you like your supervisor to have?",

"When was the last time you laughed, and what did you laugh at?",
"If happiness was a currency, how rich would you be?",
"How do you express happiness?",
"What are three healthy ways you can cope with anger?",
"What are three healthy ways you can cope with anxiety?",
"What does being happy mean to you?",
"If your mood was a weather forecast, what would it be?",
"Tell about a time you were happy.",
"Tell about a time you were heartbroken.",
"What is the difference between guilt and shame?",
"Is guilt a healthy emotion?",
"Can guilt be excessive?",
"Is there a such thing as “healthy shame”?",
"What makes you happy?",
"What makes you mad?",
"When do you feel afraid?",
"When do you feel lonely?",
"Share about the last time you felt guilty.",
"What embarrasses you?",

"How does one practice forgiveness (of self and others) from a religious point of view and from a non-religious point of view?",
"What does it mean to forgive?",
"Do you have to forgive to move forward?",
"What brings you meaning in life?",
"How do you define spirituality?",
"What’s the difference between religion and spirituality?",
"When do you feel most at peace?",
"Do you meditate? Why or why not?",

"If you could travel to the past in a time machine, what advice would you give to the 6-year-old you?",
"Would you break the rules because of something/someone you care about?",
"Are you afraid of making mistakes? Why or why not?",
"If you cloned yourself, which of your characteristics would you not want cloned?",
"What’s the difference between you and most other people?",
"Consider the thing you last cried about; does it matter to you now or will it matter to you 5 years from now?",
"What do you need to let go of in life?",
"Do you remember anyone you hated 10 years ago? Does it matter now?",
"What are you worrying about and what happens if you stop worrying about it?",
"If you died now, would you have any regrets?",
"What’s the one thing you’re most satisfied with?",
"If today was the end of the world, what would you do?",
"What would you do if you won the lottery?",
"If you could change one thing about yourself, what would it be?",
"How do you think others see you?",
"How do you get someone’s attention?",
"What masks do you wear?",
"Tell about a poor decision you made.",
"When is the last time you failed at something? How did you handle it?",
]

# Convert the list to a numpy array
questions_array = np.array(questions)

def get_random_open_questions():
    questions_array = np.array(questions)  # Convert list of questions to an array
    num_questions_to_select = 10  # Always select 10 questions
    return np.random.choice(questions_array, num_questions_to_select, replace=False)