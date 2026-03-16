
import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image

# הגדרת כותרת ועיצוב דף
st.set_page_config(page_title="סורק הבריאות שלי", page_icon="🍎")
st.title("סורק סוכר ומלח חכם 🚀")

# פונקציה לשליפת נתונים ממאגר Open Food Facts
def get_nutrition_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                product = data.get("product", {})
                name = product.get("product_name", "מוצר ללא שם")
                nutriments = product.get("nutriments", {})
                sugar = nutriments.get("sugars_100g", "לא צוין")
                salt = nutriments.get("salt_100g", "לא צוין")
                return name, sugar, salt
    except Exception as e:
        st.error(f"שגיאה בחיבור למאגר: {e}")
    return None, None, None

# יצירת טאבים לממשק נוח
tab1, tab2 = st.tabs(["📸 סריקה במצלמה", "⌨️ הקלדה ידנית"])

with tab1:
    st.subheader("סרוק ברקוד מהאריזה")
    img_file = st.camera_input("צלם את הברקוד בצורה ברורה")
   
    if img_file:
        # עיבוד התמונה לזיהוי ברקוד
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        opencv_img = cv2.imdecode(file_bytes, 1)
       
        # שימוש ב-OpenCV לזיהוי הברקוד
        detector = cv2.barcode.BarcodeDetector()
        retval, decoded_info, decoded_type, points = detector.detectAndDecode(opencv_img)
       
        if retval:
            barcode = decoded_info[0]
            st.success(f"ברקוד זוהה: {barcode}")
            name, sugar, salt = get_nutrition_data(barcode)
            if name:
                st.info(f"מוצר: {name}")
                st.metric("סוכר (ל-100 גרם)", f"{sugar} גרם")
                st.metric("מלח (ל-100 גרם)", f"{salt} גרם")
        else:
            st.warning("לא הצלחתי לזהות ברקוד בתמונה. נסה לקרב את המצלמה או להזין ידנית.")

with tab2:
    st.subheader("הזנת ברקוד באופן ידני")
    manual_code = st.text_input("הכנס את המספר שמתחת לברקוד:")
    if st.button("בדוק מוצר"):
        name, sugar, salt = get_nutrition_data(manual_code)
        if name:
            st.success(f"נמצא מוצר: {name}")
            col1, col2 = st.columns(2)
            col1.metric("סוכר", f"{sugar} גרם")
            col2.metric("מלח", f"{salt} גרם")
        else:
            st.error("הברקוד לא נמצא במאגר. נסה ברקוד אחר.") 
