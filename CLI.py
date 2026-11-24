from models import get_response
from conversation import conversation
import json

welcome_message = """===================================================
\t\tWelcome To ToolMate AI
===================================================
To use the chatbot, type 'start'.
To end the session, type 'exit'.
\n"""

print(welcome_message)

user_input = input("You: ")
while user_input != "start":
    print("Bot: Incorrect command. First, start the chatbot by typing 'start'\n")
    user_input = input("You: ")


while user_input != "exit":
    if user_input == "start":
        print("Bot: Hi! How can I help you?\n")
        
    elif not user_input.strip():
        print("Bot: Prompt is empty or contains only spaces. Provide a new prompt properly!\n")

    elif user_input == "printcv":
        cv=conversation
        print(cv)
        

    else:
        conversation.append({"role": "user", "content": user_input})
        response = get_response(conversation)
        conversation.append({"role": "assistant", "content": response})
        print(f"Bot: {response}")
    user_input = input("You: ")

print("Bot: Session Closed. Thank You!\n")