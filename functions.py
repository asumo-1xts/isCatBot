import mimetypes
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_CANDIDATES = (
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
)


# 猫判定関数
def is_cat(image_path: str) -> int:
    # 画像のMIMEタイプを判定
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        raise ValueError(f"未対応の画像形式です: {mime_type}")

    # 画像を読み込む
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Geminiに投げる
    prompt = "この画像に猫は写っていますか？YESまたはNOの1語だけで答えてください。"

    for model in MODEL_CANDIDATES:
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_data, mime_type=mime_type),
                ],
            )
            output_text = (response.text or "").strip().upper()
            print(f"[{model}] {output_text}")
            return 1 if "YES" in output_text else 0
        except Exception:
            continue  # ダメなら別のモデルで再試行

    return 2  # すべてのモデルで失敗
