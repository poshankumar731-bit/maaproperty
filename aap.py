import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import urllib.parse
import random
import requests

# 🎨 प्रीमियम थीम एवं मोबाइल स्क्रीन सेटिंग्स
st.set_page_config(
    page_title="मां प्रॉपर्टी डिजिटल ऐप", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🖌️ संशोधित अल्ट्रा-लग्जरी नियॉन डार्क थीम CSS
st.markdown("""
<style>
    /* पूरे ऐप का बैकग्राउंड - प्रीमियम डार्क ग्रेडिएंट */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white !important;
    }
    
    /* मेन कार्ड्स और डिब्बे (लग्जरी ग्लास लुक) */
    .main-card, div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        padding: 22px;
        border-radius: 25px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 18px;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }
    
    /* मुख्य लग्जरी हरे रंग के बटन्स */
    div.stButton > button {
        width: 100%;
        border-radius: 18px;
        height: 54px;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #16A34A, #22C55E) !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 18px rgba(22, 163, 74, 0.4);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* इनपुट बक्से - क्रिस्टल क्लियर व्हाइट टेक्स्ट लुक */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 16px !important;
        padding: 6px 14px !important;
        background-color: rgba(15, 23, 42, 0.7) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }
    
    label, p, span { color: #E2E8F0 !important; font-weight: 500; }
    .stMetric {
        background: rgba(255, 255, 255, 0.04); 
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 🔱 मुख्य लग्जरी डिजिटल हेडर
st.markdown("<h2 style='text-align: center; color: #22C55E; margin-top: -10px;'>🔱 मां प्रॉपर्टी (Maa Property)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38BDF8; font-weight: bold; margin-top:-10px;'>📱 ऑनलाइन लाइव सर्चिंग एवं असली मोबाइल OTP सुरक्षित बहीखाता</p>", unsafe_allow_html=True)
st.write("---")

INV_COLS = ['prop_id', 'seller_name', 'state', 'district', 'tehsil', 'ri_circle', 'patwari_halka', 'village', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'bank_name', 'acc_no', 'ifsc_code', 'upi_id', 'date_added']
KHATA_COLS = ['tx_date', 'party_type', 'party_name', 'party_phone', 'prop_id', 'deal_amount', 'amount_paid_received', 'balance_amount', 'payment_mode', 'bank_tx_id', 'notes']

# ==========================================
# ☁️ लाइव क्लाउड डेटाबेस कनेक्शन (KeyError सुरक्षित मोड)
# ==========================================
@st.cache_data(ttl=0)
def load_app_data():
    inv_blank = pd.DataFrame(columns=INV_COLS)
    khata_blank = pd.DataFrame(columns=KHATA_COLS)
    sets_blank = pd.DataFrame([
        {"key": "username", "value": "admin"}, 
        {"key": "password", "value": "Radhe@2026"}, 
        {"key": "app_phone", "value": "9876543210"},
        {"key": "sms_api_key", "value": "YOUR_API_KEY"}
    ])
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            inv = pd.DataFrame(conn.read(worksheet="Inventory"))
            for col in INV_COLS:
                if col not in inv.columns: inv[col] = None
        except: inv = inv_blank
        try:
            khata = pd.DataFrame(conn.read(worksheet="KhataBook"))
            for col in KHATA_COLS:
                if col not in khata.columns: khata[col] = None
        except: khata = khata_blank
        try:
            sets = pd.DataFrame(conn.read(worksheet="Settings"))
            if sets.empty or 'key' not in sets.columns: sets = sets_blank
        except: sets = sets_blank
        return conn, inv, khata, sets
    except:
        return None, inv_blank, khata_blank, sets_blank

conn, inv_df, khata_df, settings_df = load_app_data()

# त्रुटि सुरक्षा के लिए कॉलम सुनिश्चित करना (ताकि KeyError कभी न आए)
for c in INV_COLS:
    if c not in inv_df.columns: inv_df[c] = None
for c in KHATA_COLS:
    if c not in khata_df.columns: khata_df[c] = None

def get_setting(key_name, default_val):
    if not settings_df.empty and 'key' in settings_df.columns and 'value' in settings_df.columns:
        try:
            val = settings_df[settings_df['key'] == key_name]['value'].values[0]
            return str(val)
        except: return default_val
    return default_val

current_user = get_setting('username', 'admin')
current_pass = get_setting('password', 'Radhe@2026')
current_phone = get_setting('app_phone', '9876543210')
sms_key = get_setting('sms_api_key', '')

CG_DISTRICTS = [
    "बालोद (Balod)", "बलौदा बाज़ार (Baloda Bazar)", "बलरामपुर (Balrampur)", "बस्तर (Bastar)", 
    "बेमेतरा (Bemetara)", "बीजापुर (Bijapur)", "बिलासपुर (Bilaspur)", "दंतेवाड़ा (Dantewada)", 
    "धमतरी (Dhamtari)", "दुर्ग (Durg)", "गरियाबंद (Gariaband)", "गौरेला-पेंड्रा-मरवाही", 
    "जांजगीर-चांपा", "जशपुर (Jashpur)", "कबीरधाम (Kawardha)", "कांकेर (Kanker)", 
    "कोंडागांव (Kondagaon)", "कोरबा (Korba)", "कोरिया (Korea)", "महासमुंद (Mahasamund)", 
    "मनेंद्रगढ़-चिरमिरी-भरतपुर", "मोहला-मानपुर-अंबागढ़ चौकी", "मुंगेली (Mungeli)", "नारायणपुर", 
    "रायगढ़ (Raigarh)", "रायपुर (Raipur)", "राजनांदगांव", "सक्ती (Sakti)", "सारंगढ़-बिलाईगढ़", 
    "सुकमा (Sukma)", "सूरजपुर (Surajpur)", "सरगुजा (Surguja)", "खैरागढ़-छुईखदान-गंडई"
]

def send_real_otp_to_mobile(mobile_no, otp_code):
    if not sms_key or sms_key == "YOUR_API_KEY":
        return True, "DEMO_MODE"
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {"authorization": sms_key, "variables_values": str(otp_code), "route": "otp", "numbers": str(mobile_no)}
    headers = {'cache-control': "no-cache"}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=5)
        return True, response.json()
    except: return False, "नेटवर्क एरर"

# ==========================================
# 🔒 मोबाइल असली OTP सुरक्षा गेट
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'generated_otp' not in st.session_state:
    st.session_state.generated_otp = None

if not st.session_state.logged_in:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #38BDF8;'>🔒 डबल-स्टेप असली OTP सुरक्षा लॉगिन</h4>", unsafe_allow_html=True)
    
    if not st.session_state.otp_sent:
        with st.form("login_step1"):
            u = st.text_input("👤 एडमिन यूज़रनेम दर्ज करें")
            p = st.text_input("🔑 एडमिन पासवर्ड दर्ज करें", type="password")
            st.caption(f"ℹ OTP आपके रजिस्टर्ड नंबर पर भेजा जाएगा: **++++++{current_phone[-4:]}**")
            
            if st.form_submit_button("📲 असली मोबाइल OTP भेजें"):
                if u == current_user and p == current_pass:
                    st.session_state.generated_otp = str(random.randint(100100, 999999))
                    success, resp = send_real_otp_to_mobile(current_phone, st.session_state.generated_otp)
                    st.session_state.otp_sent = True
                    if resp == "DEMO_MODE":
                        st.info(f"🔑 [टेस्टिंग मोड]: आपका असली OTP है: {st.session_state.generated_otp}")
                    else:
                        st.success(f"✅ आपके नंबर पर असली OTP भेज दिया गया है!")
                    st.rerun()
                else: st.error("❌ गलत विवरण! कृपया दोबारा जांचें।")
    else:
        with st.form("login_step2"):
            entered_otp = st.text_input("🔢 मोबाइल पर आया OTP यहाँ लिखें", type="password")
            col_b1, col_b2 = st.columns(2)
            if col_b1.form_submit_button("🔓 ऐप अनलॉक करें"):
                if entered_otp == st.session_state.generated_otp:
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("❌ गलत OTP दर्ज किया गया है!")
            if col_b2.form_submit_button("🔄 दोबारा पासवर्ड डालें"):
                st.session_state.otp_sent = False
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🏢 मुख्य ऐप इंटरफ़ेस (लॉगिन के बाद)
# ==========================================
else:
    menu = st.tabs(["📊 डैशबोर्ड", "🌾 ज़मीन खरीद (एंट्री)", "💸 बिक्री & QR रसीद", "🔍 लाइव स्मार्ट सर्च इंजन", "📂 पूरा स्टॉक", "🧾 खाता-बही", "⚙️ सेटिंग्स"])

    # 1. डैशबोर्ड
    with menu[0]:
        v_bal, k_paid, k_bal = 0.0, 0.0, 0.0
        try:
            v_bal = pd.to_numeric(khata_df[khata_df['party_type'] == 'विक्रेता (किसान)']['balance_amount'], errors='coerce').sum()
            k_bal = pd.to_numeric(khata_df[khata_df['party_type'] == 'क्रेता (ग्राहक)']['balance_amount'], errors='coerce').sum()
            k_paid = pd.to_numeric(khata_df[khata_df['party_type'] == 'क्रेता (ग्राहक)']['amount_paid_received'], errors='coerce').sum()
        except:
            pass

        c1, c2 = st.columns(2)
        with c1:
            st.metric("🌾 किसानों को कुल देय राशि", f"₹{v_bal:,.2f}")
            st.metric("💵 कुल नगद आवक (Inflow)", f"₹{k_paid:,.2f}")
        with c2:
            st.metric("🔴 ग्राहकों से लेना (बकाया)", f"₹{k_bal:,.2f}")
            st.metric("🏡 कुल लाइव स्टॉक रजिस्ट्री", len(inv_df))
        st.write("---")
        st.success(f"📱 एडमिन पैनल एक्टिव | लिंक मोबाइल: +91 {current_phone}")

    # 2. ज़मीन खरीद फॉर्म
    with menu[1]:
        st.markdown("##### 🌾 नई ज़मीन / प्लॉट खरीद एंट्री फॉर्म")
        
        with st.form("bhulekh_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                selected_district = st.selectbox("1. जिला चुनें", CG_DISTRICTS)
                selected_tehsil = st.text_input("2. तहसील का नाम दर्ज करें *")
            with col2:
                selected_ri = st.text_input("3. राजस्व निरीक्षक मंडल (RI Circle)")
                selected_halka = st.text_input("4. पटवारी हल्का नंबर (PH No.) *")
                
            selected_village = st.text_input("5. ग्राम / नगर का नाम *")
            
            st.write("---")
            seller_name = st.text_input("विक्रेता (किसान) का नाम *")
            seller_phone = st.text_input("किसान का मोबाइल नंबर")
            prop_id = st.text_input("खसरा नंबर / प्लॉट नंबर *")
            
            col3, col4, col5 = st.columns(3)
            with col3: total_area = st.number_input("कुल रकबा (Sq.Ft)", min_value=0.0)
            with col4: buy_rate = st.number_input("खरीद दर (₹/Sq.Ft)", min_value=0.0)
            with col5: advance_paid = st.number_input("दिया गया बयाना राशि (₹)", min_value=0.0)
            
            st.write("---")
            v_bank_name = st.text_input("बैंक का नाम")
            v_acc_no = st.text_input("खाता नंबर")
            v_ifsc = st.text_input("IFSC कोड")
            v_upi_id = st.text_input("विक्रेता UPI ID")
            payment_mode = st.selectbox("भुगतान विधि", ["नकद (Cash)", "चेक (Cheque)", "RTGS/UPI"])

            if st.form_submit_button("💾 क्लाउड तिजोरी में सुरक्षित सेव करें"):
                if not prop_id or not seller_name or not selected_village or not selected_tehsil or not selected_halka:
                    st.error("❌ त्रुटि: कृपया अनिवार्य (*) वाले बक्से अवश्य भरें!")
                else:
                    total_cost = total_area * buy_rate
                    balance_to_seller = total_cost - advance_paid
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    new_inv = pd.DataFrame([{"prop_id": prop_id, "seller_name": seller_name, "state": "छत्तीसगढ़", "district": selected_district, "tehsil": selected_tehsil, "ri_circle": selected_ri, "patwari_halka": selected_halka, "village": selected_village, "total_area": total_area, "available_area": total_area, "buy_rate": buy_rate, "total_cost": total_cost, "bank_name": v_bank_name, "acc_no": v_acc_no, "ifsc_code": v_ifsc, "upi_id": v_upi_id, "date_added": now}])
                    new_khata = pd.DataFrame([{"tx_date": now, "party_type": 'विक्रेता (किसान)', "party_name": seller_name, "party_phone": seller_phone, "prop_id": prop_id, "deal_amount": total_cost, "amount_paid_received": advance_paid, "balance_amount": balance_to_seller, "payment_mode": payment_mode, "bank_tx_id": "बयाना", "notes": f"तहसील: {selected_tehsil}, हल्का: {selected_halka}"}])
                    
                    if conn:
                        conn.update(worksheet="Inventory", data=pd.concat([inv_df, new_inv], ignore_index=True))
                        conn.update(worksheet="KhataBook", data=pd.concat([khata_df, new_khata], ignore_index=True))
                    st.success("🎉 डेटा लाइव क्लाउड में सुरक्षित हो गया है।")
                    st.rerun()

    # 3. प्लॉट बिक्री
    with menu[2]:
        st.markdown("##### 💸 ग्राहक आवंटन एवं डिजिटल पेमेंट स्कैनर")
        if inv_df.empty:
            st.warning("⚠️ स्टॉक में कोई प्लॉट उपलब्ध नहीं है।")
        else:
            inv_df['available_area'] = pd.to_numeric(inv_df['available_area'], errors='coerce').fillna(0)
            available_plots = inv_df[inv_df['available_area'] > 0]['prop_id'].tolist()
            
            if not available_plots: st.warning("⚠️ बिक्री हेतु कोई रकबा खाली नहीं है।")
            else:
                with st.form("sale_form"):
                    cust_name = st.text_input("👤 ग्राहक का पूरा नाम")
                    cust_phone = st.text_input("📱 ग्राहक का मोबाइल नंबर")
                    sel_prop = st.selectbox("🎯 खसरा / प्लॉट नंबर चुनें", available_plots)
                    
                    p_info = inv_df[inv_df['prop_id'] == sel_prop].iloc[0]
                    sell_area = st.number_input("बेचा जा रहा एरिया (Sq.Ft)", min_value=1.0, max_value=float(p_info['available_area'] if p_info['available_area'] > 0 else 1.0))
                    sell_rate = st.number_input("बिक्री दर (₹/Sq.Ft)", min_value=1.0)
                    amt_received = st.number_input("प्राप्त राशि (₹)", min_value=0.0)
                    pay_method = st.selectbox("भुगतान माध्यम", ["नकद (Cash)", "UPI/ऑनलाइन स्कैनर", "बैंक ट्रांसफर"])
                    bank_tx_id = st.text_input("✍️ बैंक UTR नंबर")

                    submit_sale = st.form_submit_button("🧾 डिजिटल रसीद लॉक करें")

                if submit_sale and cust_name:
                    total_deal = sell_area * sell_rate
                    balance_from_cust = total_deal - amt_received
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    inv_df.loc[inv_df['prop_id'] == sel_prop, 'available_area'] = float(p_info['available_area']) - sell_area
                    new_sale = pd.DataFrame([{"tx_date": now, "party_type": 'क्रेता (ग्राहक)', "party_name": cust_name, "party_phone": cust_phone, "prop_id": sel_prop, "deal_amount": total_deal, "amount_paid_received": amt_received, "balance_amount": balance_from_cust, "payment_mode": pay_method, "bank_tx_id": bank_tx_id, "notes": f"UTR: {bank_tx_id}"}])
                    
                    if conn:
                        conn.update(worksheet="Inventory", data=inv_df)
                        conn.update(worksheet="KhataBook", data=pd.concat([khata_df, new_sale], ignore_index=True))
                    st.success("🎉 ग्राहक रसीद सुरक्षित हो गई है!")
                    st.rerun()

    # 4. लाइव स्मार्ट सर्च इंजन
    with menu[3]:
        st.markdown("##### 🔍 छत्तीसगढ़ लाइव एआई सर्च इंजन (स्मार्ट फ़िल्टर मोड)")
        c_search1, c_search2 = st.columns(2)
        with c_search1:
            search_dist = st.selectbox("🎯 जिला के आधार पर छानें", ["-- सभी जिले --"] + CG_DISTRICTS)
            search_teh = st.text_input("✍️ विशिष्ट तहसील का नाम लिखें")
        with c_search2:
            search_halka = st.text_input("✍️ पटवारी हल्का नंबर खोजें")
            search_vill = st.text_input("✍️ ग्राम / नगर का नाम लिखें")
            
        filtered_df = inv_df.copy()
        if search_dist != "-- सभी जिले --":
            filtered_df = filtered_df[filtered_df['district'] == search_dist]
        if search_teh:
            filtered_df = filtered_df[filtered_df['tehsil'].astype(str).str.contains(search_teh, case=False)]
        if search_halka:
            filtered_df = filtered_df[filtered_df['patwari_halka'].astype(str).str.contains(search_halka, case=False)]
        if search_vill:
            filtered_df = filtered_df[filtered_df['village'].astype(str).str.contains(search_vill, case=False)]
            
        st.write(f"📊 **खोज परिणाम:** कुल **{len(filtered_df)}** रिकॉर्ड मिले।")
        st.dataframe(filtered_df[['prop_id', 'seller_name', 'district', 'tehsil', 'patwari_halka', 'village', 'available_area']], use_container_width=True, hide_index=True)

    # 5. पूरा स्टॉक
    with menu[4]:
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

    # 6. खाता-बही
    with menu[5]:
        if not khata_df.empty and 'party_name' in khata_df.columns:
            unique_parties = sorted(khata_df['party_name'].dropna().unique().tolist())
            selected_party = st.selectbox("👤 पक्षकार का नाम चुनें:", ["-- नाम चुनें --"] + unique_parties)
            if selected_party != "-- नाम चुनें --":
                p_data = khata_df[khata_df['party_name'] == selected_party]
                st.dataframe(p_data, use_container_width=True, hide_index=True)

    # 7. सेटिंग्स पैनल
    with menu[6]:
        with st.form("settings_form"):
            new_user = st.text_input("✏️ नया यूज़रनेम", value=current_user)
            new_pass = st.text_input("✏️ नया पासवर्ड", value=current_pass)
            new_phone = st.text_input("✏️ लिंक मोबाइल नंबर", value=current_phone)
            new_key = st.text_input("🔑 Fast2SMS API Key", value=sms_key, type="password")
            
            if st.form_submit_button("💾 सेटिंग्स क्लाउड में लॉक करें"):
                if conn:
                    updated_settings = pd.DataFrame([{"key": "username", "value": str(new_user)}, {"key": "password", "value": str(new_pass)}, {"key": "app_phone", "value": str(new_phone)}, {"key": "sms_api_key", "value": str(new_key)}])
                    conn.update(worksheet="Settings", data=updated_settings)
                    st.success("🎉 सेटिंग्स लाइव सेव हो गई हैं!")
                    st.cache_data.clear()
                    st.rerun()

    if st.sidebar.button("🔴 ऐप सुरक्षित बंद करें"):
        st.session_state.logged_in = False
        st.session_state.otp_sent = False
        st.rerun()
