import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image

st.title("סורק סוכר ומלח חכם 🚀")

def get_nutrition_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data.get("product", {})
            name = product.get("product_name", "מוצר ללא שם")
            nutrients = product.get("nutriments", {})
            sugar = nutrients.get("sugars_100g", "לא ידוע")
            salt = nutrients.get("salt_100g", "לא ידוע")
            return name, sugar, salt
    return None, None, None

img_file = st.camera_input("צלם ברקוד של מוצר")

if img_file:
    # המרת התמונה לפורמט ש-OpenCV מבין
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    opencv_img = cv2.imdecode(file_bytes, 1)
   
    # זיהוי ברקוד
    detector = cv2.barcode.BarcodeDetector()
    retval, decoded_info, decoded_type, points = detector.detectAndDecode(opencv_img)
   
    if retval:
        barcode_value = decoded_info[0]
        st.success(f"ברקוד זוהה: {barcode_value}")
        name, sugar, salt = get_nutrition_info(barcode_value)
        if name:
            st.subheader(f"תוצאות עבור: {name}")
            st.metric("סוכר (ל-100 גרם)", f"{sugar} גרם")
            st.metric("מלח (ל-100 גרם)", f"{salt} גרם")
    else:
        st.warning("לא נמצא ברקוד בתמונה. נסה להחזיק את המוצר יציב יותר.")

st.write("---")
manual_barcode = st.text_input("הכנס ברקוד ידנית לגיבוי:")
if st.button("בדוק"):
    name, sugar, salt = get_nutrition_info(manual_barcode)
    if name:
        st.write(f"מוצר: {name} | סוכר: {sugar} | מלח: {salt}") 
