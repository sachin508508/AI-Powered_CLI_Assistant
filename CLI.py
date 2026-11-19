from models import get_response
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
        print("Bot: Hi There! How can I help you?\n")
        
    elif not user_input.strip():
        print("Bot: Prompt is empty or contains only spaces. Provide the prompt properly!\n")

    else:
        response = get_response(user_input)
        print(f"Bot: {response}")

    user_input = input("You: ")

print("Bot: Session Closed. Thank You!\n")