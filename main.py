import asyncio
import os

import discord
import shutil
from dotenv import load_dotenv

from functions import is_cat

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CH_ID = int(os.getenv("CHANNEL_ID"))
IMAGE_DIR = "images"

# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# Botのイベントハンドラ
@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")
    channel = client.get_channel(CH_ID)
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

        # 空のディレクトリに添付画像を保存
        if os.path.exists(IMAGE_DIR):
            shutil.rmtree(IMAGE_DIR)
        os.makedirs(IMAGE_DIR, exist_ok=True)
        filepath = os.path.join(IMAGE_DIR, attachment.filename)
        await attachment.save(filepath)
        print(f"保存しました: {filepath}")

        # 猫判定
        try:
            is_cat_result = await asyncio.to_thread(is_cat, filepath)
            if is_cat_result:
                await message.channel.send("これは猫です")
            else:
                await message.channel.send("これは猫ではありません")
        except ValueError as e:
            await message.channel.send(f"画像形式エラー: {e}")
        except Exception as e:
            print(f"猫判定エラー: {e}")
            await message.channel.send("猫判定でエラーが発生しました")


client.run(TOKEN)
