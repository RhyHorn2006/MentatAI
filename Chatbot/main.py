import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)

with open("Chatbot/dune_wiki.txt", "r", encoding="utf-8") as f:
    dune_context = f.read()
    
mentat_persona = (
    "You are a Mentat advisor from the Dune universe. You speak logically, analytically, "
    "and only use the knowledge provided. Do not guess. Use this data to answer questions:\n\n"
    + dune_context[:12000]
)

def chat(user_prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": mentat_persona},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat(user_input)
        print("MentatAi: ", response)