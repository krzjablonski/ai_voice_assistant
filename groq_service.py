import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def groq_answer_question(question_text: str) -> str:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question_text,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    question = input("What is your question? ")
    print(groq_answer_question(question))
