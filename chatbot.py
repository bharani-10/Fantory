import google.generativeai as genai
import speech_recognition as sr  # For voice input
import pyttsx3  # For AI voice output

# Replace with your actual Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")  # More stable than "gemini-2.0-flash"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speaking speed

# Stores chat history for better responses
chat_history = []

# Function to make AI speak
def speak(text):
    """ Converts text to speech """
    engine.say(text)
    engine.runAndWait()

# Function to get voice input from user
def listen():
    """ Listens to user voice input and converts it to text """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Say 'quit' to exit)")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You (voice): {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Couldn't understand. Try again!")
            return None
        except sr.RequestError:
            print("Speech service error.")
            return None

# Function to chat with AI
def chat_with_ai(user_input):
    """ Sends user input to Gemini AI and gets a response """
    global chat_history

    # Store user input in chat history
    chat_history.append({"role": "user", "text": user_input})

    # Send chat history to Gemini AI
    response = model.generate_content([msg["text"] for msg in chat_history])

    # Extract AI response text
    ai_response = response.text if response else "I'm not sure how to respond."

    # Store AI response in chat history
    chat_history.append({"role": "assistant", "text": ai_response})

    # AI speaks the response
    speak(ai_response)

    return ai_response

# Start voice-enabled chatbot
print("Chatbot: Hi! Speak or type to chat. Say 'quit' or type 'q' to exit.")
speak("Hi! Speak or type to chat. Say 'quit' to exit.")

while True:
    user_input = listen()  # Get voice input
    if user_input is None:
        user_input = input("You (text): ")  # Fallback to text input if voice fails

    if user_input.lower() in ["q", "quit"]:
        print("Chatbot: Goodbye!")
        speak("Goodbye!")
        break

    response = chat_with_ai(user_input)
    print("Chatbot:", response)
