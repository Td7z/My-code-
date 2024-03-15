import google.generativeai as genai
from twitchio.ext import commands

# Replace with your credentials
client_id = "gp762nuuoqcoxypju8c569th9wz7q5"
oauth_token = "oauth:ot0ukv78m0yb4yn72gwm0xz8ptgyo2"
channel_name = "gg_celoso"

genai.configure(api_key="AIzaSyBa1IJ5GRXPRk3gPKAfjLExww67BJJArkU")

# Find a model that supports content generation
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        model_name = m.name  # Store the model name
        break  # Stop after finding one

# Initialize the model and chat
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

# Initialize the bot
bot = commands.Bot(
    token=oauth_token,
    client_id=client_id,
    nick=channel_name,
    prefix="!",
    initial_channels=[channel_name],
)

# Function to generate personalized greetings
def generate_greeting():
    greetings = [
        "Boas vendas!",
        "Que suas vendas sejam incríveis!",
        "Muitos clientes para você!",
    ]
    return greetings[random.randint(0, len(greetings) - 1)]

# Store users who have already been greeted
greeted_users = set()

@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return  # Ignore messages from the bot itself

    # Check if the user has been greeted before
    if message.author.name not in greeted_users:
        # Generate and send a personalized greeting
        greeting = generate_greeting()
        await message.channel.send(f"{message.author.name}, {greeting}")
        greeted_users.add(message.author.name)

    # Check if the message is empty
    if not message.content:
        # Send a funny reaction or question
        reactions = [
            f"{message.author.name}, você está aí?",
            f"{message.author.name}, esqueceu de digitar algo?",
            f"*{message.author.name} está digitando...*",
        ]
        await message.channel.send(random.choice(reactions))

    await bot.handle_commands(message)

@bot.command(name="gpt")
async def gpt_command(ctx, *, question):
    try:
        response = chat.send_message(question)
        # Send the response in chunks of 300 characters or less
        for chunk in split_message(response.text):
            await ctx.send(chunk)
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

def split_message(message):
    """Splits a message into chunks of 300 characters or less."""
    chunks = []
    while message:
        chunk, message = message[:300], message[300:]
        chunks.append(chunk)
    return chunks

# Start the bot
if __name__ == "__main__":
    bot.run()