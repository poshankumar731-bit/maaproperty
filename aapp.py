import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import random

# 🎨 प्रीमियम एडवांस्ड रियल एस्टेट थीम सेटिंग्स
st.set_page_config(
    page_title="मां प्रॉपर्टी - राष्ट्रीय डिजिटल क्लाउड", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔱 मुख्य डिजिटल बैनर
st.markdown("<h1 style='text-align: center; color: #16A34A; margin-top: -10px;'>🔱 मां प्रॉपर्टी (Maa Property)</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #2563EB;'>🌐 शत-प्रतिशत ऑटोमैटिक सरकारी भूलेख एवं डिजिटल बहीखाता</h5>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# ☁️ एडवांस्ड क्लाउड डेटाबेस कनेक्शन (Google Sheets API)
# ==========================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    inv_df = conn.read(worksheet="Inventory", ttl="0")
    khata_df = conn.read(worksheet="KhataBook", ttl="0")
    settings_df = conn.read(worksheet="Settings", ttl="0")
except:
    inv_df = pd.DataFrame(columns=['prop_id', 'seller_name', 'state', 'district', 'tehsil', 'ri_circle', 'patwari_halka', 'village', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'date_added'])
    khata_df = pd.DataFrame(columns=['tx_date', 'party_type', 'party_name', 'party_phone', 'prop_id', 'deal_amount', 'amount_paid_received', 'balance_amount', 'payment_mode', 'notes'])
    settings_df = pd.DataFrame([{"key": "username", "value": "admin"}, {"key": "password", "value": "Radhe@2026"}])

def get_setting(key_name):
    try:
        val = settings_df[settings_df['key'] == key_name]['value'].values[0]
        return str(val)
    except:
        return "Radhe@2026" if key_name == "password" else "admin"

# ==========================================
# 🗺️ असली ऑटोमैटिक मास्टर भूलेख डेटाबेस (पूरी तरह लिंक्ड)
# ==========================================
MASTER_BHULEKH = {
    "छत्तीसगढ़ (Chhattisgarh)": {
        "मुंगेली (Mungeli)": {
            "मुंगेली (Mungeli)": {
                "मुंगेली मंडल-01": {
                    "हल्का नंबर 01": ["रामपुर (Rampur)", "मोहनपुर (Mohanpur)", "तखतपुर रोड"],
                    "हल्का नंबर 02": ["दाऊपारा (Daupara)", "चन्दनपुर", "दुर्गापुर"]
                },
                "मुंगेली मंडल-02": {
                    "हल्का नंबर 03": ["करही (Karhi)", "बरेला (Barela)"],
                    "हल्का नंबर 04": ["सेतगंगा (Setganga)", "राजपालपुर"]
                }
            },
            "लॉर्मी (Lormi)": {
                "लॉर्मी मंडल": {
                    "हल्का नंबर 05": ["खुड़िया (Khudia)", "शिवपुर", "गणेशपुर"],
                    "हल्का नंबर 06": ["बकेला (Bakela)", "नवागाँव", "डिंडौरी"]
                }
            },
            "पथरिया (Pathariya)": {
                "पथरिया मंडल": {
                    "हल्का नंबर 07": ["सरगांव (Sargaon)", "पथरिया खास"],
                    "हल्का नंबर 08": ["सिलतरा", "बैतलपुर"]
                }
            }
        },
        "बिलासपुर (Bilaspur)": {
            "बिलासपुर (Sadar)": {
                "बिलासपुर शहरी मंडल": {
                    "हल्का नंबर 10": ["तिफरा (Tifra)", "सिरगिट्टी (Sirgitti)", "तखतपुर"],
                    "हल्का नंबर 11": ["सकर्री (Sakarri)", "कचहरी चौक", "मंगला"]
                }
            },
            "कोटा (Kota)": {
                "कोटा मंडल": {
                    "हल्का नंबर 12": ["बेलगहना (Belgahna)", "कोटा खास"],
                    "हल्का नंबर 13": ["रतनपुर (Ratanpur)", "केंदा"]
                }
            },
            "मस्तूरी (Masturi)": {
                "मस्तूरी मंडल": {
                    "हल्का नंबर 14": ["जयरामनगर", "मस्तूरी खास"],
                    "हल्का नंबर 15": ["सीपत (Sipat)", "मल्हार"]
                }
            }
        },
        "रायपुर (Raipur)": {
            "रायपुर (Sadar)": {
                "रायपुर मंडल": {
                    "हल्का नंबर 20": ["धरसींवा", "अभनपुर", "आरंग"],
                    "हल्का नंबर 21": ["मंदिर हसौद", "नया रायपुर"]
                }
            }
        }
    },
    "मध्य प्रदेश (Madhya Pradesh)": {
        "जबलपुर (Jabalpur)": {
            "जबलपुर": {
                "जबलपुर मंडल": {
                    "हल्का नंबर 01": ["रांझी", "खमरिया"],
                    "हल्का नंबर 02": ["पनागर", "बरेला"]
                }
            }
        },
        "भोपाल (Bhopal)": {
            "हुजूर (Huzur)": {
                "भोपाल शहरी मंडल": {
                    "हल्का नंबर 05": ["बैरागढ़", "कोलार"],
                    "हल्का नंबर 06": ["गोविंदपुरा", "अवधपुरी"]
                }
            }
        }
    },
    "अन्य राज्य (Other State - मैन्युअल एंट्री)": {
        "कृपया टाइप करें": {
            "कृपया टाइप करें": {
                "कृपया टाइप करें": {
                    "कृपया टाइप करें": ["कृपया टाइप करें"]
                }
            }
        }
    }
}

# ==========================================
# 🔒 सुरक्षा लॉगिन गेट
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown("<div style='border: 1px solid #E5E7EB; padding: 20px; border-radius: 10px; background-color: #F9FAFB;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #1E3A8A;'>🔒 एडमिन क्लाउड सुरक्षा लॉगिन</h4>", unsafe_allow_html=True)
        with st.form("login_form"):
            u = st.text_input("👤 यूज़रनेम (Username)")
            p = st.text_input("🔑 पासवर्ड (Password)", type="password")
            if st.form_submit_button("🔓 डिजिटल बहीखाता अनलॉक करें"):
                if u == get_setting('username') and p == get_setting('password'):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ गलत क्रेडेंशियल! कृपया सही विवरण डालें।")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🏢 मुख्य डिजिटल इंटरफ़ेस (लॉगिन के बाद)
# ==========================================
else:
    menu = st.tabs([
        "📊 डिजिटल डैशबोर्ड (लाइव)", 
        "🌾 ज़मीन खरीद (विक्रेता खता)", 
        "💸 प्लॉट बिक्री (क्रेता बिलिंग)",
        "📂 लाइव स्टॉक बही (भूलेख)", 
        "🧾 ऑल-इन-वन डिजिटल खता"
    ])

    # 1. डैशबोर्ड
    with menu[0]:
        st.markdown("### 📊 वित्तीय और स्टॉक लाइव स्थिति")
        v_df = khata_df[khata_df['party_type'] == 'विक्रेता (किसान)'] if not khata_df.empty else pd.DataFrame(columns=['balance_amount'])
        k_df = khata_df[khata_df['party_type'] == 'क्रेता (ग्राहक)'] if not khata_df.empty else pd.DataFrame(columns=['balance_amount', 'amount_paid_received'])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌾 किसानों को कुल देय राशि", f"₹{pd.to_numeric(v_df['balance_amount'], errors='coerce').sum():,.2f}")
        c2.metric("💵 कुल नगद आवक (प्राप्त)", f"₹{pd.to_numeric(k_df['amount_paid_received'], errors='coerce').sum():,.2f}")
        c3.metric("🔴 मार्केट उधारी (ग्राहकों से लेना)", f"₹{pd.to_numeric(k_df['balance_amount'], errors='coerce').sum():,.2f}")
        c4.metric("🏡 स्टॉक में उपलब्ध खसरे", len(inv_df))
        
        st.write("---")
        st.markdown("#### 🔗 महत्वपूर्ण भूलेख लिंक्स")
        l1, l2 = st.columns(2)
        l1.link_button("🗺️ छत्तीसगढ़ भुइयां पोर्टल", "https://bhuiyan.cg.nic.in/", use_container_width=True)
        l2.link_button("🗺️ छत्तीसगढ़ भू-नक्शा", "https://bhumanaksha.cg.nic.in/", use_container_width=True)

    # 2. ज़मीन खरीद एंट्री (विक्रेता खता) - पूरी तरह ऑटोमैटिक लिंक्ड ड्रॉपडाउन
    with menu[1]:
        st.markdown("### 🌾 पक्का भूलेख प्रविष्टि फॉर्म (फुल्ली ऑटोमैटिक सिस्टम)")
        with st.form("bhulekh_form", clear_on_submit=True):
            st.markdown("##### 📍 भौगोलिक विवरण (एक चुनने पर दूसरा अपने आप खुलेगा)")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                # 1. राज्य चयन
                state_list = list(MASTER_BHULEKH.keys())
                selected_state = st.selectbox("1. राज्य चुनें", state_list)
                
                # 2. जिला चयन (राज्य के आधार पर)
                district_list = list(MASTER_BHULEKH[selected_state].keys())
                if selected_state == "अन्य राज्य (Other State - मैन्युअल एंट्री)":
                    selected_district = st.text_input("2. जिला का नाम लिखें")
                    selected_tehsil = st.text_input("3. तहसील का नाम लिखें")
                else:
                    selected_district = st.selectbox("2. जिला चुनें", district_list)
                    # 3. तहसील चयन (जिला के आधार पर)
                    tehsil_list = list(MASTER_BHULEKH[selected_state][selected_district].keys())
                    selected_tehsil = st.selectbox("3. तहसील चुनें", tehsil_list)

            with col_b:
                if selected_state == "अन्य राज्य (Other State - मैन्युअल एंट्री)":
                    selected_ri = st.text_input("4. राजस्व निरीक्षक मंडल (RI Circle) लिखें")
                    selected_halka = st.text_input("5. पटवारी हल्का नंबर लिखें")
                    selected_village = st.text_input("6. ग्राम का नाम लिखें")
                else:
                    # 4. राजस्व निरीक्षक मंडल (RI) चयन (तहसील के आधार पर)
                    ri_list = list(MASTER_BHULEKH[selected_state][selected_district][selected_tehsil].keys())
                    selected_ri = st.selectbox("4. राजस्व निरीक्षक मंडल (RI) चुनें", ri_list)
                    
                    # 5. पटवारी हल्का नंबर चयन (RI के आधार पर)
                    halka_list = list(MASTER_BHULEKH[selected_state][selected_district][selected_tehsil][selected_ri].keys())
                    selected_halka = st.selectbox("5. पटवारी हल्का नंबर चुनें", halka_list)
                    
                    # 6. ग्राम चयन (हल्का के आधार पर)
                    village_list = MASTER_BHULEKH[selected_state][selected_district][selected_tehsil][selected_ri][selected_halka]
                    selected_village = st.selectbox("6. ग्राम/शहर चुनें", village_list)
            
            st.write("---")
            st.markdown("##### 👤 पक्षकार (किसान/विक्रेता) एवं वित्तीय विवरण")
            col_x, col_y = st.columns(2)
            with col_x:
                seller_name = st.text_input("विक्रेता / किसान का पूरा नाम")
                seller_phone = st.text_input("विक्रेता का मोबाइल नंबर")
                prop_id = st.text_input("खसरा नंबर / भूखंड नंबर (Unique ID)")
            with col_y:
                total_area = st.number_input("कुल रकबा / क्षेत्रफल (Sq.Ft)", min_value=0.0)
                buy_rate = st.number_input("खरीद दर (₹ प्रति Sq.Ft)", min_value=0.0)
                advance_paid = st.number_input("दिया गया एडवांस बयाना राशि (₹)", min_value=0.0)
            
            payment_mode = st.selectbox("भुगतान विधि", ["नकद (Cash)", "चेक (Cheque)", "RTGS/UPI/बैंक ट्रांसफर"])

            if st.form_submit_button("💾 सीधे गूगल क्लाउड तिजोरी में सुरक्षित सेव करें"):
                if not prop_id or not seller_name or not selected_district or not selected_village:
                    st.error("❌ त्रुटि: कृपया अनिवार्य जानकारी अवश्य भरें!")
                else:
                    total_cost = total_area * buy_rate
                    balance_to_seller = total_cost - advance_paid
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    new_inv = pd.DataFrame([{"prop_id": prop_id, "seller_name": seller_name, "state": selected_state, "district": selected_district, "tehsil": selected_tehsil, "ri_circle": selected_ri, "patwari_halka": selected_halka, "village": selected_village, "total_area": total_area, "available_area": total_area, "buy_rate": buy_rate, "total_cost": total_cost, "date_added": now}])
                    inv_updated = pd.concat([inv_df, new_inv], ignore_index=True)
                    
                    new_khata = pd.DataFrame([{"tx_date": now, "party_type": 'विक्रेता (किसान)', "party_name": seller_name, "party_phone": seller_phone, "prop_id": prop_id, "deal_amount": total_cost, "amount_paid_received": advance_paid, "balance_amount": balance_to_seller, "payment_mode": payment_mode, "notes": f"नया सौदा | RI: {selected_ri}, हल्का: {selected_halka}, ग्राम: {selected_village}"}])
                    khata_updated = pd.concat([khata_df, new_khata], ignore_index=True)
                    
                    conn.update(worksheet="Inventory", data=inv_updated)
                    conn.update(worksheet="KhataBook", data=khata_updated)
                    st.success(f"🎉 सफल प्रविष्टि! खसरा नंबर {prop_id} सुरक्षित रूप से क्लाउड डेटाबेस में सिंक हो गया है।")
                    st.rerun()

    # 3. ग्राहक प्लॉट बिक्री (क्रेता बिलिंग)
    with menu[2]:
        st.markdown("### 💸 ग्राहक प्लॉट आवंटन एवं डिजिटल बिलिंग")
        if inv_df.empty:
            st.warning("⚠️ स्टॉक बही में वर्तमान में कोई खसरा/प्लॉट उपलब्ध नहीं है। कृपया पहले ज़मीन एंट्री करें।")
        else:
            available_plots = inv_df[pd.to_numeric(inv_df['available_area'], errors='coerce') > 0]['prop_id'].tolist()
            with st.form("sale_form", clear_on_submit=True):
                col_m, col_n = st.columns(2)
                with col_m:
                    cust_name = st.text_input("👤 क्रेता / ग्राहक का पूरा नाम")
                    cust_phone = st.text_input("📱 ग्राहक का मोबाइल नंबर")
                    sel_prop = st.selectbox("🎯 बिक्री हेतु खसरा / प्लॉट नंबर चुनें", available_plots)
                
                p_info = inv_df[inv_df['prop_id'] == sel_prop].iloc[0]
                with col_n:
                    st.info(f"📍 स्टॉक इन्फो: ग्राम-{p_info['village']} | उपलब्ध रकबा: {p_info['available_area']} Sq.Ft")
                    sell_area = st.number_input("बेचा जा रहा रकबा (Sq.Ft)", min_value=1.0, max_value=float(p_info['available_area']))
                    sell_rate = st.number_input("बिक्री दर (₹ प्रति Sq.Ft)", min_value=1.0)
                
                amt_received = st.number_input("प्राप्त राशि (एडवांस/नगद प्राप्त) (₹)", min_value=0.0)
                pay_method = st.selectbox("प्राप्ति माध्यम", ["नकद (Cash)", "बैंक ट्रांसफर", "चेक (Cheque)"])

                if st.form_submit_button("🧾 डिजिटल पक्का बिल एवं रसीद जनरेट करें"):
                    total_deal = sell_area * sell_rate
                    balance_from_cust = total_deal - amt_received
                    now = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    inv_df.loc[inv_df['prop_id'] == sel_prop, 'available_area'] = float(p_info['available_area']) - sell_area
                    
                    new_sale = pd.DataFrame([{"tx_date": now, "party_type": 'क्रेता (ग्राहक)', "party_name": cust_name, "party_phone": cust_phone, "prop_id": sel_prop, "deal_amount": total_deal, "amount_paid_received": amt_received, "balance_amount": balance_from_cust, "payment_mode": pay_method, "notes": f"प्लॉट आवंटन | ग्राम: {p_info['village']}, जिला: {p_info['district']}"}])
                    khata_updated = pd.concat([khata_df, new_sale], ignore_index=True)
                    
                    conn.update(worksheet="Inventory", data=inv_df)
                    conn.update(worksheet="KhataBook", data=khata_updated)
                    
                    st.markdown(f"""
                    <div style="border: 3px dashed #16A34A; padding: 20px; background-color: #F0FDF4; border-radius: 10px; font-family: monospace;">
                        <h3 style="text-align: center; color: #16A34A; margin: 0;">🔱 मां प्रॉपर्टी (Maa Property)</h3>
                        <p style="font-size:12px; text-align:center; color:#2563EB; margin:2px;">🌐 क्लाउड डिजिटल रसीद</p>
                        <hr>
                        <b>क्रेता ग्राहक :</b> {cust_name}<br>
                        <b>भूमि स्थान :</b> ग्राम- {p_info['village']}, तहसील- {p_info['tehsil']}, हल्का- {p_info['patwari_halka']}, जिला- {p_info['district']}<br>
                        <b>खसरा नंबर :</b> {sel_prop} | <b>एरिया:</b> {sell_area} Sq.Ft<br>
                        <hr>
                        <b>💸 कुल सौदा मूल्य :</b> ₹{total_deal:,.2f}<br>
                        <span style="color:green;"><b>🟢 प्राप्त राशि:</b> ₹{amt_received:,.2f}</span><br>
                        <span style="color:red;"><b>🔴 बकाया उधारी राशि :</b> ₹{balance_from_cust:,.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # 4. लाइव स्टॉक बही
    with menu[3]:
        st.markdown("### 📂 राष्ट्रीय रियल एस्टेट लाइव स्टॉक रजिस्ट्री")
        search = st.text_input("🔍 सुपर सर्च इंजन: खसरा, ग्राम, जिला, राज्य या नाम लिखकर खोजें")
        
        display_df = inv_df.copy()
        if search and not display_df.empty:
            display_df = display_df[
                display_df['prop_id'].astype(str).str.contains(search, case=False) | 
                display_df['village'].astype(str).str.contains(search, case=False) |
                display_df['district'].astype(str).str.contains(search, case=False) |
                display_df['state'].astype(str).str.contains(search, case=False)
            ]

        if not display_df.empty:
            for index, row in display_df.iterrows():
                st.markdown(f"""
                <div style="border: 1px solid #D1D5DB; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #FFFFFF;">
                    <h5 style="margin: 0; color: #1E3A8A;">📍 {row['state']} ➔ जिला: {row['district']} ➔ तहसील: {row['tehsil']}</h5>
                    <p style="margin: 5px 0 0 0; font-size: 13px; color: #4B5563;">
                        🏢 <b>RI मंडल:</b> {row['ri_circle']} | 🌾 <b>पटवारी हल्का:</b> {row['patwari_halka']} | 🏡 <b>ग्राम:</b> {row['village']}<br>
                        🆔 <b>खसरा नंबर:</b> {row['prop_id']} | 👤 <b>मूल भूमिस्वामी:</b> {row['seller_name']}<br>
                        📐 <b>कुल रकबा:</b> {row['total_area']} Sq.Ft | 🎯 <b>शेष उपलब्ध एरिया:</b> <span style="color:#16A34A; font-weight:bold;">{row['available_area']} Sq.Ft</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

    # 5. ऑल-इन-वन डिजिटल खता बुक
    with menu[4]:
        st.markdown("### 🧾 डिजिटल लेजर एवं उधारी खाता")
        p_search = st.text_input("👤 पक्षकार का नाम या मोबाइल नंबर लिखकर खाता खोजें")
        
        display_k = khata_df.copy()
        if p_search and not display_k.empty:
            display_k = display_k[display_k['party_name'].astype(str).str.contains(p_search, case=False) | display_k['party_phone'].astype(str).str.contains(p_search, case=False)]

        if not display_k.empty:
            st.dataframe(display_k, use_container_width=True, hide_index=True)

    if st.sidebar.button("🔴 ऐप सुरक्षित बंद करें (Logout)", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
  
