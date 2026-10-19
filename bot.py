import os
from google import genai

# Đọc tự động từ biến môi trường của máy tính
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
