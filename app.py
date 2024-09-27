import streamlit as st
from PIL import Image
import io
import time

def compress_image(image, compression_rate):
    img = Image.open(image)
    
    if compression_rate == "원본":
        return img
    elif compression_rate == "낮음":
        quality = 85
    elif compression_rate == "보통":
        quality = 60
    else:  # 높음
        quality = 35
    
    output = io.BytesIO()
    img.save(output, format=img.format, quality=quality, optimize=True)
    output.seek(0)
    
    return Image.open(output)

def main():
    st.title("이미지 압축기")
    
    uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        compression_rate = st.select_slider(
            "압축률 선택",
            options=["원본", "낮음", "보통", "높음"],
            value="원본"
        )
        
        # 이미지를 표시할 placeholder 생성
        image_placeholder = st.empty()
        
        # 로딩 스피너와 함께 이미지 압축 및 표시
        with st.spinner('이미지 처리 중...'):
            # 이미지 위에 로딩 중 표시를 위한 overlay
            overlay_placeholder = st.empty()
            
            # 이미지 압축 및 표시
            compressed_image = compress_image(uploaded_file, compression_rate)
            image_placeholder.image(compressed_image, use_column_width=True)
            
            # 잠시 로딩 표시를 위해 지연
            time.sleep(0.5)
            
        # 로딩 완료 후 overlay 제거
        overlay_placeholder.empty()
        
        # 압축된 이미지를 바이트로 변환
        img_byte_arr = io.BytesIO()
        compressed_image.save(img_byte_arr, format=compressed_image.format)
        img_byte_arr = img_byte_arr.getvalue()
        
        # 다운로드 버튼
        st.download_button(
            label="압축된 이미지 다운로드",
            data=img_byte_arr,
            file_name=f"compressed_{uploaded_file.name}",
            mime=f"image/{compressed_image.format.lower()}"
        )
        
        # 원본과 압축 후 파일 크기 비교
        original_size = uploaded_file.size
        compressed_size = len(img_byte_arr)
        st.write(f"원본 크기: {original_size / 1024:.2f} KB")
        st.write(f"압축 후 크기: {compressed_size / 1024:.2f} KB")
        st.write(f"압축률: {(1 - compressed_size / original_size) * 100:.2f}%")

if __name__ == "__main__":
    main()
