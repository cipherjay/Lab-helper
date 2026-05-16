import streamlit as st

# 1. إعدادات الصفحة والواجهة الاحترافية
st.set_page_config(page_title="Pro Medical Analyzer & Calculator", page_icon="🔬", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stNumberInput input { background-color: #262730; color: white; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; font-weight: bold; height: 50px; border: none; }
    .report-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .sugar-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #00d1b2; margin-bottom: 10px; }
    .lipid-card { background-color: #1e1e26; padding: 20px; border-radius: 15px; border-left: 5px solid #ffaa00; margin-bottom: 10px; }
    .critical-text { color: #ff4b4b; font-weight: bold; text-decoration: underline; }
    h1, h2, h3, h4 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 المحلل الطبي الشامل وحاسبة الدهون الذكية")
st.write(f"<div style='text-align:center; color:#007BFF; font-weight:bold;'>Coder: Jk & Gemini</div>", unsafe_allow_html=True)

# --- 2. البيانات الأساسية للمريض ---
st.divider()
c1, c2 = st.columns(2)
with c1: age = st.number_input("العمر (سنة)", min_value=0, value=25)
with c2: gender = st.selectbox("الجنس", ["ذكر", "أنثى"])

# --- 3. إدخال البيانات الطبية (تقسيم الشاشة إلى 3 أعمدة) ---
st.divider()
col_left, col_mid, col_right = st.columns(3)

with col_left:
    st.subheader("🩸 صورة الدم والأنيميا (CBC)")
    hb = st.number_input("HGB (الهيموجلوبين)", value=0.0, step=0.1)
    hct = st.number_input("HCT (الهيماتوكريت %)", value=0.0, step=0.1)
    wbc = st.number_input("WBC (كريات البيضاء)", value=0.0, step=0.1)
    mcv = st.number_input("MCV (حجم الكرية)", value=0.0, step=0.1)
    plt = st.number_input("PLT (الصفائح)", value=0.0, step=1.0)
    ferritin = st.number_input("Ferritin (مخزون الحديد)", value=0.0, step=1.0)

with col_mid:
    st.subheader("🍬 تحليلات السكر")
    hba1c = st.number_input("HbA1c (السكر التراكمي %)", value=0.0, step=0.1)
    sugar_val = st.number_input("قيمة السكر (الحالية)", value=0.0, step=1.0)

with col_right:
    st.subheader("🧪 حاسبة الدهون الذكية (Lipids)")
    total_chol = st.number_input("Total Cholesterol (الكوليسترول الكلي)", value=0.0, step=1.0)
    triglycerides = st.number_input("Triglycerides (الدهون الثلاثية)", value=0.0, step=1.0)
    hdl = st.number_input("HDL (الكوليسترول النافع)", value=0.0, step=1.0)

# --- 4. محرك التحليل والذكاء البرمجي ---
def start_analysis():
    cbc_res = []
    sugar_res = []
    lipid_res = []
    alerts = []

    # أ) حاسبة الدهون (LDL Calculation)
    if total_chol > 0 and hdl > 0 and triglycerides > 0:
        # معادلة فريدوالد لحساب LDL
        calculated_ldl = total_chol - hdl - (triglycerides / 5)
        
        lipid_res.append(f"Calculated LDL (الكوليسترول الضار المحسوب): **{calculated_ldl:.1f} mg/dL**")
        
        # تقييم النتيجة المحسوبة للـ LDL
        if calculated_ldl >= 160:
            lipid_res.append("🔴 LDL مرتفع جداً، يرجى مراجعة نظامك الغذائي واستشارة الطبيب.")
        elif 100 <= calculated_ldl < 160:
            lipid_res.append("🟠 LDL في النطاق الحدودي المرتفع، يرجى المتابعة والحذر.")
        else:
            lipid_res.append("✅ LDL في النطاق الطبيعي الممتاز.")
            
        # تنبيه طبي بخصوص الدهون الثلاثية العالية لأنها تؤثر على دقة المعادلة
        if triglycerides > 400:
            alerts.append("⚠️ **تنبيه الدهون:** الدهون الثلاثية أعلى من 400، معادلة الحساب قد تكون غير دقيقة في هذه الحالة ويفضل الفحص المباشر للـ LDL.")

    # ب) منطق السكر والمطابقة (تنبيه إعادة الفحص)
    if hba1c > 0 and sugar_val > 0:
        if (hba1c < 5.7 and sugar_val > 180) or (hba1c > 8.5 and sugar_val < 110):
            alerts.append("🚨 **غلط بالنتيجتين ما تتوافق:** التراكمي لا يتناسب مع السكر الحالي، يرجى إعادة التيست ليتم التأكد.")
        
        if hba1c >= 6.5 or sugar_val >= 200:
            sugar_res.append("🔴 النتيجة تشير إلى وجود سكر.")
        elif 5.7 <= hba1c < 6.5 or (100 <= sugar_val < 200):
            sugar_res.append("🟠 النتيجة في حدود السكر (مرحلة ما قبل السكر) - يرجو المتابعة.")
        else:
            sugar_res.append("✅ نتائج السكر طبيعية.")

    # ج) تحليل كريات الدم البيضاء (WBC)
    if wbc > 0:
        if wbc > 11.0:
            cbc_res.append(f"🟠 ارتفاع WBC ({wbc}): يدل على وجود التهاب أو عدوى بكتيرية.")
        elif wbc < 4.0:
            cbc_res.append(f"🔴 انخفاض WBC ({wbc}): يدل على نقص مناعة أو عدوى فيروسية.")

    # د) تحليل الأنيميا والهيموجلوبين
    hgb_min = 13.5 if gender == "ذكر" else 12.0
    if age < 12: hgb_min = 11.0
    
    if hb > 0:
        if hb < 7.0:
            cbc_res.append(f"<span class='critical-text'>CRITICAL:</span> فقر دم حاد جداً ({hb}) يحتاج نقل دم فوراً.")
        elif hb < hgb_min:
            diagnosis = "فقر دم (Anemia)"
            if mcv > 0 and mcv < 80:
                diagnosis = "أنيميا نقص الحديد (صغيرة الخلايا)"
                if ferritin > 0 and ferritin < 15: diagnosis = "أنيميا نقص الحديد المؤكدة"
            elif mcv > 100:
                diagnosis = "أنيميا نقص فيتامينات B12 أو فوليك (كبيرة الخلايا)"
            cbc_res.append(f"🔴 {diagnosis} ({hb})")

    # هـ) كشف أخطاء الجهاز (Rule of Three)
    if hb > 0 and hct > 0:
        if abs((hb * 3) - hct) > 3.5:
            alerts.append("⚠️ **خطأ في النتيجة:** الهيموجلوبين لا يتوافق مع الهيماتوكريت (عطل محتمل في الجهاز).")

    return cbc_res, sugar_res, lipid_res, alerts

# --- 5. زر العرض ومعالجة النتائج ---
if st.button("🔍 تحليل كافة النتائج وحساب الدهون"):
    c_out, s_out, l_out, a_out = start_analysis()
    
    # عرض التنبيهات والأخطاء أولاً
    if a_out:
        for a in a_out: st.error(a)
    
    # عرض التقارير في 3 أعمدة متناسقة
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        if c_out:
            st.markdown('<div class="report-card"><h4>🩸 تقرير الدم والأنيميا</h4>', unsafe_allow_html=True)
            for c in c_out: st.markdown(f"• {c}", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with col_res2:
        if s_out:
            st.markdown('<div class="sugar-card"><h4>🍬 تقرير السكر</h4>', unsafe_allow_html=True)
            for s in s_out: st.write(s)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_res3:
        if l_out:
            st.markdown('<div class="lipid-card"><h4>🧪 تقرير حاسبة الدهون</h4>', unsafe_allow_html=True)
            for l in l_out: st.write(l)
            st.markdown('</div>', unsafe_allow_html=True)

    if not c_out and not s_out and not l_out and not a_out:
        st.info("يرجى إدخال قيم في الخانات أعلاه لبدء التحليل والحساب.")

st.divider()
st.caption("ملاحظة: البرنامج مرن ويتجاهل الخانات الفارغة تماماً ويقوم بالعمليات الحسابية والتحليلية بناءً على ما تدخل فقط.")
