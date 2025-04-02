import streamlit as st
import datetime
import math

st.set_page_config(page_title="Painting Estimate Tool", layout="wide")

# --- Pricing ---
BASEBOARD_RATES = {
    'light': 1.00,
    'medium': 1.50,
    'heavy': 2.00
}

SQUAREFOOT_RATE = 1.50
DOOR_COST = 50
FRAME_COST = 50
PAINT_COVERAGE_SQFT = 400  # Updated from 350
PAINT_COST_PER_GALLON = 70

# --- Prep Level Descriptions ---
BASEBOARD_PREP_OPTIONS = {
    "Light – 1 coat of paint": "light",
    "Medium – 2 coats of paint": "medium",
    "Heavy – Prime + 2 coats, fill holes & sand": "heavy"
}

HOUSE_PREP_OPTIONS = {
    "Light – 2 coats, no patching": {"key": "light", "coats": 2},
    "Medium – Patch walls + 2 coats": {"key": "medium", "coats": 2},
    "Heavy – Patch, prime + 2 coats": {"key": "heavy", "coats": 3}
}

# --- Sidebar: Client Info ---
st.sidebar.title("🧾 Client Information")
client_name = st.sidebar.text_input("Client Name")
project_name = st.sidebar.text_input("Project Name / Address")
estimate_date = st.sidebar.date_input("Estimate Date", value=datetime.date.today())

# --- Main Header ---
st.markdown("<h1 style='color:#3366cc;'>Couleurs Vraies Peinture</h1>", unsafe_allow_html=True)
st.markdown("**Professional Painting Estimate Tool**")
st.markdown("---")

# --- Two Columns ---
col1, col2 = st.columns(2)

# ========================
# 🟦 Baseboard Estimate
# ========================
with col1:
    st.subheader("📏 Baseboard Estimate")
    linear_feet = st.number_input("Linear Feet of Baseboard", min_value=1, value=100)
    prep_label_base = st.selectbox("Prep Level (Baseboard)", list(BASEBOARD_PREP_OPTIONS.keys()))
    prep_key_base = BASEBOARD_PREP_OPTIONS[prep_label_base]

    if st.button("Calculate Baseboard Estimate"):
        base_price = linear_feet * BASEBOARD_RATES[prep_key_base]
        materials_fee = base_price * 0.12
        total = base_price + materials_fee

        st.markdown("#### 💵 Breakdown")
        st.write(f"**Base Price:** ${base_price:.2f}")
        st.write(f"**Materials Fee (12%):** ${materials_fee:.2f}")
        st.write(f"**Total Estimate:** ${total:.2f}")

        baseboard_text = f"""
Couleurs Vraies Peinture

Client: {client_name}
Project: {project_name}
Date: {estimate_date.strftime('%Y-%m-%d')}

--- Baseboard Estimate ---
Linear Feet: {linear_feet}
Prep Level: {prep_label_base}
Base Price: ${base_price:.2f}
Materials Fee (12%): ${materials_fee:.2f}
Total Price: ${total:.2f}

Merci pour votre confiance! / Thank you for your trust!
"""
        st.download_button("📄 Download Baseboard Quote", baseboard_text, file_name="baseboard_quote.txt")

# ========================
# 🟨 House Estimate
# ========================
with col2:
    st.subheader("🏠 House Estimate")
    walls = st.number_input("Walls (sqft)", min_value=0)
    ceilings = st.number_input("Ceilings (sqft)", min_value=0)
    doors = st.number_input("Number of Doors", min_value=0, step=1)
    frames = st.number_input("Number of Frames", min_value=0, step=1)
    prep_label_house = st.selectbox("Prep Level (House)", list(HOUSE_PREP_OPTIONS.keys()))
    prep_details = HOUSE_PREP_OPTIONS[prep_label_house]
    coats = prep_details["coats"]

    if st.button("Calculate House Estimate"):
        area_total = walls + ceilings
        surface_price = area_total * SQUAREFOOT_RATE
        door_total = doors * DOOR_COST
        frame_total = frames * FRAME_COST

        gallons_needed = math.ceil((area_total * coats) / PAINT_COVERAGE_SQFT)
        paint_cost = gallons_needed * PAINT_COST_PER_GALLON

        total_price = surface_price + door_total + frame_total + paint_cost

        st.markdown("#### 💵 Breakdown")
        st.write(f"**Walls & Ceilings (labor):** ${surface_price:.2f}")
        st.write(f"**Doors:** ${door_total:.2f}")
        st.write(f"**Frames:** ${frame_total:.2f}")
        st.write(f"**Paint Needed:** {gallons_needed} gallons")
        st.write(f"**Paint Cost (@ ${PAINT_COST_PER_GALLON}/gallon):** ${paint_cost:.2f}")
        st.write(f"**Total Estimate:** ${total_price:.2f}")

        house_quote = f"""
Couleurs Vraies Peinture

Client: {client_name}
Project: {project_name}
Date: {estimate_date.strftime('%Y-%m-%d')}

--- House Painting Estimate ---
Walls SqFt: {walls}
Ceilings SqFt: {ceilings}
Doors: {doors}
Frames: {frames}
Prep Level: {prep_label_house}

Labor (Walls/Ceilings): ${surface_price:.2f}
Doors: ${door_total:.2f}
Frames: ${frame_total:.2f}
Paint Needed: {gallons_needed} gallons
Paint Cost: ${paint_cost:.2f}
Total Price: ${total_price:.2f}

Merci pour votre confiance! / Thank you for your trust!
"""
        st.download_button("📄 Download House Quote", house_quote, file_name="house_quote.txt")
