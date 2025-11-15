import google.generativeai as genai
import os

genai.configure(api_key='APIKEY')

model = genai.GenerativeModel('gemini-2.5-flash')

response = model.generate_content('generate me a dictionary in this python file with general emotions as keys and more specific words for those emotions as values')

print(response.text)

