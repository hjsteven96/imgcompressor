import streamlit as st
from PIL import Image
import io
import base64

def compress_image(image, compression_rate):
    img = Image.open(image)
    
    # 압축률에 따른 품질 설정
    if compression_rate == "낮음":
        quality = 85
    elif compression_rate == "보통":
        quality = 60
    else:  # 높음
        quality = 35
    
    # 이미지 압축
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    compressed_image = output.getvalue()
    
    return compressed_image

def get_image_download_link(img, filename, text):
    b64 = base64.b64encode(img).decode()
    href = f'<a href="data:image/jpeg;base64,{b64}" download="{filename}">다운로드 {text}</a>'
    return href

def main():
    st.title("이미지 압축기")
    
    uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "jpeg", "png", "gif"])
    compression_rate = st.select_slider("압축률 선택", options=["낮음", "보통", "높음"], value="보통")
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="원본 이미지", use_column_width=True)
        
        if st.button("압축하기"):
            compressed_image = compress_image(uploaded_file, compression_rate)
            st.image(compressed_image, caption="압축된 이미지", use_column_width=True)
            
            # 압축된 이미지 다운로드 링크 제공
            st.markdown(get_image_download_link(compressed_image, "compressed_image.jpg", "압축된 이미지"), unsafe_allow_html=True)
            
            # 원본과 압축 후 파일 크기 비교
            original_size = uploaded_file.size
            compressed_size = len(compressed_image)
            st.write(f"원본 크기: {original_size / 1024:.2f} KB")
            st.write(f"압축 후 크기: {compressed_size / 1024:.2f} KB")
            st.write(f"압축률: {(1 - compressed_size / original_size) * 100:.2f}%")

if __name__ == "__main__":
    main()
