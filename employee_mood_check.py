from utils.dummy_functions import send_whatsapp_message, clear_session
from proxies.proxy import EmployeeProxy
from proxies.employee_session_proxy import EmployeeSessionProxy
from proxies.employee_mood_session_proxy import EmployeeMoodSessionProxy
from proxies.employee_message_proxy import EmployeeMessageHistoryProxy
from utils.agents import get_employee_mood_check_extraction, mood_check_response


def employee_mood_check(contact_number: str, user_message: str):
    print(f"[MoodCheck] Processing message from {contact_number}")
    employee_record = EmployeeProxy.get_employee_record(contact_number)
    print(f"[MoodCheck] Employee record found: {bool(employee_record)}")

    asked_user_feedback = EmployeeMoodSessionProxy.get_employee_asked_user_feedback(contact_number)
    print(f"[MoodCheck] Asked user feedback flag: {asked_user_feedback}")

    if asked_user_feedback is not True:
        follow_up_prompt = "Thank you so much for your feedback. May I know what made you feel that way?"
        send_whatsapp_message(contact_number, follow_up_prompt)
        print("[MoodCheck] Sent feedback follow-up prompt")
        EmployeeMessageHistoryProxy.save_message(contact_number, "user", follow_up_prompt)
        EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": follow_up_prompt})
        EmployeeMoodSessionProxy.set_employee_asked_user_feedback(contact_number, True)
        print("[MoodCheck] Marked asked_user_feedback in session")
        return True

    print(f"[MoodCheck] Recording user message: {user_message}")
    EmployeeMessageHistoryProxy.save_message(contact_number, "user", user_message)
    EmployeeSessionProxy.add_message(contact_number, {"role": "user", "content": user_message})
    session_messages = EmployeeSessionProxy.get_messages(contact_number)
    print(f"[MoodCheck] Loaded {len(session_messages)} session messages")
    # feedback_extraction = get_employee_mood_check_extraction(session_messages[-1:])
    # print(f"[MoodCheck] Feedback extraction: {feedback_extraction}")
    print(f"[MoodCheck] Latest session messages: {session_messages[-2:]}")  # show recent entries
    mood_check_response_message = mood_check_response(user_message)
    send_whatsapp_message(contact_number, mood_check_response_message.message_to_user)
    print(f"[MoodCheck] Sent response: {mood_check_response_message.message_to_user}")
    clear_session(contact_number)
    print("[MoodCheck] Cleared employee session data")
    EmployeeMoodSessionProxy.clear_employee_asked_user_feedback(contact_number)
    EmployeeSessionProxy.clear_messages(contact_number)
    print("[MoodCheck] Reset asked_user_feedback flag and cleared messages\n")
    return True

while True:
    user_message = input("\nUser: ")
    print("[MoodCheck] --- New Interaction ---")
    employee_mood_check(contact_number="+971509784398", user_message=user_message)
