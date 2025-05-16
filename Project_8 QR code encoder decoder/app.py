# Streamlit library import for web interface
import streamlit as st

# QR code generate karne ke liye library
import qrcode

# Image handling ke liye (QR image open ya save karne ke liye)
from PIL import Image   

# QR code decode karne ke liye OpenCV library
import cv2

# Image data ko numpy array mein convert karne ke liye
import numpy as np

# BytesIO object banane ke liye (image ko memory mein temporarily rakhne ke liye)
import io


# Web page ka title or layout set kar rahe hain
st.set_page_config(page_title="QR Code Encoder & Decoder", layout="centered")

# Page ki heading
st.title("🔳 QR Code Encoder / Decoder")

# User se option choose karwa rahe hain (encode ya decode)
option = st.radio("Select Operation", ["Encode QR Code", "Decode QR Code"])

# ------------------------------ ENCODER SECTION ------------------------------
if option == "Encode QR Code":
    # User se text ya URL input le rahe hain
    text = st.text_input("Enter text or URL to generate QR Code:")

    # Jab button click ho aur input khaali na ho
    if st.button("Generate QR Code") and text:
        # QR code banane ke liye qrcode object banaya hai
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)              # Input data add kiya
        qr.make(fit=True)              # QR ko size fit karne diya
        img = qr.make_image(fill="black", back_color="white").convert("RGB")  # QR image banai

        # Image ko bytes mein convert kiya display aur download ke liye
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Streamlit par image dikhayi
        st.image(img_bytes, caption="QR Code", use_container_width=True)

        # Download button diya QR code image download karne ke liye
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name="qrcode.png",
            mime="image/png"
        )

# ------------------------------ DECODER SECTION ------------------------------
elif option == "Decode QR Code":
    # User se QR code image upload karwane ke liye file uploader
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

    # Agar koi file upload hui ho
    if uploaded_file:
        # File ko bytes mein read karke numpy array banaya
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        # OpenCV se image decode ki
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Uploaded image ko Streamlit par dikhaya
        st.image(img, caption="Uploaded QR Code", use_container_width=True)

        # QR detector banaya OpenCV ka
        qr_detector = cv2.QRCodeDetector()
        # Try kiya pehle normally detect aur decode karna
        data, bbox, _ = qr_detector.detectAndDecode(img)

        # Agar pehle try mein data na mile to grayscale mein convert karke dobara try kiya
        if not data:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            data, bbox, _ = qr_detector.detectAndDecode(gray)

        # Agar data mil gaya ho to:
        if data:
            # Decoded text dikhaya
            st.success("🔓 Decoded Data:")
            st.code(data)

            # Decoded data se wapas QR code generate kiya
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill="black", back_color="white").convert("RGB")

            # Image ko bytes mein convert kiya display aur download ke liye
            qr_bytes = io.BytesIO()
            qr_img.save(qr_bytes, format="PNG")
            qr_bytes.seek(0)

            # Regenerated QR code image show ki
            st.image(qr_bytes, caption="Re-generated QR Code", use_container_width=True)

            # Download button diya QR code ko save karne ke liye
            st.download_button(
                label="Download QR Code",
                data=qr_bytes,
                file_name="decoded_qrcode.png",
                mime="image/png"
            )
        else:
            # Agar QR code detect nahi hua to error show kiya
            st.error("❌ QR Code not detected or could not be decoded.")

# ------------------------------ FOOTER ------------------------------
# Neeche ek simple HTML footer diya gaya hai credit dene ke liye
st.markdown(
    """
    ---
    <footer style='text-align: center;'>
        <p>Created with ❤️ by <a href="https://github.com/NabiaHaider" target="_blank">Nabia Haider</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)
