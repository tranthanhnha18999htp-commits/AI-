"""
MẪU AI ĐƠN GIẢN: TRỢ LÝ TƯ VẤN QUÁN CÀ PHÊ MỘC
Chạy được cả trên máy tính cá nhân và online trên GitHub / Codespaces.
"""
MODEL_NAME = "moc_ai"
import os
from google import genai

# ==============================================================================
# PHẦN 1: BỘ NÃO AI (API KEY)
# Tự động đọc từ biến môi trường GEMINI_API_KEY (khi chạy online/Codespaces).
# Nếu không tìm thấy, chương trình sẽ hỏi bạn nhập trực tiếp trên màn hình.
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY or API_KEY == "DAN_API_KEY_CUA_BAN_VAO_DAY":
    print("=" * 55)
    print("CHƯA TÌM THẤY GEMINI_API_KEY TỰ ĐỘNG.")
    API_KEY = input("Vui lòng dán API Key của bạn vào đây và nhấn Enter: ").strip()
    print("=" * 55 + "\n")

# Khởi tạo kết nối với bộ não Gemini
client = genai.Client(api_key=API_KEY)


# ==============================================================================
# PHẦN 2: DỮ LIỆU CỦA BẠN (ĐỌC TỪ FILE TAILIEU.TXT)
# Tự động mở file tailieu.txt để đọc kiến thức riêng bạn đã chuẩn bị.
# ==============================================================================
file_tai_lieu = "tailieu.txt"

if os.path.exists(file_tai_lieu):
    with open(file_tai_lieu, "r", encoding="utf-8") as f:
        thong_tin_quan = f.read()
    print(f"[Hệ thống]: Đã nạp thành công dữ liệu từ file '{file_tai_lieu}'!\n")
else:
    # Dữ liệu dự phòng nếu chưa có file tailieu.txt
    thong_tin_quan = """
Tên quán: Cà Phê Mộc
Địa chỉ: 123 Đường Hoa Hồng, Quận 1, TP.HCM
Giờ mở cửa: 07:00 - 22:30 hàng ngày
Menu đặc biệt: Cà phê Muối (35k), Trà Đào Cam Sả (40k), Bạc xỉu (32k).
Chính sách: Miễn phí giữ xe, wifi tốc độ cao (pass: caphemoc2026), không bán đồ ăn mặn.
"""
    print(f"[Lưu ý]: Chưa thấy file '{file_tai_lieu}', đang dùng dữ liệu dự phòng.\n")


# ==============================================================================
# PHẦN 3: VÒNG LẶP HỎI - ĐÁP
# ==============================================================================
def main():
    print("=" * 55)
    print("Chào bạn! Tôi là AI tư vấn của Quán Cà Phê Mộc.")
    print("Tôi đã học xong dữ liệu từ file tailieu.txt.")
    print("Bạn có thể hỏi tôi bất kỳ thông tin nào về quán.")
    print("Gõ 'tam biet' hoặc 'exit' để dừng chương trình.")
    print("=" * 55 + "\n")

    while True:
        cau_hoi = input("Bạn hỏi: ").strip()

        if cau_hoi.lower() in ["exit", "tam biet", "quit"]:
            print("\nCảm ơn bạn đã ghé thăm Quán Cà Phê Mộc. Hẹn gặp lại!")
            break

        if not cau_hoi:
            continue

        # Ghép tài liệu vào prompt gửi cho AI
        loi_dan = f"""Bạn là nhân viên tư vấn vui vẻ, thân thiện của Quán Cà Phê Mộc.
Hãy sử dụng thông tin được cung cấp dưới đây để trả lời câu hỏi của khách hàng:

--- THÔNG TIN QUÁN ---
{thong_tin_quan}
---------------------

Quy tắc bắt buộc:
1. Chỉ trả lời dựa trên thông tin đã cung cấp ở trên.
2. Nếu khách hỏi thông tin không có trong tài liệu (ví dụ: quán có bán bún bò, pizza không), hãy lịch sự nói rằng quán chưa phục vụ món đó.
3. Trả lời ngắn gọn, tự nhiên và thân thiện.

Khách hàng hỏi: {cau_hoi}
"""

        try:
            phan_hoi = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=loi_dan,
            )
            print(f"\nAI Mộc: {phan_hoi.text}\n")
            print("-" * 55)

        except Exception as e:
            print(f"\n[Lỗi kết nối]: {e}")
            print("Mẹo: Hãy kiểm tra lại API Key hoặc đường truyền mạng nhé!\n")


if __name__ == "__main__":
    main()