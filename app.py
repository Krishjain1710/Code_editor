import openai
import os

api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment
client = openai.OpenAI(api_key=api_key)  # Initialize OpenAI client

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello, AI!"}],
    max_tokens=100
)

print(response.choices[0].message.content)  # Print AI response

