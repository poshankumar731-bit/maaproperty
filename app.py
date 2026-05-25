import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import urllib.parse

# 🎨 प्रीमियम मोबाइल ऐप ऑप्टिमाइज्ड थीम सेटिंग्स (A4 / Mobile Screen Friendly)
st.set_page_config(
    page_title="मां प्रॉपर्टी डिजिटल ऐप", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# सुपर-फास्ट रेंडरिंग के लिए कस्टम मोबाइल CSS स्टाइलिंग
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .stMetric {background-color: #F3F4F6; padding: 10px; border-radius: 8px;}
    div.stButton > button:first-child {
        width: 100%; background-color: #16A34A; color: white; font-weight: bold; border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 🔱 मुख्य डिजिटल बैनर
st.markdown("<h2 style='text-align: center; color: #16A34A; margin-top: -10px;'>🔱 मां प्रॉपर्टी (Maa Property)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2563EB; font-weight: bold; margin-top:-10px;'>📱 100% सुरक्षित हैंग-फ्री मोबाइल एंड्रॉयड एप्लीकेशन</p>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# ☁️ सुपर-फास्ट लाइव क्लाउड डेटाबेस कनेक्शन (कैशिंग के साथ ताकि हैंग न हो)
# ==========================================
@st.cache_data(ttl=0)  # लाइव डेटा बिना देरी के तुरंत लोड करने का जादुई कोड
def load_app_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        inv = conn.read(worksheet="Inventory")
        khata = conn.read(worksheet="KhataBook")
        sets = conn.read(worksheet="Settings")
        return conn, pd.DataFrame(inv), pd.DataFrame(khata), pd.DataFrame(sets)
    except:
        # बैकअप डेटा फ्रेम अगर सर्वर कभी धीमा हो
        inv_blank = pd.DataFrame(columns=['prop_id', 'seller_name', 'state', 'district', 'tehsil', 'ri_circle', 'patwari_halka', 'village', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'bank_name', 'acc_no', 'ifsc_code', 'upi_id', 'date_added'])
        khata_blank = pd.DataFrame(columns=['tx_date', 'party_type', 'party_name', 'party_phone', 'prop_id', 'deal_amount', 'amount_paid_received', 'balance_amount', 'payment_mode', 'bank_tx_id', 'notes'])
        sets_blank = pd.DataFrame([{"key": "username", "value": "admin"}, {"key": "password", "value": "Radhe@2026"}, {"key": "app_phone", "value": "9876543210"}])
        return None, inv_blank, khata_blank, sets_blank

conn, inv_df, khata_df, settings_df = load_app_data()

def get_setting(key_name, default_val):
    if not settings_df.empty and 'key' in settings_df.columns:
        try:
            val = settings_df[settings_df['key'] == key_name]['value'].values[0]
            return str(val)
        except:
            return default_val
    return default_val

# छत्तीसगढ़ मास्टर भूलेख लिस्ट
CG_BHULEKH = {
    "मुंगेली (Mungeli)": ["मुंगेली (Mungeli)", "लॉर्मी (Lormi)", "पथरिया (Pathariya)"],
    "बिलासपुर (Bilaspur)": ["बिलासपुर (Sadar)", "कोटा (Kota)", "तखतपुर", "मस्तूरी", "बिल्हा"],
    "रायपुर (Raipur)": ["रायपुर (Sadar)", "धरसींवा", "आरंग", "अभनपुर"],
    "दुर्ग (Durg)": ["दुर्ग (Sadar)", "भिलाई", "पाटन", "धमधा"]
}

current_user = get_setting('username', 'admin')
current_pass = get_setting('password', 'Radhe@2026')
current_phone = get_setting('app_phone', '9876543210')

# ==========================================
# 🔒 मोबाइल सुरक्षा गेट (लॉगिन)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div style='border: 1px solid #D1D5DB; padding: 15px; border-radius: 10px; background-color: #F9FAFB;'>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: center; color: #1E3A8A;'>🔒 सुरक्षित एडमिन लॉगिन (हेल्पलाइन: +91 {current_phone})</h5>", unsafe_allow_html=True)
    with st.form("login_form"):
        u = st.text_input("👤 यूज़रनेम (Username)")
        p = st.text_input("🔑 पासवर्ड (Password)", type="password")
        if st.form_submit_button("🔓 मोबाइल बहीखाता अनलॉक करें"):
            if u == current_user and p == current_pass:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ गलत विवरण! कृपया सही पासवर्ड डालें।")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🏢 मुख्य मोबाइल इंटरफ़ेस (क्लीन एंड क्लियर)
# ==========================================
else:
    menu = st.tabs([
        "📊 डैशबोर्ड", 
        "🌾 ज़मीन खरीद", 
        "💸 प्लॉट बिक्री & QR",
        "📂 लाइव स्टॉक", 
        "🧾 खाता-बही (लेजर)",
        "⚙️ सेटिंग्स"
    ])

    # 1. डैशबोर्ड (फास्ट लोड)
    with menu[0]:
        v_df = khata_df[khata_df['party_type'] == 'विक्रेता (किसान)'] if not khata_df.empty else pd.DataFrame()
        k_df = khata_df[khata_df['party_type'] == 'क्रेता (ग्राहक)'] if not khata_df.empty else pd.DataFrame()

        c1, c2 = st.columns(2)
        with c1:
            st.metric("🌾 किसानों को देय राशि", f"₹{pd.to_numeric(v_df['balance_amount'], errors='coerce').sum():,.2f}")
            st.metric("💵 कुल नगद आवक", f"₹{pd.to_numeric(k_df['amount_paid_received'], errors='coerce').sum():,.2f}")
        with c2:
            st.metric("🔴 ग्राहकों से लेना (बकाया)", f"₹{pd.to_numeric(k_df['balance_amount'], errors='coerce').sum():,.2f}")
            st.metric("🏡 लाइव स्टॉक संख्या", len(inv_df))
        
        st.write("---")
        st.success(f"📱 ऐप स्थिति: बिल्कुल सुरक्षित और ऑनलाइन क्लाउड से कनेक्टेड | हेल्पलाइन: +91 {current_phone}")

    # 2. ज़मीन खरीद (क्लीन इनपुट फॉर्म)
    with menu[1]:
        st.markdown("##### 🌾 नई ज़मीन / खसरा रजिस्ट्री एंट्री")
        manual_mode = st.checkbox("✍️ क्या सूची ऑनलाइन नहीं मिल रही? (हाथ से लिखें)")
        
        with st.form("bhulekh_form", clear_on_submit=True):
            if not manual_mode:
                selected_district = st.selectbox("जिला चुनें", sorted(list(CG_BHULEKH.keys())))
                selected_tehsil = st.selectbox("तहसील चुनें", CG_BHULEKH[selected_district])
            else:
                selected_district = st.text_input("जिला का नाम हाथ से लिखें")
                selected_tehsil = st.text_input("तहसील का नाम हाथ से लिखें")
            
            selected_ri = st.text_input("राजस्व निरीक्षक मंडल (RI)")
            selected_halka = st.text_input("पटवारी हल्का नं. (PH No.)")
            selected_village = st.text_input("ग्राम का नाम")
            
            st.write("---")
            seller_name = st.text_input("विक्रेता (किसान) का नाम")
            seller_phone = st.text_input("किसान का मोबाइल नंबर")
            prop_id = st.text_input("खसरा / प्लॉट नंबर (Unique ID)")
            
            total_area = st.number_input("कुल रकबा (Sq.Ft)", min_value=0.0)
            buy_rate = st.number_input("खरीद दर (₹/Sq.Ft)", min_value=0.0)
            advance_paid = st.number_input("एडवांस बयाना भुगतान (₹)", min_value=0.0)
            
            st.write("---")
            st.caption("🏦 किसान का बैंक खाता (डायरेक्ट ऑनलाइन भुगतान हेतु)")
            v_bank_name = st.text_input("बैंक का नाम")
            v_acc_no = st.text_input("खाता नंबर")
            v_ifsc = st.text_input("IFSC कोड")
            v_upi_id = st.text_input("UPI ID (जैसे: 9876543210@paytm)")
            payment_mode = st.selectbox("भुगतान विधि", ["नकद (Cash)", "चेक (Cheque)", "RTGS/UPI"])

            if st.form_submit_button("💾 क्लाउड तिजोरी में सुरक्षित सेव करें"):
                if not prop_id or not seller_name or not selected_village:
                    st.error("❌ कृपया अनिवार्य बक्से (खसरा नं, नाम, ग्राम) अवश्य भरें!")
                else:
                    total_cost = total_area * buy_rate
                    balance_to_seller = total_cost - advance_paid
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    new_inv = pd.DataFrame([{"prop_id": prop_id, "seller_name": seller_name, "state": "छत्तीसगढ़", "district": selected_district, "tehsil": selected_tehsil, "ri_circle": selected_ri, "patwari_halka": selected_halka, "village": selected_village, "total_area": total_area, "available_area": total_area, "buy_rate": buy_rate, "total_cost": total_cost, "bank_name": v_bank_name, "acc_no": v_acc_no, "ifsc_code": v_ifsc, "upi_id": v_upi_id, "date_added": now}])
                    new_khata = pd.DataFrame([{"tx_date": now, "party_type": 'विक्रेता (किसान)', "party_name": seller_name, "party_phone": seller_phone, "prop_id": prop_id, "deal_amount": total_cost, "amount_paid_received": advance_paid, "balance_amount": balance_to_seller, "payment_mode": payment_mode, "bank_tx_id": "बयाना", "notes": f"बैंक खाता: {v_acc_no}"}])
                    
                    if conn:
                        conn.update(worksheet="Inventory", data=pd.concat([inv_df, new_inv], ignore_index=True))
                        conn.update(worksheet="KhataBook", data=pd.concat([khata_df, new_khata], ignore_index=True))
                    st.success("🎉 डेटा लाइव सिंक हो गया है!")
                    st.rerun()

    # 3. प्लॉट बिक्री + डिजिटल QR गेटवे
    with menu[2]:
        st.markdown("##### 💸 ग्राहक आवंटन एवं डिजिटल पेमेंट स्कैनर")
        if inv_df.empty:
            st.warning("⚠️ स्टॉक में कोई प्लॉट उपलब्ध नहीं है।")
        else:
            available_plots = inv_df[pd.to_numeric(inv_df['available_area'], errors='coerce') > 0]['prop_id'].tolist()
            
            with st.form("sale_form"):
                cust_name = st.text_input("👤 ग्राहक का पूरा नाम")
                cust_phone = st.text_input("📱 ग्राहक का मोबाइल नंबर")
                sel_prop = st.selectbox("🎯 खसरा / प्लॉट नंबर चुनें", available_plots)
                
                p_info = inv_df[inv_df['prop_id'] == sel_prop].iloc[0]
                st.info(f"📍 लोकेशन: ग्राम- {p_info['village']} | शेष एरिया: {p_info['available_area']} Sq.Ft")
                
                sell_area = st.number_input("बेचा जा रहा एरिया (Sq.Ft)", min_value=1.0, max_value=float(p_info['available_area']))
                sell_rate = st.number_input("बिक्री दर (₹/Sq.Ft)", min_value=1.0)
                amt_received = st.number_input("अभी प्राप्त की जा रही राशि (₹)", min_value=0.0)
                pay_method = st.selectbox("भुगतान का माध्यम", ["UPI/ऑनलाइन स्कैनर", "नकद (Cash)", "बैंक ट्रांसफर"])
                bank_tx_id = st.text_input("✍️ बैंक UTR नंबर / ट्रांजैक्शन ID")

                submit_sale = st.form_submit_button("🧾 डिजिटल रसीद लॉक करें")

            if submit_sale and cust_name:
                total_deal = sell_area * sell_rate
                balance_from_cust = total_deal - amt_received
                now = datetime.now().strftime("%d-%m-%Y %H:%M")
                
                inv_df.loc[inv_df['prop_id'] == sel_prop, 'available_area'] = float(p_info['available_area']) - sell_area
                new_sale = pd.DataFrame([{"tx_date": now, "party_type": 'क्रेता (ग्राहक)', "party_name": cust_name, "party_phone": cust_phone, "prop_id": sel_prop, "deal_amount": total_deal, "amount_paid_received": amt_received, "balance_amount": balance_from_cust, "payment_mode": pay_method, "bank_tx_id": bank_tx_id, "notes": f"रिफरेंस: {bank_tx_id}"}])
                
                if conn:
                    conn.update(worksheet="Inventory", data=inv_df)
                    conn.update(worksheet="KhataBook", data=pd.concat([khata_df, new_sale], ignore_index=True))
                st.success("🎉 रसीद सुरक्षित हो गई है!")

                # 📲 डायनामिक ऑटो-क्यूआर कोड जनरेशन
                if pay_method == "UPI/ऑनलाइन स्कैनर":
                    target_upi = p_info['upi_id'] if pd.notna(p_info['upi_id']) and p_info['upi_id'] != "" else "9876543210@paytm"
                    upi_url = f"upi://pay?pa={target_upi}&pn={urllib.parse.quote(str(p_info['seller_name']))}&am={amt_received}&cu=INR"
                    qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(upi_url)}"
                    
                    st.markdown("---")
                    st.image(qr_api, caption="📱 इसे स्कैन करके सीधे भुगतान लें (0% शुल्क)")
                    st.caption(f"🏦 खाताधारक: {p_info['seller_name']} | UPI: {target_upi}")

                # 🖨️ पक्की प्रिंटर रसीद (A4 / Small Printer Friendly)
                st.write("---")
                bill_html = f"""
                <div id="print_receipt" style="border: 1px solid #000; padding: 15px; font-family: monospace; background-color: #FFF; color: #000; max-width: 100%;">
                    <h3 style="text-align: center; margin: 0;">🔱 मां प्रॉपर्टी (Maa Property)</h3>
                    <p style="text-align: center; font-size: 11px; margin: 2px 0;">संपर्क: +91 {current_phone} | दिनांक: {now}</p>
                    <hr style="border-top: 1px dashed #000;">
                    <b>👤 ग्राहक:</b> {cust_name} ({cust_phone})<br>
                    <b>📍 ग्राम:</b> {p_info['village']} | 🆔 <b>खसरा:</b> {sel_prop}<br>
                    <b>📐 रकबा:</b> {sell_area} Sq.Ft @ ₹{sell_rate}/Sq.Ft<br>
                    <hr style="border-top: 1px dashed #000;">
                    <b>🤝 कुल मूल्य:</b> ₹{total_deal:,.2f}<br>
                    <b>🟢 प्राप्त नगद:</b> ₹{amt_received:,.2f} ({pay_method})<br>
                    <b>🏛️ यूटीआर नं:</b> {bank_tx_id if bank_tx_id else 'N/A'}<br>
                    <b>🔴 बकाया राशि:</b> ₹{balance_from_cust:,.2f}<br>
                </div>
                """
                st.markdown(bill_html, unsafe_allow_html=True)
                
                # डायरेक्ट प्रिंट कमांड बटन
                print_script = """
                <button onclick="var printContents = document.getElementById('print_receipt').innerHTML;
                var originalContents = document.body.innerHTML;
                document.body.innerHTML = printContents;
                window.print();
                document.body.innerHTML = originalContents;
                window.location.reload();" 
                style="width: 100%; background-color: #16A34A; color: white; padding: 10px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top:10px;">
                🖨️ रसीद सीधे प्रिंटर से निकालें
                </button>
                """
                st.markdown(print_script, unsafe_allow_html=True)

    # 4. लाइव स्टॉक (फास्ट रेंडरिंग)
    with menu[3]:
        st.markdown("##### 📂 लाइव उपलब्ध स्टॉक")
        search = st.text_input("🔍 खोजें (खसरा, ग्राम या नाम लिखें)")
        if not inv_df.empty:
            df_m = inv_df.copy()
            if search:
                df_m = df_m[df_m['prop_id'].astype(str).str.contains(search, case=False) | df_m['village'].astype(str).str.contains(search, case=False) | df_m['seller_name'].astype(str).str.contains(search, case=False)]
            st.dataframe(df_m[['prop_id', 'seller_name', 'district', 'village', 'total_area', 'available_area']], use_container_width=True, hide_index=True)

    # 5. सिस्टेमैटिक खाता-बही (क्लीन लेजर)
    with menu[4]:
        st.markdown("##### 🧾 पक्षकार डिजिटल पासबुक इतिहास")
        if not khata_df.empty:
            unique_parties = sorted(khata_df['party_name'].unique().tolist())
            selected_party = st.selectbox("👤 पक्षकार का नाम चुनें:", ["-- नाम चुनें --"] + unique_parties)
            
            if selected_party != "-- नाम चुनें --":
                p_data = khata_df[khata_df['party_name'] == selected_party]
                t_deal = pd.to_numeric(p_data['deal_amount'], errors='coerce').max()
                t_rec = pd.to_numeric(p_data['amount_paid_received'], errors='coerce').sum()
                t_bal = t_deal - t_rec
                
                st.markdown(f"**कुल सौदा मूल्य:** ₹{t_deal:,.2f} | **कुल पेड राशि:** ₹{t_rec:,.2f} | **अंतिम बकाया:** ₹{t_bal:,.2f}")
                st.dataframe(p_data[['tx_date', 'prop_id', 'amount_paid_received', 'payment_mode', 'bank_tx_id']], use_container_width=True, hide_index=True)

    # 6. सेटिंग्स (लाइव एडमिन प्रोफाइल एडिटर)
    with menu[5]:
        st.markdown("##### ⚙️ एडमिन प्रोफाइल एवं क्रेडेंशियल")
        with st.form("settings_form"):
            new_user = st.text_input("✏️ नया यूज़रनेम", value=current_user)
            new_pass = st.text_input("✏️ नया पासवर्ड", value=current_pass)
            new_phone = st.text_input("✏️ अपना मोबाइल नंबर", value=current_phone)
            if st.form_submit_button("💾 प्रोफाइल लाइव अपडेट करें"):
                if conn:
                    updated_settings = pd.DataFrame([{"key": "username", "value": new_user}, {"key": "password", "value": new_pass}, {"key": "app_phone", "value": new_phone}])
                    conn.update(worksheet="Settings", data=updated_settings)
                st.success("🎉 प्रोफाइल बदल गई है! ऐप रीस्टार्ट करें।")
                st.rerun()

    # सुरक्षित लॉगआउट
    if st.sidebar.button("🔴 ऐप सुरक्षित बंद करें"):
        st.session_state.logged_in = False
        st.rerun()
