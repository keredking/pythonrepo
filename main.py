import os
from groq import Groq

# Create Groq client using API key from environment
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

if not os.environ.get("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY not set.")
    exit()

print("Groq Chatbot. Type 'quit' to exit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "quit":
        print("Goodbye!")
        break

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": question}
        ]
    )

    answer = completion.choices[0].message.content

    print("AI:", answer)
    print()