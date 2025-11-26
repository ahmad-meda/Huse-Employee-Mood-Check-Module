def send_whatsapp_message(contact_number, response):
    print(f"Sending WhatsApp message to {contact_number}: {response}")

def generate_llm_response(company_id, employees, query, mobile_number):
    print(f"Generating LLM response for {mobile_number}: {employees} {query}")
    return "LLM response"

def sendLLMResponse(sender_employee, generate_llm_response):
    print(f"Sending LLM response to {generate_llm_response.mobile_number}: {generate_llm_response}")

def clear_session(contact_number):
    return contact_number