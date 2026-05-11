import streamlit as st

# إعداد الواجهة والسمة الغامقة
st.set_page_config(page_title="Smart Medical Hub PRO", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput input { background-color: #262730; color: white; border-radius: 10px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #262730; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; height: 50px; }
    .report-card { background-color: #1e1e26; padding: 15px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .sugar-card { background-color: #1e1e26; padding: 15px; border-radius: 15px; border-left: 5px solid #00d1b2; margin-bottom: 10px; }
    .critical { color: #ff0000; font-weight: bold; background-color: #3b0000; padding: 5px; border-radius: 5px; }
    .high { color: #ffa500; }
    .low { color: #00bfff; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 المحلل الطبي الذكي - الإصدار الاحترافي")
st.write("---")

# --- مدخلات المريض ---
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    age = st.number_input("العمر", min_value=0, max_value=110, value=25)
with col_info2:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
with col_info3:
    user_status = st.selectbox("حالة السكر المعروفة", ["سليم (Normal)", "مصاب بالسكر (Diabetic)", "متابعة (Monitoring)"])

st.write("---")

# --- إدخال البيانات ---
col_cbc, col_sugar = st.columns(2)

with col_cbc:
    st.subheader("🩸 تحليلات الدم (CBC)")
    hgb = st.number_input("HGB (الهيموجلوبين)", value=0.0, step=0.1)
    hct = st.number_input("HCT (الهيماتوكريت %)", value=0.0, step=0.1)
    wbc = st.number_input("WBC (البيضاء)", value=0.0, step=0.1)
    plt = st.number_input("PLT (الصفائح)", value=0.0, step=1.0)
    rbc = st.number_input("RBC (الحمراء)", value=0.0, step=0.01)

with col_sugar:
    st.subheader("🍬 تحليلات السكر")
    hba1c = st.number_input("HbA1c (التراكمي %)", value=0.0, step=0.1)
    sugar_type = st.radio("نوع الفحص اليومي:", ["صائم (FBS)", "عشوائي (RBS)"])
    sugar_val = st.number_input(f"قيمة الـ {sugar_type}", value=0.0, step=1.0)

# --- محرك التحليل المتطور ---
def run_analysis():
    reports = {"cbc": [], "sugar": [], "alerts": []}

    # 1. تحليل الهيموجلوبين (HGB)
    if hgb > 0:
        hgb_min = 13.5 if gender == "ذكر" else 12.0
        if age < 12: hgb_min = 11.0
        if hgb < 7.0: reports["cbc"].append(f"<span class='critical'>CRITICAL LOW:</span> الهيموجلوبين منخفض جداً ({hgb}). استشر طبيباً فوراً.")
        elif hgb < hgb_min: reports["cbc"].append(f"<span class='low'>LOW:</span> الهيموجلوبين منخفض ({hgb}).")
        elif hgb > 18.0: reports["cbc"].append(f"<span class='critical'>CRITICAL HIGH:</span> الهيموجلوبين مرتفع جداً ({hgb}).")
        elif hgb > 17.5: reports["cbc"].append(f"<span class='high'>HIGH:</span> الهيموجلوبين مرتفع ({hgb}).")

    # 2. تحليل كريات الدم البيضاء (WBC)
    if wbc > 0:
        if wbc > 20.0: reports["cbc"].append(f"<span class='critical'>CRITICAL HIGH:</span> كريات البيضاء مرتفعة جداً ({wbc}).")
        elif wbc > 11.0: reports["cbc"].append(f"<span class='high'>HIGH:</span> ارتفاع في كريات البيضاء ({wbc}).")
        elif wbc < 4.0: reports["cbc"].append(f"<span class='low'>LOW:</span> انخفاض في كريات البيضاء ({wbc}).")

    # 3. تحليل الصفائح (PLT)
    if plt > 0:
        if plt < 50: reports["cbc"].append(f"<span class='critical'>CRITICAL LOW:</span> الصفائح منخفضة بشكل خطير ({plt}).")
        elif plt < 150: reports["cbc"].append(f"<span class='low'>LOW:</span> انخفاض الصفائح ({plt}).")
        elif plt > 450: reports["cbc"].append(f"<span class='high'>HIGH:</span> ارتفاع الصفائح ({plt}).")

    # 4. تحليل السكر (Diabetes)
    if hba1c > 0:
        if hba1c >= 8.0: reports["sugar"].append(f"<span class='critical'>UNCONTROLLED:</span> التراكمي مرتفع جداً ({hba1c}%).")
        elif hba1c >= 6.5: reports["sugar"].append(f"<span class='high'>DIABETIC RANGE:</span> التراكمي في نطاق السكر ({hba1c}%).")
        elif 5.7 <= hba1c < 6.5: reports["sugar"].append(f"<span class='high'>PRE-DIABETIC:</span> مرحلة ما قبل السكر ({hba1c}%).")

    if sugar_val > 0:
        if sugar_val < 60: reports["sugar"].append(f"<span class='critical'>CRITICAL LOW:</span> هبوط حاد في السكر ({sugar_val}).")
        elif sugar_type == "صائم (FBS)" and sugar_val >= 126: reports["sugar"].append(f"<span class='high'>HIGH:</span> السكر الصائم مرتفع ({sugar_val}).")
        elif sugar_type == "عشوائي (RBS)" and sugar_val >= 200: reports["sugar"].append(f"<span class='high'>HIGH:</span> السكر العشوائي مرتفع ({sugar_val}).")

    # 5. كشف التناقض وعطل الجهاز
    if hgb > 0 and hct > 0:
        if abs((hgb * 3) - hct) > 3.5:
            reports["alerts"].append("🚨 **عطل محتمل في الجهاز:** تناقض بين HGB و HCT. يرجى إعادة المعايرة.")

    if hba1c > 0 and sugar_val > 0:
        if (hba1c < 5.7 and sugar_val > 180) or (hba1c > 8.5 and sugar_val < 110):
            reports["alerts"].append("⚠️ **تناقض في النتائج:** التراكمي لا يتفق مع السكر اليومي. أعد التيست ليتم التأكد.")

    return reports

# --- العرض النهائي ---
if st.button("بدء التحليل الفوري"):
    analysis = run_analysis()
    
    if analysis["alerts"]:
        for a in analysis["alerts"]: st.error(a)
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        if analysis["cbc"]:
            st.markdown('<div class="report-card"><h4>نتائج الدم (CBC)</h4>', unsafe_allow_html=True)
            for r in analysis["cbc"]: st.markdown(f"• {r}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res2:
        if analysis["sugar"]:
            st.markdown('<div class="sugar-card"><h4>نتائج السكر</h4>', unsafe_allow_html=True)
            for s in analysis["sugar"]: st.markdown(f"• {s}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not analysis["cbc"] and not analysis["sugar"] and not analysis["alerts"]:
        st.success("✅ جميع النتائج المدخلة طبيعية جداً!")
