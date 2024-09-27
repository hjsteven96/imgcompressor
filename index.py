import streamlit as st
from PIL import Image
import io
import time

def compress_image(image, quality):
    img = Image.open(image)
    output = io.BytesIO()
    img.save(output, format=img.format, quality=quality, optimize=True)
    output.seek(0)
    return Image.open(output)

def resize_image(image, scale_factor=0.5):
    width, height = image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return image.resize(new_size, Image.LANCZOS)

def main():
    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .title {
            text-align: center;
        }
        .stApp {
            position: relative;
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>이미지 압축기</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col_image, col_control = st.columns([2, 1])

        with col_image:
            image_placeholder = st.empty()
            overlay_placeholder = st.empty()
            original_image = Image.open(uploaded_file)
            preview_image = resize_image(original_image)
            image_placeholder.image(preview_image, use_column_width=True, caption="이미지 미리보기 (50% 크기)")

        with col_control:
            st.subheader("압축 설정")
            quality = st.slider("품질", 0, 100, 76, 1, format="%d%%")
            
            # 압축 실행 및 결과 표시
            overlay_placeholder.markdown(
                """
                <div class="overlay">
                    <div class="spinner"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            compressed_image = compress_image(uploaded_file, quality)
            
            # 원본과 압축 후 파일 크기 비교
            original_size = uploaded_file.size
            compressed_byte_arr = io.BytesIO()
            compressed_image.save(compressed_byte_arr, format=compressed_image.format)
            compressed_size = len(compressed_byte_arr.getvalue())

            # 압축된 이미지 미리보기 (50% 크기)
            preview_compressed = resize_image(compressed_image)
            image_placeholder.image(preview_compressed, use_column_width=True, caption="압축된 이미지 미리보기 (50% 크기)")

            # 오버레이 제거
            overlay_placeholder.empty()

            st.write(f"원래 크기: {original_size / 1024:.2f} KB")
            st.write(f"압축 크기: {compressed_size / 1024:.2f} KB")
            st.write(f"압축률: {(1 - compressed_size / original_size) * 100:.2f}%")

            # 다운로드 버튼
            st.download_button(
                label="압축된 이미지 다운로드",
                data=compressed_byte_arr.getvalue(),
                file_name=f"compressed_{uploaded_file.name}",
                mime=f"image/{compressed_image.format.lower()}"
            )

if __name__ == "__main__":
    main()
