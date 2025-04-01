import streamlit as st

def calculate_baseboard_price(linear_feet, prep_level, add_caulk=False, add_sanding=False, add_quarter_round=False):
    base_rates = {
        'light': 1.25,
        'medium': 2.00,
        'heavy': 3.00
    }

    if prep_level not in base_rates:
        raise ValueError("Invalid prep level. Choose from: 'light', 'medium', 'heavy'")

    base_price = linear_feet * base_rates[prep_level]
    caulk_price = 0.25 * linear_feet if add_caulk else 0
    sanding_price = 0.50 * linear_feet if add_sanding else 0
    quarter_round_price = 0.75 * linear_feet if add_quarter_round else 0

    subtotal = base_price + caulk_price + sanding_price + quarter_round_price
    materials_fee = subtotal * 0.12
    total_price = subtotal + materials_fee

    return {
        'Base Price': round(base_price, 2),
        'Caulking Add-on': round(caulk_price, 2),
        'Sanding Add-on': round(sanding_price, 2),
        'Quarter Round Add-on': round(quarter_round_price, 2),
        'Materials Fee (12%)': round(materials_fee, 2),
        'Total Price': round(total_price, 2)
    }

# Streamlit mobile UI
st.set_page_config(page_title="Baseboard Pricing Calculator", layout="centered")
st.title("🎨 Baseboard Pricing Calculator")

linear_feet = st.number_input("Total Linear Feet of Baseboard:", min_value=1, value=100)
prep_level = st.selectbox("Prep Level:", ["light", "medium", "heavy"])

add_caulk = st.checkbox("Add Caulking")
add_sanding = st.checkbox("Add Sanding")
add_quarter_round = st.checkbox("Add Quarter Round Painting")

if st.button("Calculate Total Price"):
    result = calculate_baseboard_price(
        linear_feet,
        prep_level,
        add_caulk,
        add_sanding,
        add_quarter_round
    )

    st.subheader("💵 Price Breakdown")
    for item, cost in result.items():
        st.write(f"**{item}:** ${cost}")