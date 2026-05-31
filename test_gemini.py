import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

response = model.generate_content("""
Analyze these blood test values:
Glucose: 180
Haemoglobin: 11
Cholesterol: 250

Give a short health risk assessment in 1 sentence.
""")

print(response.text)