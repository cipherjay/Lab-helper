import streamlit as st

# إعداد الواجهة والسمة الغامقة
st.set_page_config(page_title="Smart Medical Hub", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput input { background-color: #262730; color: white; border-radius: 10px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #262730; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; border: none; height: 50px; }
    .report-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .sugar-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #00d1b2; margin-bottom: 10px; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 المحلل الطبي الذكي")
st.write("---")

# --- مدخلات المريض ---
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    age = st.number_input("العمر", min_value=0, max_value=110, value=25)
with col_info2:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
with col_info3:
    user_status = st.selectbox("حالة السكر", ["سليم (Normal)", "مصاب بالسكر (Diabetic)", "متابعة (Monitoring)"])

st.write("---")

# --- إدخال البيانات ---
col_cbc, col_sugar = st.columns(2)

with col_cbc:
    st.subheader("🩸 تحليلات الدم (CBC)")
    hgb = st.number_input("HGB (الهيموجلوبين)", value=0.0)
    hct = st.number_input("HCT (الهيماتوكريت %)", value=0.0)
    wbc = st.number_input("WBC (البيضاء)", value=0.0)
    plt = st.number_input("PLT (الصفائح)", value=0.0)
    rbc = st.number_input("RBC (الحمراء)", value=0.0)
    mchc = st.number_input("MCHC", value=0.0)

with col_sugar:
    st.subheader("🍬 تحليلات السكر")
    hba1c = st.number_input("HbA1c (التراكمي %)", value=0.0)
    sugar_type = st.radio("نوع الفحص المرفق:", ["صائم (FBS)", "عشوائي (RBS)"])
    sugar_val = st.number_input(f"قيمة الـ {sugar_type}", value=0.0)

# --- محرك التحليل ---
def run_analysis():
    cbc_reports = []
    sugar_reports = []
    alerts = []

    # تحليل CBC مرن
    if hgb > 0:
        hgb_min = 13.5 if gender == "ذكر" else 12.0
        if age < 12: hgb_min = 11.0
        if hgb < hgb_min: cbc_reports.append(f"🔴 انخفاض الهيموجلوبين ({hgb})")
        elif hgb > 17.5: cbc_reports.append(f"🟠 ارتفاع الهيموجلوبين ({hgb})")

    if hgb > 0 and hct > 0:
        if abs((hgb * 3) - hct) > 3.5:
            alerts.append("🚨 عطل محتمل في الجهاز: الهيموجلوبين لا يتناسق مع الهيماتوكريت.")

    if wbc > 11.0: cbc_reports.append(f"🟠 ارتفاع كريات الدم البيضاء ({wbc})")
    if plt > 450: cbc_reports.append(f"🟠 ارتفاع الصفائح ({plt})")

    # تحليل السكر والتناقض
    if hba1c > 0:
        if hba1c >= 6.5: sugar_reports.append(f"🔴 التراكمي مرتفع ({hba1c}%)")
        elif 5.7 <= hba1c < 6.5: sugar_reports.append(f"🟠 مرحلة ما قبل السكر ({hba1c}%)")
        else: sugar_reports.append(f"✅ التراكمي طبيعي ({hba1c}%)")

    if sugar_val > 0:
        if sugar_type == "صائم (FBS)" and sugar_val >= 126: sugar_reports.append(f"🔴 السكر الصائم مرتفع ({sugar_val})")
        elif sugar_type == "عشوائي (RBS)" and sugar_val >= 200: sugar_reports.append(f"🔴 السكر العشوائي مرتفع ({sugar_val})")

    if hba1c > 0 and sugar_val > 0:
        if (hba1c < 5.7 and sugar_val > 180) or (hba1c > 8.5 and sugar_val < 110):
            alerts.append("⚠️ تناقض في النتائج: التراكمي لا يتفق مع السكر اليومي. أعد التيست ليتم التأكد.")

    return cbc_reports, sugar_reports, alerts

# --- العرض ---
if st.button("تحليل النتائج الآن"):
    c_res, s_res, alts = run_analysis()
    
    if alts:
        for a in alts: st.error(a)
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        if c_res:
            st.markdown('<div class="report-card"><h4>نتائج الدم</h4>', unsafe_allow_html=True)
            for r in c_res: st.write(r)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res2:
        if s_res:
            st.markdown('<div class="sugar-card"><h4>نتائج السكر</h4>', unsafe_allow_html=True)
            for s in s_res: st.write(s)
            st.markdown('</div>', unsafe_allow_html=True)

    if not c_res and not s_res and not alts:
        st.info("الرجاء إدخال القيم أولاً.")
