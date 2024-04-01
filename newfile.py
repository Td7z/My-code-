import twitchio
from twitchio.ext import commands
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key="your_api_key")

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

@bot.command(name='gemini')
async def gemini_question(ctx, *, question):
    response = chat.send_message(question)
    await ctx.send(f"Gemini: {response.text}")

bot.run()
