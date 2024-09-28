import streamlit as st
import pandas as pd
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

#configure genai with api key
genai.configure(api_key="AIzaSyDOGMGkjh8e2YNUgcfzOkHER1q7Du4hrKY")
#Set up the model 
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

#apply safety settings
safety_settings = [
 {
     "category": "HARM_CATEGORY_HARASSMENT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
     "category": "HARM_CATEGORY_HATE_SPEECH",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
     "threshold": "BLOCK_MEDIUM_AND_ABOVE"   
 },
 
]

system_promt="""

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifyingany abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps:Based on your analysis, suggest potential next steps, including furthur tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response:Only respond if the image pertains to human health issues.
3. Your insights are invaluable in guiding clinical decisions. Please proceesd with analysis, adhering to the structured approach outlined above.

"""

#genai model config

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  safety_settings=safety_settings
)

#set page config

st.set_page_config(page_title="Doctor_BOT", page_icon=":robot:")

#set the logo

#st.image("#path", width=200)

#set the Title 

st.title("🏥 Dr. Bot 🤖: Your Virtual Medical Companion 💊🩺")

#set the subTitle 
st.subheader("An application that can help users to identify medical problems")
uploaded_file=st.file_uploader("Upload the medical image", type=["png","jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=250, caption="Uploaded Medical Image")
submit_button=st.button("GENERATE THE ANALYSIS")

if submit_button:
    #process the uploaded image
    image_data=uploaded_file.getvalue()
    
    #making our image ready
    image_parts = [
        {
        
        "mime_type": "image/jpeg",
      "data": image_data
        }
    ]
    
    #making our promt ready
    prompt_parts=[
        
        image_parts[0],
        system_promt,
    ]
    
    #generate a response based on promt and image
    
    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the analysis based on your image")
        st.write(response.text)
    