import google.generativeai as palm
import os
os.environ['PALM_API_KEY'] = "AIzaSyBpSQPlMLOFJcWmay8B685XwNmND-3mQGo"
palm.configure(api_key="AIzaSyBpSQPlMLOFJcWmay8B685XwNmND-3mQGo")

response = palm.generate_text(prompt="The opposite of hot is")
print(response.result)