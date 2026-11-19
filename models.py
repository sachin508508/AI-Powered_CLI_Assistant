from openai import OpenAI, _exceptions
from os import getenv
from dotenv import load_dotenv
from tools import tools, tool_register
from json import loads, dumps

load_dotenv()

weatherapi_key = getenv("WEATHERAPI_KEY")
api_key = getenv("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"
model = OpenAI(api_key=api_key,
               base_url=base_url)
model_name = "deepseek-flash"
system_instruction = """You are an helpful assistant, who provides very concise and clear response for the user queries. 
Whenever a tool is necessary to answer the user query, use the tool call correctly.
1. To use calculator tool, two values must be provided with a operation and the operation must be presented with any of the below names: 
["addition", "subtraction", "multiplication", "division"]. If any of the parameters not provided, ask the user to provide necessary information. Dont assume the result on your own, get the answers from the tool alone.
"""

def get_response(query):
    history = [
    {
        "role": "system", "content":system_instruction,
    },
    {
        "role": "user", "content": f"{query}"
    }
    ]
    try:
        while True:
            result = model.chat.completions.create(
                        model=model_name,
                        messages= history,
                        tools= tools,
                        tool_choice="auto"
                    )
            print("step1 working...")
            model_message = result.choices[0].message
            model_tools = model_message.tool_calls
            if not model_tools:
                response = model_message.content
                break

            history.append(model_message)

            print(f"Printing the history: \n\t {history}")

            for tool_call in model_tools:
                function_name = tool_call.function.name
                function_arguments = loads(tool_call.function.arguments)
                print("step2 working...")

                if function_name in tool_register:
                    tool_result = tool_register[function_name](**function_arguments)
                    print("step3 working...")
                    print(tool_result)
                else:
                    tool_result = {
                        "error": f"Tool {function_name} is not implemented yet!"
                        }

                history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": dumps(tool_result)

                })

                print(f"Printing the history: \n\t {history}")
            


        print(f"Printing the history: \n\t {history}")    
        response = result.choices[0].message.content

    except _exceptions.AuthenticationError:
        response = "Invalid API Key! Check the API key."

    except _exceptions.PermissionDeniedError:
        response = "Access Denied! Check the access permission."

    except _exceptions.RateLimitError:
        response = "Rate Limit Exceeded! Retry after waiting some time."

    except _exceptions.BadRequestError:
        response = "Invalid request parameter or payload! Check and provide valid request."

    except _exceptions.NotFoundError:
        response = "Incorrect endpoint or Model name! Check the endpoint/model configurations."

    except _exceptions.APITimeoutError:
        response = "Request Timeout! Retry again."

    except _exceptions.APIConnectionError:
        response = "Connection Issue! Check the API and network configurations and Retry later."

    except _exceptions.InternalServerError:
        response = "Error occurred in Server! Retry later."

    
    return response


# Below code for Testing purpose only.
user_query = input("You: ")
final_response = get_response(user_query)
print(f"\n\n\nBot: {final_response}")