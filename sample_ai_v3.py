import os
import tempfile
import requests
import streamlit as st
import speech_recognition as sr

# --- Cấu hình trang Streamlit ---
st.set_page_config(
    page_title="Trợ lý AI - Codespaces",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Trợ lý AI: Lắng nghe, Phân tích & Trò chuyện")
st.caption("Phiên bản tối ưu cho GitHub Codespaces & Ollama")

# --- Sidebar: Kiểm tra kết nối Ollama ---
st.sidebar.header("⚙️ Cấu hình Ollama")
ollama_url = st.sidebar.text_input("URL Ollama API", "http://localhost:11434")
ollama_model = st.sidebar.selectbox(
    "Mô hình (Model)",
    ["llama3", "qwen2.5", "moc_ai", "gemma"],
    index=0
)

# Nút kiểm tra kết nối Ollama trực tiếp
if st.sidebar.button("🔌 Kiểm tra kết nối Ollama"):
    try:
        r = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if r.status_code == 200:
            models = [m['name'] for m in r.json().get('models', [])]
            st.sidebar.success(f"Kết nối thành công! Model hiện có: {', '.join(models) if models else 'Chưa pull model nào'}")
        else:
            st.sidebar.error("Ollama đang chạy nhưng gặp lỗi kết nối.")
    except Exception as e:
        st.sidebar.error(f"Chưa bật `ollama serve` hoặc sai URL ({e})")

# Nút xóa lịch sử chat
if st.sidebar.button("🗑️ Xóa lịch sử Chat"):
    st.session_state.messages = []
    st.rerun()

# Khởi tạo lịch sử chat trong session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Giao diện Tabs ---
tab_listen, tab_chat = st.tabs(["🎙️ Lắng nghe & Phân tích", "💬 Trò chuyện (Chat)"])

# ==========================================
# TAB 1: LẮNG NGHE & TỔNG KẾT
# ==========================================
with tab_listen:
    st.subheader("1. Đầu vào thông tin")
    
    # Cho phép chọn phương thức nhập để tránh bị kẹt nếu micro bị trình duyệt chặn
    input_method = st.radio(
        "Chọn phương thức nhập:", 
        ["🎙️ Ghi âm từ Micro", "✏️ Nhập văn bản trực tiếp"], 
        horizontal=True
    )
    
    transcribed_text = ""

    if input_method == "🎙️ Ghi âm từ Micro":
        audio_file = st.audio_input("Nhấn vào biểu tượng micro để ghi âm:")
        if audio_file:
            st.audio(audio_file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_file.getbuffer())
                tmp_audio_path = tmp_file.name

            with st.spinner("Đang chuyển âm thanh thành văn bản..."):
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(tmp_audio_path) as source:
                        audio_data = recognizer.record(source)
                        transcribed_text = recognizer.recognize_google(audio_data, language="vi-VN")
                        st.success("Đã nhận diện xong giọng nói!")
                except sr.UnknownValueError:
                    st.warning("Không nghe rõ giọng nói. Bạn hãy thử nói to rõ hơn hoặc dùng ô nhập văn bản.")
                except Exception as e:
                    st.error(f"Lỗi đọc file âm thanh: {e}")
                finally:
                    if os.path.exists(tmp_audio_path):
                        os.remove(tmp_audio_path)
    else:
        transcribed_text = st.text_area("Nhập hoặc dán nội dung bạn muốn AI phân tích:", height=150)

    # Nếu có nội dung văn bản -> Phân tích bằng Ollama
    if transcribed_text:
        st.info(f"**Nội dung nhận diện được:** {transcribed_text}")
        
        if st.button("🚀 Bắt đầu Phân tích & Tổng kết", type="primary"):
            prompt_analysis = f"""
Bạn là chuyên viên lắng nghe và phân tích nhu cầu. 
Dưới đây là nội dung chia sẻ từ người dùng:

\"\"\"{transcribed_text}\"\"\"

Hãy phân tích và trả lời bằng tiếng Việt theo định dạng Markdown:
### 🎯 Chủ đề chính
(Tóm tắt ngắn gọn 1-2 câu)

### 🔍 Các vấn đề / trăn trở cốt lõi
- (Liệt kê các điểm chính)

### 💡 Hướng xử lý / Hành động tiếp theo
- (2-3 gợi ý hành động thiết thực)
"""
            with st.spinner(f"Đang gửi sang Ollama model '{ollama_model}'..."):
                try:
                    res = requests.post(
                        f"{ollama_url}/api/generate",
                        json={"model": ollama_model, "prompt": prompt_analysis, "stream": False},
                        timeout=90
                    )
                    if res.status_code == 200:
                        st.markdown("### 📊 Kết quả Phân tích Trọng tâm")
                        st.markdown(res.json().get("response", ""))
                    else:
                        st.error(f"Lỗi từ Ollama API (Code: {res.status_code}). Đảm bảo bạn đã tải model bằng lệnh: `ollama pull {ollama_model}`")
                except Exception as e:
                    st.error(f"Không thể kết nối Ollama tại {ollama_url}. Bạn hãy kiểm tra xem `ollama serve` đã chạy trong Terminal chưa.")

# ==========================================
# TAB 2: TRÒ CHUYỆN (CHATBOT)
# ==========================================
with tab_chat:
    st.subheader("💬 Trò chuyện trực tiếp")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Nhập tin nhắn của bạn..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI đang suy nghĩ..."):
                try:
                    payload = {
                        "model": ollama_model,
                        "messages": st.session_state.messages,
                        "stream": False
                    }
                    res = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=90)
                    if res.status_code == 200:
                        ai_response = res.json().get("message", {}).get("content", "")
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        st.error(f"Lỗi Ollama Chat (Code: {res.status_code}). Kiểm tra xem model '{ollama_model}' đã được tải về chưa.")
                except Exception as e:
                    st.error(f"Lỗi kết nối Ollama: {e}")