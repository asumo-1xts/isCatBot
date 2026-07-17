import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True  # on_messageを使うなら必須

# Client作成時にintentsを渡す
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!neko":
        await message.channel.send("にゃーん")


client.run(TOKEN)
