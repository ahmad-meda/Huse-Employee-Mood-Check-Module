from utils.formats import MoodCheckResponse, GetEmployeeMoodCheckExtraction        
from utils.ai_client import client
from Files.SQLAlchemyModels import Employee
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

model = "gpt-5.1"


def mood_check_response(message: str):
    system_message = [
        {
            "role": "system",
            "content": (
                f"""You are an extremely professional HR Chatbot. Generate a system like farwell single ackowledgement HR Like professional Reply to the message of the user who has been asked his how his week was at work: {message}
                The message should be a single acknowledgement and not a conversation
                Example:
                Input: "I don't like my manager"
                Output: "I will escalate this matter to upper management right away so we can address this situation and find a resolution that works for you."
                    """
            )
        }
    ] 

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=MoodCheckResponse,
        temperature=0.5
    )

    return completion.choices[0].message.parsed

def get_employee_mood_check_extraction(messages: list):
    system_message = [
        {
            "role": "system",
            "content": (
                f"""
                The user has rated his mood for the week from 1 to 5 and he has been asked to give the reason for his mood.
                You are a data extraction assistant used for extracting the reason the employee is feeling a certain mood.
                """
            )
        }
    ] + messages
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=system_message,
        response_format=GetEmployeeMoodCheckExtraction,
        temperature=0.1
    )
    return completion.choices[0].message.parsed