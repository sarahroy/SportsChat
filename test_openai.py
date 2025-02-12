import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

try:
    client = openai.OpenAI(api_key=api_key)  # Create an OpenAI client
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, how are you?"}]
    )
    print(response.choices[0].message.content)
except openai.OpenAIError as e:
    print("OpenAI API Error:", e)
