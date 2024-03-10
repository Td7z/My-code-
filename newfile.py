from twitchio.ext import commands
from gemini import Gemini

# Credenciais da Twitch
client_id = "gp762nuuoqcoxypju8c569th9wz7q5"
oauth_token = "oauth:sum22gpyyij84mvo5d33zh84jhvwy2"

# Chave da API Gemini
gemini_api_key = "AIzaSyBa1IJ5GRXPRk3gPKAfjLExww67BJJArkU"

# Inicializa o bot
bot = commands.Bot(
    irc_token=oauth_token,
    client_id=client_id,
    nick="YOUR_BOT_USERNAME",
    prefix="!",
    initial_channels=["YOUR_TWITCH_CHANNEL"]
)

# Inicializa o cliente Gemini
gemini = Gemini(gemini_api_key)

@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return  # Ignora mensagens do próprio bot

    await bot.handle_commands(message)

@bot.command(name="gpt")
async def gpt_command(ctx, *, question):
    try:
        # Envia a pergunta para a API Gemini
        response = gemini.generate_text(prompt=question)
        
        # Responde no chat com a resposta da Gemini
        await ctx.send(f"{ctx.author.mention}, {response['text']}")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    bot.run()