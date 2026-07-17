import os

import discord
from dotenv import load_dotenv

from functions import is_cat

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
IMAGE_DIR = "images"

# 保存先ディレクトリ
os.makedirs(IMAGE_DIR, exist_ok=True)

# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# Botのイベントハンドラ
@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is not None:
        await channel.send("猫判定botがログインしました")


# メッセージ受信時のイベントハンドラ
@client.event
async def on_message(message):
    # テストコマンド
    if message.content == "!neko":
        await message.channel.send("にゃーん")
        return

    # Bot自身のメッセージは無視
    # 添付ファイルがない場合も無視
    if message.author.bot or not message.attachments:
        return

    # 添付ファイルを精査
    for attachment in message.attachments:
        # 画像以外は無視
        if attachment.content_type is None or not attachment.content_type.startswith(
            "image/"
        ):
            continue

        # 添付画像を保存
        filepath = os.path.join(IMAGE_DIR, attachment.filename)
        await attachment.save(filepath)
        print(f"保存しました: {filepath}")

        # 猫判定
        if is_cat(filepath):
            await message.channel.send("これは猫です")
        else:
            await message.channel.send("これは猫ではありません")


client.run(TOKEN)
