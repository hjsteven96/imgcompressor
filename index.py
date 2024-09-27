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

def main():
    st.set_page_config(layout="wide")
    st.title("이미지 압축기")

    uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])

        with col1:
            image_placeholder = st.empty()
            original_image = Image.open(uploaded_file)
            image_placeholder.image(original_image, use_column_width=True)

        with col2:
            st.subheader("압축 설정")
            quality = st.slider("품질", 0, 100, 76, 1, format="%d%%")
            
            zoom = st.slider("확대/축소", 0.5, 2.0, 1.0, 0.1)

            if st.button("압축 적용"):
                with st.spinner('이미지 압축 중...'):
                    compressed_image = compress_image(uploaded_file, quality)
                    
                    # 원본과 압축 후 파일 크기 비교
                    original_size = uploaded_file.size
                    compressed_byte_arr = io.BytesIO()
                    compressed_image.save(compressed_byte_arr, format=compressed_image.format)
                    compressed_size = len(compressed_byte_arr.getvalue())

                    # 이미지 확대/축소 적용
                    width, height = compressed_image.size
                    new_size = (int(width * zoom), int(height * zoom))
                    resized_image = compressed_image.resize(new_size, Image.LANCZOS)

                    image_placeholder.image(resized_image, use_column_width=True)

                st.success('압축 완료!')

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
