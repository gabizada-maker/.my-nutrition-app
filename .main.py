 import streamlit as st
import requests
from PIL import Image
from pyzbar.pyzbar import decode

st.title("סורק סוכר ומלח חכם 🚀")

# פונקציה לשליפת נתונים מהמאגר
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

# אפשרות 1: צילום תמונה
img_file = st.camera_input("צלם ברקוד של מוצר")

if img_file:
    # פתיחת התמונה ופענוח הברקוד
    img = Image.open(img_file)
    barcodes = decode(img)
   
    if barcodes:
        barcode_value = barcodes[0].data.decode('utf-8')
        st.success(f"ברקוד זוהה: {barcode_value}")
       
        name, sugar, salt = get_nutrition_info(barcode_value)
        if name:
            st.subheader(f"תוצאות עבור: {name}")
            st.metric("סוכר (ל-100 גרם)", f"{sugar} גרם")
            st.metric("מלח (ל-100 גרם)", f"{salt} גרם")
        else:
            st.warning("הברקוד זוהה, אך המוצר לא נמצא במאגר.")
    else:
        st.error("לא הצלחתי למצוא ברקוד בתמונה. נסה לצלם מקרוב וברור יותר.")

# אפשרות 2: הזנה ידנית (גיבוי)
st.write("---")
manual_barcode = st.text_input("או הכנס ברקוד ידנית:")
if st.button("בדוק ברקוד ידני"):
    name, sugar, salt = get_nutrition_info(manual_barcode)
    if name:
        st.subheader(f"תוצאות עבור: {name}")
        st.write(f"**סוכר:** {sugar} גרם | **מלח:** {salt} גרם")
    else:
        st.error("מוצר לא נמצא.") 

