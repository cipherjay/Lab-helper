import streamlit as st

# إعداد الواجهة والسمة الغامقة
st.set_page_config(page_title="Ultra Medical Analyzer", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput input { background-color: #262730; color: white; border-radius: 10px; }
    .stSelectbox div[data-baseweb="select"] { background-color: #262730; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; height: 50px; border: none; }
    .report-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .sugar-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #00d1b2; margin-bottom: 10px; }
    h1, h2, h3 { color: #ff4b4b; text-align: center; }
    .critical { color: #ff4b4b; font-weight: bold; text-decoration: underline; }
    .high { color: #ffa500; font-weight: bold; }
    .low { color: #00bfff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 المحلل الطبي الشامل والمطور")
st.write(f"<div style='text-align:center; color:#007BFF;'>Coder: Jk & Gemini Pro</div>", unsafe_allow_html=True)

# --- بيانات المريض ---
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1: age = st.number_input("العمر", min_value=0, value=25)
with col_p2: gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
with col_p3: status = st.selectbox("حالة السكر", ["سليم", "مصاب بالسكر", "متابعة"])

st.divider()

# --- إدخال البيانات (CBC + سكر + أنيميا) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🩸 تحليلات الدم (CBC & Anemia)")
    hb = st.number_input("HGB (الهيموجلوبين)", value=0.0)
    wbc = st.number_input("WBC (كريات البيضاء)", value=0.0)
    hct = st.number_input("HCT (الهيماتوكريت %)", value=0.0)
    mcv = st.number_input("MCV (حجم الخلية)", value=0.0)
    plt = st.number_input("PLT (الصفائح)", value=0.0)
    ferritin = st.number_input("Ferritin (مخزون الحديد)", value=0.0)
    morphology = st.selectbox("شكل الخلايا:", ["None", "Microcytic", "Macrocytic", "Target Cells", "Sickle Cells"])

with col_right:
    st.subheader("🍬 تحليلات السكر")
    hba1c = st.number_input("HbA1c (التراكمي %)", value=0.0)
    sugar_type = st.radio("نوع الفحص:", ["صائم (FBS)", "عشوائي (RBS)"])
    sugar_val = st.number_input(f"قيمة {sugar_type}", value=0.0)

# --- محرك التحليل الذكي ---
def run_comprehensive_analysis():
    cbc_out = []
    sugar_out = []
    alerts = []

    # 1. تحليل كريات الدم البيضاء (WBC) - الميزة الجديدة
    if wbc > 0:
        if wbc > 30.0:
            cbc_out.append(f"<span class='critical'>CRITICAL HIGH:</span> ارتفاع حاد جداً ({wbc}). قد يدل على عدوى شديدة أو استجابة نخاعية قوية. استشر طبيباً فوراً.")
        elif wbc > 11.0:
            cbc_out.append(f"<span class='high'>HIGH:</span> ارتفاع ({wbc}). يدل عادةً على وجود التهاب أو عدوى بكتيرية، أو إجهاد بدني شديد.")
        elif wbc < 4.0:
            cbc_out.append(f"<span class='low'>LOW:</span> انخفاض ({wbc}). قد يدل على نقص المناعة، عدوى فيروسية، أو تأثر نخاع العظم.")

    # 2. تحليل الأنيميا والهيموجلوبين
    hgb_min = 13.5 if gender == "ذكر" else 12.0
    if age < 12: hgb_min = 11.0
    
    if hb > 0:
        if hb < 7.0: cbc_out.append(f"<span class='critical'>CRITICAL LOW:</span> فقر دم حاد جداً ({hb}). يحتاج تدخل طبي.")
        elif hb < hgb_min:
            diag = "فقر دم (Anemia)"
            if mcv > 0 and mcv < 80:
                diag = "فقر دم صغير الخلايا (نقص حديد أو ثلاسيميا)"
                if ferritin > 0 and ferritin < 15: diag = "أنيميا نقص الحديد المؤكدة"
            elif mcv > 100: diag = "فقر دم كبير الخلايا (نقص B12 أو فوليك)"
            cbc_out.append(f"🔴 {diag} ({hb})")
        
        # كشف عطل الجهاز
        if hct > 0 and abs((hb * 3) - hct) > 3.5:
            alerts.append("🚨 عطل محتمل في الجهاز: الهيموجلوبين لا يتوافق مع الهيماتوكريت.")

    # 3. تحليل الصفائح
    if plt > 0:
        if plt < 50: cbc_out.append(f"<span class='critical'>CRITICAL PLT:</span> نقص حاد في الصفائح ({plt}). خطر نزيف.")
        elif plt > 450: cbc_out.append(f"<span class='high'>HIGH PLT:</span> ارتفاع في الصفائح ({plt}).")

    # 4. تحليل السكر والتناقض
    if hba1c > 0:
        if hba1c >= 6.5: sugar_out.append(f"🔴 السكر التراكمي مرتفع ({hba1c}%) - نطاق الإصابة.")
        elif 5.7 <= hba1c < 6.5: sugar_out.append(f"🟠 مرحلة ما قبل السكر ({hba1c}%)")
    
    if hba1c > 0 and sugar_val > 0:
        if (hba1c < 5.7 and sugar_val > 180) or (hba1c > 8.5 and sugar_val < 110):
            alerts.append("⚠️ تناقض: التراكمي لا يتفق مع السكر اليومي. أعد التحليل للتأكد.")

    return cbc_out, sugar_out, alerts

# --- العرض ---
if st.button("🔍 تحليل كافة البيانات"):
    c_results, s_results, errs = run_comprehensive_analysis()
    
    if errs:
        for e in errs: st.error(e)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if c_results:
            st.markdown('<div class="report-card"><h4>نتائج الدم (CBC & WBC)</h4>', unsafe_allow_html=True)
            for res in c_results: st.markdown(f"• {res}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_r2:
        if s_results:
            st.markdown('<div class="sugar-card"><h4>نتائج السكر</h4>', unsafe_allow_html=True)
            for s in s_results: st.markdown(f"• {s}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if not c_results and not s_results and not errs:
        st.success("✅ جميع البيانات المدخلة طبيعية.")
