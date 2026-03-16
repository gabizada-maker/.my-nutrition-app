import streamlit as st
import requests

# כותרת האפליקציה
st.title("סורק תזונה חכם 🥗")

# אתחול המונים בזיכרון
if 'totals' not in st.session_state:
    st.session_state.totals = {"sugar": 0.0, "salt": 0.0}

# פונקציה לשליפת נתונים לפי ברקוד
def get_data(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        res = requests.get(url).json()
        if res.get('status') == 1:
            p = res['product']
            nutr = p.get('nutriments', {})
            return {
                "name": p.get('product_name', 'מוצר לא ידוע'),
                "sugar": nutr.get('sugars_100g', 0),
                "salt": nutr.get('salt_100g', 0)
            }
    except:
        return None
    return None

# --- ממשק המצלמה ---
st.subheader("סריקה מהירה 📸")
picture = st.camera_input("צלם את הברקוד מהאריזה")

# --- הזנה ידנית ---
st.divider()
barcode_input = st.text_input("הזן ברקוד ידנית (אם הצילום לא עובד):")
weight = st.number_input("כמות בגרמים שצרכת:", min_value=1, value=100)

if st.button("חשב והוסף ליומן"):
    # כאן נשתמש בברקוד שהוזן
    product = get_data(barcode_input)
    if product:
        s = (weight / 100) * product['sugar']
        n = (weight / 100) * product['salt']
        st.session_state.totals['sugar'] += s
        st.session_state.totals['salt'] += n
        st.success(f"הוספת: {product['name']}")
    else:
        st.error("הברקוד לא נמצא במאגר")

# הצגת נתונים מצטברים
st.sidebar.header("סיכום יומי")
st.sidebar.metric("סך סוכר (גרם) 🍭", round(st.session_state.totals['sugar'], 2))
st.sidebar.metric("סך מלח (גרם) 🧂", round(st.session_state.totals['salt'], 2))

