import discord
import asyncio
import youtube_dl
import subprocess

intents = discord.Intents.default()
intents.voice_states = True

# Ligação/conexão ao Bot
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Estou Online!', client.user.name)

@client.event
async def on_message(message):
    if message.content.lower().startswith('!play'):
        # Extrair o URL do vídeo do comando
        url = message.content.split(' ', 1)[1]

        # Download do vídeo usando youtube_dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['formats'][0]['url']

        # Iniciar a reprodução do áudio no canal de voz
        voice_channel = message.author.voice.channel
        if voice_channel:
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(video_url), after=lambda e: print('done', e))
        else:
            await message.channel.send('Você precisa estar em um canal de voz para usar esse comando.')

client.run('MTE2NDU0MjA2OTgxNDA4MzY4NA.G55NHE.fAoUqday6nyhg86BiE6-P6-CUk9ilwKwywc7rA')
