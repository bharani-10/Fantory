import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyCa3Ag32NQUlkbe5LEwEH67z08uPNT4hYg")

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to send a request to Gemini AI
def chat_with_ai(prompt):
    response = model.generate_content(prompt)
    return response.text  # Extract AI response text

# Continuous chat loop
while True:
    user_input = input("You: ")  # Take user input
    if user_input.lower() == "q":  # Exit condition
        print("Chatbot: Goodbye!")
        break
    response = chat_with_ai(user_input)  # Get AI response
    print("Chatbot:", response)  # Print AI response 