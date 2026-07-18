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
    # 指定されたチャンネル以外は無視
    if message.channel.id != CH_ID:
        return

    # テストコマンド
    if message.content == "!neko":
        await message.channel.send("v1.1.0: にゃーん")
        return

    # 添付ファイルがない場合も無視
    if not message.attachments:
        return

    # 添付ファイルを精査
    for attachment in message.attachments:
        # ファイル形式が不明の場合は無視
        if attachment.content_type is None:
            continue

        # ファイル形式が画像でない場合も無視
        if not attachment.content_type.startswith("image/"):
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
            if is_cat_result == 1:
                await message.reply("むむ、これは猫です", mention_author=False)
            elif is_cat_result == 0:
                await message.add_reaction("👀")
            else:
                await message.reply(
                    "Geminiに意地悪されています。人間、対応せよ", mention_author=False
                )
                exit(1)
        except ValueError:
            await message.add_reaction("❌")
        except Exception:
            await message.reply(
                "謎のエラーが発生しました。人間、対応せよ", mention_author=False
            )
            exit(1)


client.run(TOKEN)
