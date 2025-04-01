import streamlit as st
import datetime
import csv
import io

def calculate_baseboard_price(linear_feet, prep_key):
    base_rates = {
        'light': 1.00,
        'medium': 1.50,
        'heavy': 2.00
    }

    if prep_key not in base_rates:
        raise ValueError("Invalid prep level.")

    base_price = linear_feet * base_rates[prep_key]

    # Automatically add caulking for heavy prep only
    caulk_price = 0.25 * linear_feet if prep_key == "heavy" else 0

    subtotal = base_price + caulk_price
    materials_fee = subtotal * 0.12
    total_price = subtotal + materials_fee

    return {
        'Base Price': round(base_price, 2),
        'Caulking (included with Heavy Prep)': round(caulk_price, 2),
        'Materials Fee (12%)': round(materials_fee, 2),
        'Total Price': round(total_price, 2)
    }

# Prep level descriptions
prep_options = {
    "Light – 1 coat of paint": "light",
    "Medium – 2 coats of paint": "medium",
    "Heavy – Prime + 2 coats, fill holes, sand, caulk": "heavy"
}

# UI
st.set_page_config(page_title="Baseboard Pricing Calculator", layout="centered")
st.markdown("""
# Couleurs Vraies Peinture
**Baseboard Painting Estimate Tool**
""")

client_name = st.text_input("Client Name")
project_name = st.text_input("Project Name / Address")
estimate_date = st.date_input("Estimate Date", value=datetime.date.today())

linear_feet = st.number_input("Total Linear Feet of Baseboard:", min_value=1, value=100)

prep_description = st.selectbox("Prep Level:", list(prep_options.keys()))
prep_key = prep_options[prep_description]

if st.button("Calculate Total Price"):
    result = calculate_baseboard_price(linear_feet, prep_key)

    st.subheader("💵 Price Breakdown")
    for item, cost in result.items():
        st.write(f"**{item}:** ${cost}")

    # Text output
    text_output = f"""
Couleurs Vraies Peinture

Client: {client_name}
Project: {project_name}
Date: {estimate_date.strftime('%Y-%m-%d')}

Total Linear Feet: {linear_feet}
Prep Level: {prep_description}

--- Estimate ---
"""
    for item, cost in result.items():
        text_output += f"{item}: ${cost}\n"

    text_output += "\nMerci pour votre confiance! / Thank you for your trust!"

    st.download_button("📄 Download Quote (Text)", text_output, file_name="baseboard_quote.txt")

    # CSV output
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Client", "Project", "Date", "Linear Feet", "Prep Level"])
    writer.writerow([client_name, project_name, estimate_date, linear_feet, prep_description])
    writer.writerow([])
    writer.writerow(["Item", "Cost ($)"])
    for item, cost in result.items():
        writer.writerow([item, cost])

    st.download_button("📊 Download Quote (CSV)", csv_buffer.getvalue(), file_name="baseboard_quote.csv", mime="text/csv")

