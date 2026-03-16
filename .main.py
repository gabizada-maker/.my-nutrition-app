import streamlit as st
import requests

# כותרת האפליקציה
st.title("מדד סוכר ומלח יומי 🥗")
st.write("עקוב אחר התזונה שלך בקלות")

# יצירת זיכרון למשתמש
if 'totals' not in st.session_state:
    st.session_state.totals = {"sugar": 0.0, "salt": 0.0}

# פונקציה לשליפת נתונים ממאגר הברקודים
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

# ממשק קלט
barcode = st.text_input("הזן מספר ברקוד:")
weight = st.number_input("כמה גרם אכלת?", min_value=1, value=100)

if st.button("הוסף ליומן"):
    product = get_data(barcode)
    if product:
        s = (weight / 100) * product['sugar']
        n = (weight / 100) * product['salt']
        st.session_state.totals['sugar'] += s
        st.session_state.totals['salt'] += n
        st.success(f"הוספת: {product['name']}")
    else:
        st.error("הברקוד לא נמצא")

# תצוגת נתונים
st.divider()
st.metric("סך סוכר (גרם) 🍭", round(st.session_state.totals['sugar'], 2))
st.metric("סך מלח (גרם) 🧂", round(st.session_state.totals['salt'], 2))

if st.button("איפוס"):
    st.session_state.totals = {"sugar": 0.0, "salt": 0.0}
    st.rerun()
