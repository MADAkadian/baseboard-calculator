import streamlit as st
import datetime

st.set_page_config(page_title="Painting Estimate Tool", layout="wide")

# Pricing
BASEBOARD_RATES = {
    'light': 1.00,
    'medium': 1.50,
    'heavy': 2.00
}

SQUAREFOOT_RATE = 1.50
DOOR_COST = 50
FRAME_COST = 50

PREP_DESCRIPTIONS = {
    "Light – 2 coats, no patching": "light",
    "Medium – Patch walls + 2 coats": "medium",
    "Heavy – Patch, prime + 2 coats": "heavy"
}

# Sidebar – Client Info
st.sidebar.title("🧾 Client Information")
client_name = st.sidebar.text_input("Client Name")
project_name = st.sidebar.text_input("Project Name / Address")
estimate_date = st.sidebar.date_input("Estimate Date", value=datetime.date.today())

# Header
st.markdown("<h1 style='color:#3366cc;'>Couleurs Vraies Peinture</h1>", unsafe_allow_html=True)
st.markdown("**Professional Painting Estimate Tool**")
st.markdown("---")

col1, col2 = st.columns(2)

# Baseboard Estimate
with col1:
    st.subheader("📏 Baseboard Estimate")
    linear_feet = st.number_input("Linear Feet of Baseboard", min_value=1, value=100)
    prep_label_baseboard = st.selectbox("Prep Level", list(PREP_DESCRIPTIONS.keys()), key="prep_baseboard")
    prep_key_baseboard = PREP_DESCRIPTIONS[prep_label_baseboard]

    if st.button("Calculate Baseboard Estimate"):
        base_price = linear_feet * BASEBOARD_RATES[prep_key_baseboard]
        materials_fee = base_price * 0.12
        total = base_price + materials_fee

        st.markdown("#### 💵 Breakdown")
        st.write(f"**Base Price:** ${base_price:.2f}")
        st.write(f"**Materials Fee (12%):** ${materials_fee:.2f}")
        st.write(f"**Total Estimate:** ${total:.2f}")

        quote = f"""
Couleurs Vraies Peinture

Client: {client_name}
Project: {project_name}
Date: {estimate_date.strftime('%Y-%m-%d')}

--- Baseboard Estimate ---
Linear Feet: {linear_feet}
Prep Level: {prep_label_baseboard}
Base Price: ${base_price:.2f}
Materials Fee (12%): ${materials_fee:.2f}
Total Price: ${total:.2f}

Merci pour votre confiance! / Thank you for your trust!
"""
        st.download_button("📄 Download Baseboard Quote", quote, file_name="baseboard_quote.txt")

# House Estimate
with col2:
    st.subheader("🏠 House Estimate")
    walls = st.number_input("Walls (sqft)", min_value=0)
    ceilings = st.number_input("Ceilings (sqft)", min_value=0)
    doors = st.number_input("Number of Doors", min_value=0, step=1)
    frames = st.number_input("Number of Frames", min_value=0, step=1)
    prep_label_house = st.selectbox("Prep Level", list(PREP_DESCRIPTIONS.keys()), key="prep_house")
    prep_key_house = PREP_DESCRIPTIONS[prep_label_house]

    if st.button("Calculate House Estimate"):
        surface_total = (walls + ceilings) * SQUAREFOOT_RATE
        door_total = doors * DOOR_COST
        frame_total = frames * FRAME_COST
        subtotal = surface_total + door_total + frame_total
        materials_fee = subtotal * 0.12
        total = subtotal + materials_fee

        st.markdown("#### 💵 Breakdown")
        st.write(f"**Walls & Ceilings:** ${surface_total:.2f}")
        st.write(f"**Doors:** ${door_total:.2f}")
        st.write(f"**Frames:** ${frame_total:.2f}")
        st.write(f"**Materials Fee (12%):** ${materials_fee:.2f}")
        st.write(f"**Total Estimate:** ${total:.2f}")

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

Walls/Ceilings Total: ${surface_total:.2f}
Doors: ${door_total:.2f}
Frames: ${frame_total:.2f}
Materials Fee (12%): ${materials_fee:.2f}
Total Price: ${total:.2f}

Merci pour votre confiance! / Thank you for your trust!
"""
        st.download_button("📄 Download House Quote", house_quote, file_name="house_quote.txt")


