import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def chatbot_response(user_input):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Answer the student's query: {user_input}",
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Example usage
print(chatbot_response("What is the exam schedule for next week?"))
