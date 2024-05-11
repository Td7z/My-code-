import discord
from discord.ext import commands
import os
import youtube_dl
from dislash import InteractionClient, Option, OptionType, slash_command

# Configurações do youtube-dl
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# Definir intents aqui
intents = discord.Intents.all()

# Substitua 'SEU_TOKEN_AQUI' pelo seu token real
DISCORD_TOKEN = 
BOT_ID = 1197174313149796485

# Inicializar o bot com o BOT_ID
bot = commands.Bot(command_prefix="!", intents=intents, application_id=BOT_ID)
inter_client = InteractionClient(bot)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    @slash_command(
        name="play",
        description="Reproduzir uma música.",
        options=[
            Option("query", "Nome da música ou URL.", OptionType.STRING, required=True),
        ],
    )
    async def play(self, ctx, query: str):
        await ctx.send("Processando...", ephemeral=True)
        
        try:
            # Verificar se o usuário está em um canal de voz.
            if not ctx.author.voice:
                raise commands.CommandError("Você precisa estar em um canal de voz para usar este comando.")

            # Entrar no canal de voz do usuário.
            try:
                self.voice_client = await ctx.author.voice.channel.connect()
            except discord.ClientException:
                raise commands.CommandError("Já estou conectado a um canal de voz.")

            # Procurar e reproduzir a música.
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(query, download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    URL = info['formats'][0]['url']
                except youtube_dl.utils.DownloadError:
                    raise commands.CommandError("Erro ao baixar informações da música. Verifique a URL.")

                try:
                    source = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
                    self.voice_client.play(source)
                except Exception as e:
                    raise commands.CommandError(f"Erro ao reproduzir a música: {e}")

                embed = discord.Embed(
                    title="Tocando",
                    description=f"Reproduzindo: {info['title']}",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
        except commands.CommandError as e:
            embed = discord.Embed(
                title="Erro",
                description=str(e),
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

# O bot deve ser inicializado apenas uma vez.
@bot.event
async def on_ready():
    print(f"Logado como {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.add_cog(Music(bot))

bot.run(DISCORD_TOKEN)
