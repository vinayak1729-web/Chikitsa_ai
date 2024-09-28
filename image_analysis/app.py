from flask import Flask, render_template, request, redirect, url_for, session
import os
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Configure the Generative AI model
genai.configure(api_key="AIzaSyDOGMGkjh8e2YNUgcfzOkHER1q7Du4hrKY")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."
3. Your insights are invaluable in guiding clinical decisions. Please proceed with analysis, adhering to the structured approach outlined above.
"""

# Set up the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(request.url)

        if uploaded_file:
            # Process the uploaded image
            image_data = uploaded_file.read()

            # Prepare image parts
            image_parts = [{
                "mime_type": "image/jpeg",
                "data": image_data
            }]
            
            # Prepare the prompt parts
            prompt_parts = [
                image_parts[0],
                system_prompt,
            ]

            # Generate a response based on the prompt and image
            response = model.generate_content(prompt_parts)

            return render_template('result.html', analysis=response.text)

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)

