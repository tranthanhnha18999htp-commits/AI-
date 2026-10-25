import streamlit as st
import ollama

# 1. Cấu hình tiêu đề trang web
st.set_page_config(page_title="AI Tư Vấn Mộc", page_icon="☕")
st.title("☕ AI Tư Vấn - Quán Cà Phê Mộc")

# 2. Khởi tạo bộ nhớ lưu trữ lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Dạ em chào anh/chị ạ! Em là Trợ lý Mộc Nhi của Quán Cà Phê Mộc ☕✨. Anh/chị cần hỏi gì cứ nhắn em nhé!"}
    ]

# 3. Vẽ lại toàn bộ các tin nhắn cũ lên màn hình
for msg in st.session_state.messages:
    avatar = "☕" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 4. Nhận tin nhắn mới từ người dùng
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Lưu và hiển thị câu hỏi của khách
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 5. GỬI CÂU HỎI VÀO NÃO BỘ OLLAMA (Dòng tích hợp cốt lõi)
    try:
        with st.chat_message("assistant", avatar="☕"):
            with st.spinner("AI Mộc đang soạn câu trả lời..."):
                response = ollama.chat(
                    model="moc_ai:lastest",  # Điền đúng tên mô hình bạn đã đúc
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response["message"]["content"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Lỗi kết nối Ollama: {e}")