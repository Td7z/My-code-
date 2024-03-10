from twitchio.ext import commands
import google.generativeai

# Twitch credentials
client_id = "gp762nuuoqcoxypju8c569th9wz7q5"
oauth_token = "oauth:sum22gpyyij84mvo5d33zh84jhvwy2"

# Initialize the bot
bot = commands.Bot(
    token=oauth_token,
    client_id=client_id,
    nick="hawkinngx",
    prefix="!",
    initial_channels=["zerinonze"],
)

# Initialize the Gemini client (might require additional credentials)
gemini = gemini.Client()

@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return  # Ignore messages from the bot itself
    await bot.handle_commands(message)

@bot.command(name="gpt")
async def gpt_command(ctx, *, question):
    try:
        # Send the question to the Gemini API
        response = gemini.generate_text(prompt=question)

        # Respond in chat with the response from Gemini
        await ctx.send(f"{ctx.author.mention}, {response['text']}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

if __name__ == "__main__":
    bot.run()