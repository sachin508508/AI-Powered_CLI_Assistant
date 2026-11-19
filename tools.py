from typing import Dict, Callable
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
weatherapi_key = os.getenv("WEATHERAPI_KEY")


"""
Available tools
"""
# Tool 1: Calculator
def calculator(operation: str, operand1: int, operand2: int):
    if operation == "addition":
        return operand1 + operand2

    elif operation == "subtraction":
        return operand1 - operand2

    elif operation == "multiplication":
        return operand1 * operand2

    elif operation == "division":
        return operand1 / operand2

    else:
        return 0

# Tool 2: WeatherAPI
def weather(city):
    data = requests.api.get(
        url="https://api.weatherapi.com/v1/current.json",
        params={"key":weatherapi_key, "q":city, "aqi": "no"}).json()
    return {
        "City":data["location"]["name"], 
        "Country": data["location"]["country"], 
        "Temperature (in Celsius)": data["current"]["temp_c"],
        "Wind Speed (in kph)": data["current"]["wind_kph"], 
        "Humidity": data["current"]["humidity"], 
        "Condition": data["current"]["condition"]["text"]
        }



"""
Tool Definitions
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform primary arithmetic operations with 2 values",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Arithmetic operation name"
                    },
                    "operand1": {
                        "type": "integer",
                        "description": "First operand or value"
                    },
                    "operand2": {
                        "type": "integer",
                        "description": "Second operand or value"
                    },
                },
                "required": ["operation", "operand1", "operand2"]
            },
        }
              
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Provide weather information based on location",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Location/City name"
                    }
                },
                "required": ["city"]
            }
        }
    }
]



"""
Tool Registry
"""
tool_register: Dict[str, Callable] = {
    "calculator": calculator,
    "weather": weather
}