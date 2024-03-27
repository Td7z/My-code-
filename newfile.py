import discord
import ffmpeg
import youtube_dl
import asyncio

client = discord.Client()

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

        # Conectar ao canal de voz do usuário
        if message.author.voice is None:
            await message.channel.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()

        # Tocar o áudio
        source = discord.FFmpegPCMAudio(video_url)
        voice_client.play(source)

        # Aguardar o término da reprodução
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Desconectar do canal de voz
        await voice_client.disconnect()

client.run('MTE2NDU0MjA2OTgxNDA4MzY4NA.GF7m8h.tUyVYIzcGkivklLYXol591-qW9j8kmu9LGli58')
