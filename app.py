import streamlit as st

st.set_page_config(
    page_title="BRSR Carbon Calculator",
    page_icon="🌱",
    layout="centered"
)

# Header
st.title("🌱 BRSR Carbon Footprint Calculator")
st.subheader("Free tool for Indian companies")
st.write("Calculate Scope 1 and Scope 2 emissions for BRSR Section C — Principle 6 reporting")
st.markdown("---")

# Company details
st.header("🏢 Company Details")
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Company Name", placeholder="Enter company name")
    reporting_year = st.selectbox("Reporting Year", 
                                   ["FY 2024-25", "FY 2023-24", "FY 2022-23"])
with col2:
    revenue = st.number_input("Annual Revenue (₹ Crores)", min_value=0.0)
    employees = st.number_input("Total Employees", min_value=0)

st.markdown("---")

# Scope 1
st.header("🏭 Scope 1 — Direct Emissions")
st.caption("Emissions from sources your company owns or controls directly")

col1, col2, col3 = st.columns(3)
with col1:
    diesel = st.number_input("Diesel (litres)", min_value=0.0,
                              help="Company vehicles, generators, equipment")
    lpg = st.number_input("LPG (kg)", min_value=0.0,
                           help="Canteen, heating, industrial processes")
with col2:
    petrol = st.number_input("Petrol (litres)", min_value=0.0,
                              help="Company owned cars and bikes")
    png = st.number_input("PNG / CNG (SCM)", min_value=0.0,
                           help="Piped natural gas consumption")
with col3:
    coal = st.number_input("Coal (tonnes)", min_value=0.0,
                            help="Boilers and industrial furnaces")
    furnace_oil = st.number_input("Furnace Oil (litres)", min_value=0.0,
                                   help="Industrial heating")

st.markdown("---")

# Scope 2
st.header("⚡ Scope 2 — Electricity Emissions")
st.caption("Emissions from purchased electricity — check your electricity bills")
electricity = st.number_input("Electricity consumed (kWh)", min_value=0.0,
                               help="Total units purchased from grid annually")

st.markdown("---")

# Calculate
calculate = st.button("🧮 Calculate Carbon Footprint", type="primary",
                       use_container_width=True)

if calculate:

    # Emission factors — India specific sources
    EF = {
        'diesel':      0.002680,   # tCO2e/litre — IPCC
        'petrol':      0.002310,   # tCO2e/litre — IPCC
        'lpg':         0.002980,   # tCO2e/kg — IPCC
        'png':         0.002020,   # tCO2e/SCM — IPCC
        'coal':        2.420000,   # tCO2e/tonne — IPCC
        'furnace_oil': 0.002960,   # tCO2e/litre — IPCC
        'electricity': 0.000820,   # tCO2e/kWh — CEA 2023
    }

    # Calculations
    s1_diesel      = diesel      * EF['diesel']
    s1_petrol      = petrol      * EF['petrol']
    s1_lpg         = lpg         * EF['lpg']
    s1_png         = png         * EF['png']
    s1_coal        = coal        * EF['coal']
    s1_furnace     = furnace_oil * EF['furnace_oil']
    total_scope1   = s1_diesel + s1_petrol + s1_lpg + s1_png + s1_coal + s1_furnace

    total_scope2   = electricity * EF['electricity']
    total          = total_scope1 + total_scope2

    # Intensities
    intensity_rev  = round(total / revenue, 4)   if revenue   > 0 else 0
    intensity_emp  = round(total / employees * 1000, 4) if employees > 0 else 0

    # Results
    st.markdown("---")
    st.header("📊 Your Results")

    name_display = company_name if company_name else "Your Company"
    st.success(f"Carbon footprint calculated for {name_display} — {reporting_year}")

    # 3 main metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("🏭 Scope 1", f"{round(total_scope1, 2)} tCO2e")
    c2.metric("⚡ Scope 2", f"{round(total_scope2, 2)} tCO2e")
    c3.metric("🌍 Total",   f"{round(total, 2)} tCO2e")

    st.markdown("---")

    # Scope 1 breakdown
    st.subheader("Scope 1 Breakdown by Source")
    sources = {
        "Diesel":      s1_diesel,
        "Petrol":      s1_petrol,
        "LPG":         s1_lpg,
        "PNG / CNG":   s1_png,
        "Coal":        s1_coal,
        "Furnace Oil": s1_furnace,
    }

    for source, value in sources.items():
        if value > 0:
            pct = round(value / total_scope1 * 100, 1) if total_scope1 > 0 else 0
            st.write(f"**{source}:** {round(value, 4)} tCO2e ({pct}%)")
            st.progress(pct / 100)

    st.markdown("---")

    # Intensity metrics
    if revenue > 0 or employees > 0:
        st.subheader("Emission Intensity Metrics")
        i1, i2 = st.columns(2)
        if revenue > 0:
            i1.metric("Per ₹ Crore Revenue",
                      f"{intensity_rev} tCO2e/Cr",
                      help="BRSR Essential Indicator — emission intensity")
        if employees > 0:
            i2.metric("Per 1000 Employees",
                      f"{intensity_emp} tCO2e",
                      help="Social intensity benchmark")

    st.markdown("---")

    # BRSR mapping
    st.subheader("📋 BRSR Filing Guide")
    st.info("""
**Where to report these numbers in your BRSR:**

✅ **Scope 1** → Section C, Principle 6, Essential Indicator 6(i)

✅ **Scope 2** → Section C, Principle 6, Essential Indicator 6(ii)

✅ **Total Scope 1 + 2** → Section C, Principle 6, Essential Indicator 6(iii)

✅ **Emission intensity** → Section C, Principle 6, Essential Indicator 6(iv)

**Methodology:** GHG Protocol Corporate Standard 2015

**Emission factors:** CEA 2023 (electricity) · IPCC AR6 (fuels)
    """)

    st.warning("""
⚠️ **Important:** This tool covers Scope 1 and Scope 2 only.
Scope 3 value chain emissions require additional data collection.
For BRSR Core assurance requirements please consult a certified ESG professional.
    """)

    # Download results as text
    result_text = f"""
BRSR CARBON FOOTPRINT CALCULATOR RESULTS
=========================================
Company: {name_display}
Reporting Year: {reporting_year}

SCOPE 1 EMISSIONS: {round(total_scope1, 2)} tCO2e
SCOPE 2 EMISSIONS: {round(total_scope2, 2)} tCO2e
TOTAL EMISSIONS:   {round(total, 2)} tCO2e

INTENSITY METRICS:
Per Crore Revenue: {intensity_rev} tCO2e/Cr
Per 1000 Employees: {intensity_emp} tCO2e

Methodology: GHG Protocol Corporate Standard
Electricity EF: 0.00082 tCO2e/kWh (CEA 2023)
=========================================
Generated by BRSR Carbon Calculator
Built by Your Name — ESG Data Analyst
    """

    st.download_button(
        label="📥 Download Results as Text File",
        data=result_text,
        file_name=f"BRSR_Carbon_Results_{name_display}.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:grey; font-size:12px;'>
Built by <b>Your Name</b> · Aspiring ESG Data Analyst<br>
Methodology: GHG Protocol Corporate Standard · CEA 2023 · IPCC AR6<br>
Free tool for Indian companies preparing BRSR Section C disclosures<br>
🔗 Connect on LinkedIn: Your LinkedIn URL
</div>
""", unsafe_allow_html=True)
