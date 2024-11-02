import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv('.env')

genai.configure(api_key=os.getenv('API-KEY'))

def bot(msg):
    model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="You are a programmer with high knowledge of artificial intelligence and reasoning")
    response = model.generate_content(msg)
    return response.text
    print(response)