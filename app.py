import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import random

# 🎨 छत्तीसगढ़ भूलेख एवं क्लाउड प्रीमियम थीम
st.set_page_config(page_title="मां प्रॉपर्टी - क्लाउड संस्करण", layout="wide", initial_sidebar_state="collapsed")

st.markdown("<h2 style='text-align: center; color: #15803D; margin-top: 10px;'>🔱 मां प्रॉपर्टी (Maa Property)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1E3A8A; font-size:14px;'>🌐 100% सुरक्षित लाइव क्लाउड बहीखाता संस्करण</p>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# ☁️ क्लाउड डेटाबेस कनेक्शन (Google Sheets से सिंक)
# ==========================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    inv_df = conn.read(worksheet="Inventory", ttl="0")
    khata_df = conn.read(worksheet="KhataBook", ttl="0")
    settings_df = conn.read(worksheet="Settings", ttl="0")
except:
    inv_df = pd.DataFrame(columns=['prop_id', 'seller_name', 'state', 'district', 'tehsil', 'patwari_halka', 'village', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'date_added'])
    khata_df = pd.DataFrame(columns=['tx_date', 'party_type', 'party_name', 'party_phone', 'prop_id', 'deal_amount', 'amount_paid_received', 'balance_amount', 'payment_mode', 'notes'])
    settings_df = pd.DataFrame([{"key": "username", "value": "admin"}, {"key": "password", "value": "Radhe@2026"}, {"key": "phone", "value": "9876543210"}])

def get_setting(key_name):
    try:
        val = settings_df[settings_df['key'] == key_name]['value'].values[0]
        return str(val)
    except:
        if key_name == "password": return "Radhe@2026"
        if key_name == "username": return "admin"
        return "9876543210"

# 🌾 छत्तीसगढ़ भुइयां लिंक्ड मास्टर डेटा (मुंगेली/बिलासपुर विशेष)
BHUIYAN_DATA = {
    "छत्तीसगढ़ (Chhattisgarh)": {
        "मुंगेली (Mungeli)": {
            "मुंगेली": {
                "हल्का नंबर 01": ["रामपुर", "मोहनपुर", "तखतपुर रोड"],
                "हल्का नंबर 02": ["दुर्गापुर", "चन्दनपुर", "दाऊपारा"]
            },
            "लॉर्मी (Lormi)": {
                "हल्का नंबर 03": ["शिवपुर", "गणेशपुर", "खुड़िया"],
                "हल्का नंबर 04": ["नवागाँव", "बकेला", "डिंडौरी"]
            }
        },
        "बिलासपुर (Bilaspur)": {
            "बिलासपुर (Sadar)": {
                "हल्का नंबर 07": ["तिफरा", "सिरगिट्टी"],
                "हल्का नंबर 08": ["सकर्री", "कचहरी चौक"]
            }
        }
    }
}

# ==========================================
# 🔒 मोबाइल ओटीपी क्लाउड सुरक्षा लॉगिन
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>🔒 क्लाउड एडमिन लॉगिन</h4>", unsafe_allow_html=True)
        if not st.session_state.otp_sent:
            with st.form("login_step1"):
                u = st.text_input("यूज़रनेम (Username)")
                p = st.text_input("पासवर्ड (Password)", type="password")
                if st.form_submit_button("🔑 स्टेप 1: ओटीपी कोड प्राप्त करें"):
                    if u == get_setting('username') and p == get_setting('password'):
                        st.session_state.otp_sent = True
                        st.session_state.generated_otp = str(random.randint(100000, 999999))
                        st.rerun()
                    else:
                        st.error("❌ गलत यूज़रनेम या पासवर्ड!")
        else:
            with st.form("login_step2"):
                st.warning(f"🔒 सुरक्षा कोड (ओटीपी अलर्ट): 👉 {st.session_state.generated_otp} 👈")
                entered_otp = st.text_input("6-अंकों का मोबाइल OTP दर्ज करें", type="password")
                if st.form_submit_button("🔓 क्लाउड ऐप अनलॉक करें"):
                    if entered_otp == st.session_state.generated_otp:
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌ गलत ओटीपी कोड!")

# ==========================================
# 🏢 मुख्य मोबाइल क्लाउड इंटरफ़ेस (Tabs Layout)
# ==========================================
else:
    menu = st.tabs([
        "📊 लाइव रिपोर्ट", 
        "🌾 ज़मीन खरीद (विक्रेता)", 
        "💸 प्लॉट बिक्री (क्रेता)",
        "📂 स्टॉक बही", 
        "🧾 डिजिटल खता"
    ])

    # 1. डैशबोर्ड
    with menu[0]:
        v_df = khata_df[khata_df['party_type'] == 'विक्रेता (किसान)'] if not khata_df.empty else pd.DataFrame(columns=['balance_amount'])
        k_df = khata_df[khata_df['party_type'] == 'क्रेता (ग्राहक)'] if not khata_df.empty else pd.DataFrame(columns=['balance_amount', 'amount_paid_received'])

        st.metric("🌾 किसानों को देय बकाया", f"₹{pd.to_numeric(v_df['balance_amount'], errors='coerce').sum():,.2f}")
        st.metric("💵 ग्राहकों से कुल आवक (नकद)", f"₹{pd.to_numeric(k_df['amount_paid_received'], errors='coerce').sum():,.2f}")
        st.metric("🔴 ग्राहकों से लेना बकाया (मार्केट उधारी)", f"₹{pd.to_numeric(k_df['balance_amount'], errors='coerce').sum():,.2f}")
        st.metric("🏡 लाइव उपलब्ध खसरा स्टॉक संख्या", len(inv_df))
        st.write("---")
        st.link_button("🌐 छत्तीसगढ़ भुइयां सरकारी पोर्टल लिंक", "https://bhuiyan.cg.nic.in/")

    # 2. ज़मीन एंट्री (विक्रेता खता)
    with menu[1]:
        st.subheader("🌾 भुइयां खसरा एवं किसान खता एंट्री")
        with st.form("bhulekh_form", clear_on_submit=True):
            selected_state = st.selectbox("राज्य चुनें", list(BHUIYAN_DATA.keys()))
            districts = list(BHUIYAN_DATA[selected_state].keys())
            selected_district = st.selectbox("जिला चुनें", districts)
            tehsils = list(BHUIYAN_DATA[selected_state][selected_district].keys())
            selected_tehsil = st.selectbox("तहसील चुनें", tehsils)
            halkas = list(BHUIYAN_DATA[selected_state][selected_district][selected_tehsil].keys())
            selected_halka = st.selectbox("पटवारी हल्का चुनें", halkas)
            villages = BHUIYAN_DATA[selected_state][selected_district][selected_tehsil][selected_halka]
            selected_village = st.selectbox("ग्राम चुनें", villages)
            
            st.write("---")
            seller_name = st.text_input("👤 किसान (विक्रेता) का पूरा नाम")
            seller_phone = st.text_input("📱 किसान का मोबाइल")
            prop_id = st.text_input("📦 खसरा नंबर")
            total_area = st.number_input("कुल एरिया (Sq.Ft)", min_value=0.0)
            buy_rate = st.number_input("खरीद दर (₹ प्रति Sq.Ft)", min_value=0.0)
            advance_paid = st.number_input("दिया गया एडवांस बयाना (₹)", min_value=0.0)

            if st.form_submit_button("☁️ सीधे इंटरनेट क्लाउड पर सुरक्षित सेव करें"):
                if not prop_id or not seller_name:
                    st.error("❌ खसरा नंबर और नाम डालना जरूरी है!")
                else:
                    total_cost = total_area * buy_rate
                    balance_to_seller = total_cost - advance_paid
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    new_inv = pd.DataFrame([{"prop_id": prop_id, "seller_name": seller_name, "state": selected_state, "district": selected_district, "tehsil": selected_tehsil, "patwari_halka": selected_halka, "village": selected_village, "total_area": total_area, "available_area": total_area, "buy_rate": buy_rate, "total_cost": total_cost, "date_added": now}])
                    inv_updated = pd.concat([inv_df, new_inv], ignore_index=True)
                    
                    new_khata = pd.DataFrame([{"tx_date": now, "party_type": 'विक्रेता (किसान)', "party_name": seller_name, "party_phone": seller_phone, "prop_id": prop_id, "deal_amount": total_cost, "amount_paid_received": advance_paid, "balance_amount": balance_to_seller, "payment_mode": "क्लाउड प्रविष्टि", "notes": "नया भू-सौदा दर्ज"}])
                    khata_updated = pd.concat([khata_df, new_khata], ignore_index=True)
                    
                    conn.update(worksheet="Inventory", data=inv_updated)
                    conn.update(worksheet="KhataBook", data=khata_updated)
                    st.success("🎉 अद्भुत! डेटा सीधे आपके सुरक्षित गूगल क्लाउड ड्राइव में सिंक हो गया है।")

    # 3. ग्राहक प्लॉट बिक्री (क्रेता खता)
    with menu[2]:
        st.subheader("💸 ग्राहक प्लॉट बिक्री एवं डिजिटल उधारी लेजर")
        if inv_df.empty:
            st.warning("स्टॉक बही में कोई खसरा उपलब्ध नहीं है। पहले ज़मीन एंट्री करें।")
        else:
            available_plots = inv_df[pd.to_numeric(inv_df['available_area'], errors='coerce') > 0]['prop_id'].tolist()
            with st.form("sale_form", clear_on_submit=True):
                cust_name = st.text_input("👤 ग्राहक (क्रेता) का पूरा नाम")
                cust_phone = st.text_input("📱 ग्राहक का मोबाइल")
                sel_prop = st.selectbox("🎯 खसरा नंबर चुनें", available_plots)
                
                p_info = inv_df[inv_df['prop_id'] == sel_prop].iloc[0]
                sell_area = st.number_input("बेचा जा रहा एरिया (Sq.Ft)", min_value=1.0, max_value=float(p_info['available_area']))
                sell_rate = st.number_input("बिक्री दर (₹)", min_value=1.0)
                amt_received = st.number_input("प्राप्त नगद/चेक राशि (₹)", min_value=0.0)

                if st.form_submit_button("🧾 क्लाउड रसीद एवं बिल जारी करें"):
                    total_deal = sell_area * sell_rate
                    balance_from_cust = total_deal - amt_received
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    inv_df.loc[inv_df['prop_id'] == sel_prop, 'available_area'] = float(p_info['available_area']) - sell_area
                    
                    new_sale = pd.DataFrame([{"tx_date": now, "party_type": 'क्रेता (ग्राहक)', "party_name": cust_name, "party_phone": cust_phone, "prop_id": sel_prop, "deal_amount": total_deal, "amount_paid_received": amt_received, "balance_amount": balance_from_cust, "payment_mode": "确认", "notes": "प्लॉट आवंटन सौदा"}])
                    khata_updated = pd.concat([khata_df, new_sale], ignore_index=True)
                    
                    conn.update(worksheet="Inventory", data=inv_df)
                    conn.update(worksheet="KhataBook", data=khata_updated)
                    
                    st.markdown(f"""
                    <div style="border: 2px solid #15803D; padding: 15px; background-color: #F4FBF7; border-radius: 8px;">
                        <h4 style="text-align: center; color: #15803D; margin: 0;">🔱 मां प्रॉपर्टी (Maa Property)</h4>
                        <p style="font-size:12px; text-align:center; color:blue;">🌐 क्लाउड डिजिटल पक्का बिल</p><hr>
                        <b>पक्षकार ग्राहक:</b> {cust_name}<br>
                        <b>खसरा नं:</b> {sel_prop} | <b>ग्राम:</b> {p_info['village']}<br>
                        <b>कुल सौदा राशि:</b> ₹{total_deal:,.2f}<br>
                        <span style="color:green;"><b>प्राप्त एडवांस:</b> ₹{amt_received:,.2f}</span><br>
                        <span style="color:red;"><b>बकाया उधारी राशि:</b> ₹{balance_from_cust:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # 4. स्टॉक एवं भू-नक्शा बही
    with menu[3]:
        st.subheader("📂 लाइव खसरा क्लाउड स्टॉक सूची")
        search = st.text_input("🔍 खसरा या ग्राम खोजें")
        
        display_df = inv_df.copy()
        if search and not display_df.empty:
            display_df = display_df[display_df['prop_id'].astype(str).str.contains(search, case=False) | display_df['village'].astype(str).str.contains(search, case=False)]

        if not display_df.empty:
            for index, row in display_df.iterrows():
                st.markdown(f"""
                <div style="border: 1px solid #15803D; padding: 10px; border-radius: 6px; margin-bottom: 5px; background-color: #F0FDF4; font-size:13px;">
                    <b>📍 खसरा: {row['prop_id']} | ग्राम: {row['village']}</b><br>
                    👤 भूमिस्वामी किसान: {row['seller_name']} | 📦 उपलब्ध रकबा: {row['available_area']} Sq.Ft
                </div>
                """, unsafe_allow_html=True)
                c_b1, c_b2 = st.columns(2)
                c_b1.link_button("🗺️ छत्तीसगढ़ लाइव भू-नक्शा", "https://bhumanaksha.cg.nic.in/")
                c_b2.link_button("📄 लाइव B-I खतौनी", "https://bhuiyan.cg.nic.in/")
                st.write("---")
        else:
            st.info("स्टॉक बही खाली है।")

    # 5. पक्षकार खता बुक
    with menu[4]:
        st.subheader("🧾 पक्षकार क्लाउड डिजिटल खता लेजर")
        p_search = st.text_input("👤 पक्षकार का नाम लिखें (किसान/ग्राहक)")
        
        display_k = khata_df.copy()
        if p_search and not display_k.empty:
            display_k = display_k[display_k['party_name'].astype(str).str.contains(p_search, case=False)]

        if not display_k.empty:
            st.dataframe(display_k, use_container_width=True)
        else:
            st.info("कोई लेन-देन रिकॉर्ड नहीं मिला।")

    if st.sidebar.button("🔴 ऐप सुरक्षित बंद करें (Logout)", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
