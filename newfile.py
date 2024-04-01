import twitchio
from twitchio.ext import commands
import google.generativeai as genai
import speech_recognition as sr  # Example speech recognition library

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

# Speech recognition setup
recognizer = sr.Recognizer()

@bot.event
async def event_message(ctx):
    if ctx.content.lower() == "ok gpt":
        await ctx.send("Faça sua pergunta:")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            question = recognizer.recognize_google(audio, language="pt-BR")
            response = chat.send_message(question)
            await ctx.send(f"Gemini: {response.text}")
        except sr.UnknownValueError:
            await ctx.send("Não entendi a pergunta.")
        except sr.RequestError as e:
            await ctx.send(f"Erro ao processar a pergunta: {e}")

bot.run()
