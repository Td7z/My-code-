import twitchio
from twitchio.ext import commands
import google.generativeai as genai
import speech_recognition as sr

# Configure Gemini AI
genai.configure(api_key="AIzaSyBa1IJ5GRXPRk3gPKAfjLExww67BJJArkU")

# Find a suitable Gemini model
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name
        break  # Use the first suitable model

model = genai.GenerativeModel(model_name)

# Start Gemini chat globally
chat = model.start_chat(history=[])

# Twitch bot setup
bot = commands.Bot(
    token='oauth:b7wcmiqrdq8l8qem9r1wjfbtjk5w3z',
    client_id='gp762nuuoqcoxypju8c569th9wz7q5',
    nick='hawkinngx',
    prefix='!',
    initial_channels=['hawkinngx']
)

# Function to handle voice input
def listen_and_ask_gemini():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'ok Gemini' followed by your question:")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if text.startswith("ok Gemini"):
            question = text.replace("ok Gemini", "").strip()
            response = chat.send_message(question)
            print(f"Gemini: {response.text}")
        else:
            print("Didn't hear 'ok Gemini' at the beginning.")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from speech recognition service; {e}")

# Command for manual text input
@bot.command(name='gemini')
async def gemini_question(ctx, *, question):
    response = chat.send_message(question)
    await ctx.send(f"Gemini: {response.text}")

# Start listening for voice input
listen_and_ask_gemini()

# Run the Twitch bot
bot.run()
