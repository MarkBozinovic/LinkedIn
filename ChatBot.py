
import openai

openai.api_key="api-key"

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()

if __name__ == "__main__":
    print("ChatGPT Terminal Chat - type 'quit' to exit\n")
    while True:
        user_input = input("Hi, please chat with Chatgpt and type quit, exit, bye to exit: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        response = chat_with_gpt(user_input)
        print("ChatGPT:", response)
