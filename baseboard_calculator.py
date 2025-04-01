import streamlit as st
import datetime
import csv
import io
from fpdf import FPDF

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
st.markdown("""
# Couleurs Vraies Peinture
**Baseboard Painting Estimate Tool**
1103 Rues des fondateurs, Paquetville, NB, E8R 1B3  
📞 506-397-1618 | ✉️ couleurvraiespeinture@gmail.com
""")

client_name = st.text_input("Client Name")
project_name = st.text_input("Project Name / Address")
estimate_date = st.date_input("Estimate Date", value=datetime.date.today())

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

    # Format plain text quote
    text_output = f"""
Couleurs Vraies Peinture
1103 Rues des fondateurs, Paquetville, NB, E8R 1B3
506-397-1618 | couleurvraiespeinture@gmail.com

Client: {client_name}
Project: {project_name}
Date: {estimate_date.strftime('%Y-%m-%d')}

Total Linear Feet: {linear_feet}
Prep Level: {prep_level.title()}

--- Estimate ---
"""
    for item, cost in result.items():
        text_output += f"{item}: ${cost}\n"

    text_output += "\nMerci pour votre confiance! / Thank you for your trust!"

    st.download_button("📄 Download Quote (Text)", text_output, file_name="baseboard_quote.txt")

    # Create CSV buffer
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Client", "Project", "Date", "Linear Feet", "Prep Level"])
    writer.writerow([client_name, project_name, estimate_date, linear_feet, prep_level])
    writer.writerow([])
    writer.writerow(["Item", "Cost ($)"])
    for item, cost in result.items():
        writer.writerow([item, cost])

    st.download_button("📊 Download Quote (CSV)", csv_buffer.getvalue(), file_name="baseboard_quote.csv", mime="text/csv")

    # Create PDF quote
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Couleurs Vraies Peinture", ln=True, align='L')
    pdf.cell(200, 10, txt="1103 Rues des fondateurs, Paquetville, NB, E8R 1B3", ln=True, align='L')
    pdf.cell(200, 10, txt="506-397-1618 | couleurvraiespeinture@gmail.com", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Client: {client_name}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Project: {project_name}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Date: {estimate_date.strftime('%Y-%m-%d')}", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Linear Feet: {linear_feet}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Prep Level: {prep_level.title()}", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt="--- Estimate ---", ln=True, align='L')
    for item, cost in result.items():
        pdf.cell(200, 10, txt=f"{item}: ${cost}", ln=True, align='L')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Merci pour votre confiance! / Thank you for your trust!")

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    st.download_button("🧾 Download Quote (PDF)", pdf_buffer.getvalue(), file_name="baseboard_quote.pdf", mime="application/pdf")
