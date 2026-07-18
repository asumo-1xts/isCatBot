import mimetypes
import os
from dotenv import load_dotenv
from enum import Enum
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_CANDIDATES = (
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
)


# Geminiの返答の型を定義
class IsCat(str, Enum):
    YES = "YES"
    NO = "NO"


# 猫判定関数
def is_cat(image_path: str) -> int:
    # 画像のMIMEタイプを判定
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None or mime_type not in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        raise ValueError(f"未対応の画像形式です: {mime_type}")

    # 画像を読み込む
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Geminiに投げる
    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    "この画像に猫は写っていますか？",
                    types.Part.from_bytes(data=image_data, mime_type=mime_type),
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="text/x.enum",
                    response_schema=IsCat,
                ),
            )
            answer = IsCat(response.text.strip())
            print(f"[{model}] {answer}")
            return 1 if answer is IsCat.YES else 0
        except Exception:
            continue  # ダメなら別のモデルで再試行

    return 2  # すべてのモデルで失敗
